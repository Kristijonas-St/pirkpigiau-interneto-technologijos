from flask import Flask, request, jsonify, make_response

back = Flask(__name__)

@back.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Allow only 'adas' & 'padas' to access /protected
    if username in ['adas', 'a'] and password in ['padas', 'a']:
        res = make_response(jsonify(success=True))
        if username == 'adas' and password == 'padas':
            res.set_cookie('session', 'logged_in')  # Allows /protected
        else:
            res.set_cookie('session', 'guest')  # This is not allowed in /protected
        return res
    else:
        return jsonify(success=False), 401

@back.route('/protected')
def protected():
    session_cookie = request.cookies.get('session')  # Checking for 'session' cookie

    if session_cookie == 'logged_in': 
        return jsonify(access=True)  # Access granted
    else:
        return jsonify(access=False), 403  # Access denied

if __name__ == "__main__":
    back.run(debug=True)
