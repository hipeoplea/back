import sqlite3
from flask import Flask, jsonify
import uuid

app = Flask(__name__)
sql = sqlite3.connect('memes.db', check_same_thread=False)
con = sql.cursor()


@app.route('/get_memes/<id>', methods=['GET'])
def give_memes(id):
    try:
        resp = con.execute("SELECT * from users where id = ?", (id,)).fetchone()
        if resp:
            last_memeid = con.execute("Select * from mem ORDER by priority DESC, likes ASC ").fetchall()
            if resp[3]:
                print(resp[3])
                viewed = resp[3].split(' ')
                if len(viewed) >= len(last_memeid) + 2:
                    viewed = ['-3', '-2']
            else:
                viewed = ['-3', '-2']
            counter = 0
            while True:
                if str(last_memeid[counter][0]) not in viewed:
                    answ = last_memeid[counter]
                    print(answ)
                    break
                counter += 1
            chtoto = con.execute("Update users set last_pic = ?, viewed = ? where id = ?",
                                 (answ[0], " ".join(viewed) + " " + str(answ[0]), id))
            sql.commit()
            memes = [
                {'id': str(answ[0]),
                 'url': str(answ[1]),
                 'author': str(answ[2]),
                 'likes': str(answ[3])
                 }]
            return jsonify({'memes': memes})
        else:
            return jsonify({'error': 'authentication error'})
    except Exception as Error:
        return jsonify({'error': str(Error)})


@app.route('/like_meme/<id>', methods=['GET'])
def like_meme(id):
    try:
        resp = con.execute("SELECT role from users where id = ?", (id,)).fetchone()
        if resp:
            mem_id = int(con.execute("SELECT last_pic from users where id =?", (id,)).fetchone()[0])
            an = con.execute("SELECT * from mem where id = ?", (mem_id,)).fetchall()
            if an:
                answ = con.execute("UPDATE mem SET likes = likes + 1 WHERE id = ? ", (mem_id,))
                sql.commit()
                return jsonify({'liked': True})
            else:
                return jsonify({'error': 'element with such id does not exist'})
        else:
            return jsonify({'error': 'authentication error'})
    except Exception as Error:
        return jsonify({'error': str(Error)})


@app.route('/skip_meme/<id>', methods=['GET'])
def skip_meme(id):
    try:
        mem_id = con.execute("SELECT last_pic from users where id =?", (id,)).fetchone()[0]
        an = con.execute("SELECT * from mem where id = ?", (mem_id,)).fetchall()
        answ = con.execute("UPDATE mem SET likes = likes - 1 WHERE id = ? and likes > 0", (mem_id,))
        sql.commit()
        return jsonify({'skipped': True})
    except Exception as Error:
        return jsonify({'error': str(Error)})


@app.route('/add_user', methods=['GET'])
def add_role():
    try:
        hash = uuid.uuid1().hex
        add = con.execute('INSERT into users values (?, ?, ?, ?)', (str(hash), str(0), 0, ''))
        sql.commit()
        return jsonify({'token': hash})
    except Exception as Error:
        return jsonify({'error': str(Error)})


@app.route('/make_admin/<token>', methods=['GET'])
def make_admin(token):
    try:
        usr = con.execute('SELECT * From users where id = ?', (token,)).fetchall()
        if usr:
            up = con.execute("UPDATE users SET role = 1 where id = ?", (token,))
            sql.commit()
            return jsonify({"role_change": True})
        else:
            return jsonify({"error": 'this user does not exist'})
    except Exception as Error:
        return jsonify({'error': str(Error)})


@app.route('/priority/<id_mem>')
def priority(id_mem):
    try:
        mem = con.execute("Select * from mem where id = ?", (id_mem,)).fetchall()
        if mem:
            resp = con.execute("UPDATE mem set priority = 1 where id = ?", (id_mem,))
            sql.commit()
            return jsonify({'change_priority': True})
        else:
            return jsonify({'error': 'mem with this id does not exist'})
    except Exception as Error:
        return jsonify({'error': str(Error)})


@app.route('/dashboard/<id>')
def dashboard(id):
    try:
        resp = con.execute("SELECT * from users where id = ?", (id,)).fetchone()
        if resp[2] == 1:
            memes = []
            stats = con.execute("Select * from mem ORDER by likes DESC ").fetchall()
            for i in stats:
                memes.append(
                    {'id': i[0],
                     'url': i[1],
                     'author': i[2],
                     'likes': i[3],
                     'priority': i[4]
                     })
            return jsonify({'stats': memes})
        else:
            return jsonify({'error': 'authentication error'})
    except Exception as Error:
        return jsonify({'error': str(Error)})

if __name__ == '__main__':
    app.run(debug=True)
