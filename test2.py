'''import requests

BASE_URL = 'http://127.0.0.1:5000/'
resp = requests.post(BASE_URL + 'register', json = {'first_name': 'Erick', 'last_name': 'Pereira', 'email': 'erick120420000@gmail.com'})
print(resp.status_code)
print(resp.json())'''

import datetime
print(str(datetime.timedelta(minutes = 10)))