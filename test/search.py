import requests
import pprint

BASE_URL = 'http://127.0.0.1:5000/'
resp = requests.get(BASE_URL + 'search?title=The Lord of the Rings&creator=John Ronald', headers = {'X-Access-Token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjEsImV4cCI6MTc3MTk1NjQ3N30.57ExK0896VqBkX15gZxN2EDKi-6sju0qLXVC4LW_nrE'})
print(resp.status_code)
pprint.pprint(resp.json())