import requests

BASE_URL = 'http://127.0.0.1:5000/'
resp = requests.get(BASE_URL + 'login', json = {'token': '560ca5ea16d796f7', 'email': 'erick1204200100@gmail.com'})
print(resp.status_code)
print(resp.json())