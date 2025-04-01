from flask import Flask, request, jsonify, make_response

back = Flask(__name__)

@back.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    res = make_response(jsonify(success=True))
    
    if username == 'adas' and password == 'padas':
        res.set_cookie('session', 'logged_in')
    elif username == 'a' and password == 'a':
        res.set_cookie('session', 'guest')
    else:
        return jsonify(success=False), 401

    print(f"User {username} logged in with session: {res.headers.get('Set-Cookie')}")
    return res

@back.route('/protected')
def protected():
    session_cookie = request.cookies.get('session')  
    print(f"Session Cookie Received: {session_cookie}")

    if session_cookie == 'logged_in': 
        return jsonify(access=True)
    else:
        return jsonify(access=False), 403

if __name__ == "__main__":
    back.run(debug=True)
