import requests

BASE_URL = 'http://127.0.0.1:5000/'
resp = requests.get(BASE_URL + 'login', json = {'token': '014bab26cc492bab', 'email': 'erick120420000@gmail.com'})
print(resp.status_code)
print(resp.json())