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
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    #usertype = db.Column(db.String(50), nullable=False, default="client")

with app.app_context():
    db.create_all()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        res = make_response(jsonify(success=True))
        res.set_cookie('session', f'{username} logged_in')
        return res
    else:
        return jsonify(success=False, message="Invalid credentials"), 401

@app.route('/protected')
def protected():
    session_cookie = request.cookies.get('session')
    if 'logged_in' in session_cookie:
    #if session_cookie.__contains__('logged_in'):
    #if session_cookie:
        return jsonify(access=True)
    elif 'registered' in session_cookie:
        return jsonify(access=True)
    else:
        return jsonify(access=False), 403

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify(success=False, message="Please fill the required fields"), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify(success=False, message="Username already taken!"), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    res = make_response(jsonify(success=True))
    res.set_cookie('session', f'{username} registered')
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
    username = request.cookies.get('session')

    if not username:
        return jsonify(success=False, message="Not logged in"), 401

    if "logged_in" in username:
        username = username.replace(" logged_in", "")
    else:
        username = username.replace(" registered", "")
    deleted_count = db.session.query(User).filter_by(username=username).delete()

    if deleted_count > 0:
        db.session.commit()
        return jsonify(success=True, message=f"User '{username}' deleted.")
    else:
        return jsonify(success=False, message="User not found."), 404


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
    app.run(debug=True)


'''
To delete user via Postman
DELETE /delete_user

To view users via Postman
GET /view_users

'''


