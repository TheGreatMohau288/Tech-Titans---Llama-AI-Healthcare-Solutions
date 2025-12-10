import sqlite3
import bcrypt
import os
from datetime import datetime

DB_PATH = 'data.db'  # move this file outside repo or add to .gitignore

def init_db(path=DB_PATH):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password_hash BLOB NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def create_user(username: str, password: str, path=DB_PATH) -> bool:
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())  # bcrypt includes the salt
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute('INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)',
                    (username, hashed, datetime.utcnow().isoformat()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # username already exists
        return False
    finally:
        conn.close()

def verify_user(username: str, password: str, path=DB_PATH) -> bool:
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return False
    stored_hash = row[0]
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash)

if __name__ == '__main__':
    init_db()

    # quick interactive demo (remove for production)
    while True:
        action = input('Action [register/login/quit]: ').strip().lower()
        if action == 'quit':
            break
        username = input('username: ').strip()
        password = input('password: ').strip()
        if action == 'register':
            ok = create_user(username, password)
            print('Registered' if ok else 'Username already exists')
        elif action == 'login':
            ok = verify_user(username, password)
            print('Login successful' if ok else 'Login failed')
        else:
            print('Unknown action')