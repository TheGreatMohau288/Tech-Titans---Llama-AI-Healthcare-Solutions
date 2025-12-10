from flask import Flask, request, session, jsonify
from sqlite_techtitans import init_db, create_user, verify_user, get_user
import os

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET', 'replace-with-secure-secret')
DB_PATH = os.environ.get('DB_PATH', 'data.db')

init_db(DB_PATH)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '')
    if not username or not password:
        return jsonify({'error': 'username and password required'}), 400
    ok = create_user(username, password, path=DB_PATH)
    return jsonify({'created': ok}), (201 if ok else 409)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '')
    if verify_user(username, password, path=DB_PATH):
        session['user'] = username
        return jsonify({'login': True})
    return jsonify({'login': False}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({'logout': True})

@app.route('/me')
def me():
    user = session.get('user')
    if not user:
        return jsonify({'user': None}), 401
    info = get_user(user, path=DB_PATH)
    info.pop('password_hash', None)
    return jsonify({'user': info})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)