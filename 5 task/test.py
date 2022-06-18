import requests
import sqlite3

con = sqlite3.connect("memes.db")
cursour = con.cursor()

id = '7f93bbbfef1611ec8ce49408532e44b8'
print(cursour.execute("Select * from mem ORDER by priority DESC, likes ASC ").fetchall())
print(cursour.execute("SELECT * from users where id = ?", (id,)).fetchone())

print(requests.get('http://127.0.0.1:5000/dashboard/7f93bbbfef1611ec8ce49408532e44b8').json())