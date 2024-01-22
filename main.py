

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Создаем базу данных SQLite и таблицу, если их нет
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        timestamp DATETIME NOT NULL
    )
''')
conn.commit()
conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_name = request.form['name']
        timestamp = datetime.now()

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, timestamp) VALUES (?, ?)', (user_name, timestamp))
        conn.commit()
        conn.close()

        return redirect(url_for('users_list'))

    return render_template('index.html')

@app.route('/users-list')
def users_list():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, timestamp FROM users ORDER BY timestamp DESC')
    users = cursor.fetchall()
    conn.close()

    return render_template('users_list.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)