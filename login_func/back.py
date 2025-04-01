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
        res.set_cookie('session', 'logged_in')
        return res
    else:
        return jsonify(success=False, message="Invalid credentials"), 401

@app.route('/protected')
def protected():
    session_cookie = request.cookies.get('session')
    if session_cookie == 'logged_in':
        return jsonify(access=True)
    else:
        return jsonify(access=False), 403

#Tam, kad butu hashed passwordas database ir veiktu loginas reikia addint per postmana
# post pasirenki body/raw ir pastint sita dali
# {
#     "username": "adas",
#     "password": "padas"
# }

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(success=True, message="User added successfully!")

#Jeigu reikes istrinti useri
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

#perziuret database
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
