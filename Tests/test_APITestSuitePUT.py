#author: Ilka Pleiser
import requests
import json

'''
PUT-Request: Update
Request:
Response: 200
'''
BASE_URL = "https://reqres.in/"
payload = {
    "name": "morpheus",
    "job": "zion resident"
}
response = requests.put(BASE_URL + "api/users/2", data = payload)
print (json.dumps(response.json(), indent=4))
resp = response.json()
print (response)
