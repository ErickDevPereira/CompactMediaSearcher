import requests

BASE_URL = 'http://127.0.0.1:5000/'
resp = requests.post(BASE_URL + 'register', json = {'email': 'erick1204200100@gmail.com', 'first_name': 'Erick', 'last_name': 'Pereira'})
print(resp.status_code)
print(resp.json())