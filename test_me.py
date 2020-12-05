import requests

BASE = 'http://127.0.0.1:5000/'

response = requests.get(BASE + "City Hall/12/7")
#
print(response.json())


# in order to test the code ->
# first run in terminal mywebservice.py, then run in another terminal test_me.py with wished params
