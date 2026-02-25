import requests
import pprint

BASE_URL = 'http://127.0.0.1:5000/'
resp = requests.get(BASE_URL + 'search?title=Texas Chainsaw Massacre&creator=Tope', headers = {'X-Access-Token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjEsImV4cCI6MTc3MjA0NzEwMH0.Dt47bDRJx7NLMs1VK-aD1FD75YNkd8ayWRYpAQVEw9g'})
print(resp.status_code)
pprint.pprint(resp.json())