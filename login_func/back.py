from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

    if user and user.password == password:
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

if __name__ == "__main__":
    app.run(debug=True)
