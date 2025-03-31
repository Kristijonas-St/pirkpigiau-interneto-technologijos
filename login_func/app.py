import requests

s = requests.session()

login_url = 'http://localhost:5000/login'
login_data = {'username': 'adas', 'password': 'padas'}

res = s.post(login_url, json=login_data)

if res.json().get('success'):
    print('Login OK')
else:
    print('Login FAILED')

protected_url = 'http://localhost:5000/protected'

res = s.get(protected_url)

if res.json().get('access'):
    print('Access OK')
else:
    print('Access FAILED')



