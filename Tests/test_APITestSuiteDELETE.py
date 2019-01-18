#author: Ilka Pleiser
import requests
import json

'''
DELETE-Request: Delete
Request:
Response: 204
'''
BASE_URL = "https://reqres.in/"
response = requests.delete(BASE_URL + "api/users/2")
print (response.status_code)
print (response)
