from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sympy import failing_assumptions

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

with app.app_context():
    db.create_all()

import jwt
import datetime

# Secret key for encoding/decoding JWTs
app.config['SECRET_KEY'] = 'your-secret-key'

def generate_jwt(username):
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=15)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def decode_jwt(token):
    try:
        return jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        token = generate_jwt(username)
        res = make_response(jsonify(success=True))
        res.set_cookie('token', token, httponly=True, secure=True, samesite='Strict')
        return res
    else:
        return jsonify(success=False, message="Invalid credentials"), 401

@app.route('/protected')
def protected():
    token = request.cookies.get('token')
    if not token:
        return jsonify(access=False, message="No token"), 403

    decoded = decode_jwt(token)
    if decoded:
        return jsonify(access=True, user=decoded['username'])
    else:
        return jsonify(access=False, message="Invalid or expired token"), 403


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify(success=False, message="Please fill the required fields"), 400

    if len(username) < 5 or len(username) > 20:
        return jsonify(success=False, message="Username must be between 5 and 20 characters long"), 400

    if len(password) < 6 or len(password) > 20:
        return jsonify(success=False, message="Password must be between 6 and 20 characters long"), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify(success=False, message="Username already taken!"), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    token = generate_jwt(username)
    res = make_response(jsonify(success=True))
    res.set_cookie('token', token, httponly=True, secure=True, samesite='Strict')
    return res

@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    data = request.get_json()
    username = data.get('username')

    deleted_count = db.session.query(User).filter_by(username=username).delete()

    if deleted_count > 0:
        db.session.commit()
        return jsonify(success=True, message="User deleted successfully!")
    else:
        return jsonify(success=False, message="User not found!"), 404

@app.route('/delete_logged_user', methods=['DELETE'])
def delete_logged_user():
    token = request.cookies.get('token')

    if not token:
        return jsonify(success=False, message="Token missing"), 401

    decoded = decode_jwt(token)
    if not decoded:
        return jsonify(success=False, message="Invalid or expired token"), 403

    username = decoded.get('username')
    if not username:
        return jsonify(success=False, message="Username missing in token"), 400

    deleted_count = db.session.query(User).filter_by(username=username).delete()

    if deleted_count > 0:
        db.session.commit()
        return jsonify(success=True, message=f"User '{username}' deleted.")
    else:
        return jsonify(success=False, message="User not found"), 404



@app.route('/view_users', methods=['GET'])
def view_users():
    users = User.query.all()

    users_data = []
    for user in users:
        user_info = {
            'id': user.id,
            'username': user.username,
            'password': user.password
        }
        users_data.append(user_info)

    return jsonify(users_data)

if __name__ == "__main__":
    app.run(ssl_context=("cert.pem", "key.pem"))
