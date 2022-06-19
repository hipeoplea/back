# в файле test.py примеры запросов
import sqlite3
from flask import Flask, jsonify, Response

app = Flask(__name__)
sql = sqlite3.connect('memes.db', check_same_thread=False)

#метод возвращает список мемов с данными о них
@app.route('/get_memes', methods=['GET'])
def give_memes():
    try:
        memes = []
        con = sql.cursor()
        answ = con.execute("SELECT * from mem").fetchall()
        for i in answ:
            memes.append(
                {'id': i[0],
                 'url': i[1],
                 'author': i[2],
                 'likes': i[3]
                 })
        return jsonify({'memes': memes})
    except Exception as Error:
        return jsonify({'error': str(Error)})

#количество лайков у мема с заданным id увеличивается на 1
@app.route('/like_meme/<mem_id>', methods=['GET'])
def like_meme(mem_id):
    try:
        con = sql.cursor()
        an = con.execute("SELECT * from mem where id = ?", (mem_id,)).fetchall()
        if an:
            answ = con.execute("UPDATE mem SET likes = likes + 1 WHERE id = ? ", (mem_id,))
            sql.commit()
            return jsonify({'liked': True})
        else:
            return jsonify({'error': 'element with such id does not exist'})
    except Exception as Error:
        return jsonify({'error': str(Error)})

#количество лайков у мема с заданным id уменьшается на 1
@app.route('/skip_meme/<mem_id>', methods=['GET'])
def skip_meme(mem_id):
    try:
        con = sql.cursor()
        an = con.execute("SELECT * from mem where id = ?", (mem_id,)).fetchall()
        if an:
            answ = con.execute("UPDATE mem SET likes = likes - 1 WHERE id = ? ", (mem_id,))
            sql.commit()
            return jsonify({'skipped': True})
        else:
            return jsonify({'error': 'element with such id does not exist'})
    except Exception as Error:
        return jsonify({'error': str(Error)})


if __name__ == '__main__':
    app.run(debug=True)