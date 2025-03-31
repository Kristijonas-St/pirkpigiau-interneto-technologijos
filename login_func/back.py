from flask import Flask, request, jsonify, make_response

back = Flask(__name__)


@back.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == 'adas' and password == 'padas':
        res = make_response(jsonify(success=True))
        res.set_cookie('session', 'logged_in')
        return res
    else:
        return jsonify(success=False), 401
    
@back.route('/protected')
def protected():
    session_cookie = request.cookies.get('session')
    if session_cookie == 'logged_in':
        return jsonify(access=True)
    else:
        return jsonify(access=False), 403
    
if __name__ == "__main__":
    back.run(debug=True)