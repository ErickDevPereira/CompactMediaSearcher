import requests
import pprint

BASE_URL = 'http://127.0.0.1:5000/'
resp = requests.get(BASE_URL + 'search?title=God of War&creator=Matthew', headers = {'X-Access-Token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjEsImV4cCI6MTc3MTk5Mzg3N30.97aKiMITlTPDc6rr-A2cuUApR6YFdNGyNj1jenEoYm8'})
print(resp.status_code)
pprint.pprint(resp.json())