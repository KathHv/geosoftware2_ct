#author: Ilka Pleiser
import requests
import json

'''
POST-Request: Create
Request:
Response: 201
'''
BASE_URL = "https://reqres.in/"
payload = {
    "name": "morpheus",
    "job": "leader"
}
response = requests.post(BASE_URL + "api/users", data = payload)
#print (response.json())
print (json.dumps(response.json(), indent=4))
print (response)

'''
POST-Request: Register - Successful
Request:
Response: 201
'''
BASE_URL = "https://reqres.in/"
payload = {
    "email": "sydney@fife",
    "password": "pistol"
}
response = requests.post(BASE_URL + "api/register", data = payload)
#print (response.json())
print (json.dumps(response.json(), indent=4))
print (response)

'''
POST-Request: Register - Unsuccessful
Request:
Response: 400
'''
BASE_URL = "https://reqres.in/"
payload = {
    "email": "sydney@fife",
}
response = requests.post(BASE_URL + "api/register", data = payload)
#print (response.json())
print (json.dumps(response.json(), indent=4))
print (response)

'''
POST-Request: Login - Successful
Request:
Response: 200
'''
BASE_URL = "https://reqres.in/"
payload = {
    "email": "peter@klaven",
    "password": "cityslicka"
}
response = requests.post(BASE_URL + "api/login", data = payload)
#print (response.json())
print (json.dumps(response.json(), indent=4))
print (response)

'''
POST-Request: Login - Unsuccessful
Request:
Response: 400
'''
BASE_URL = "https://reqres.in/"
payload = {
    "email": "peter@klaven",
}
response = requests.post(BASE_URL + "api/login", data = payload)
#print (response.json())
print (json.dumps(response.json(), indent=4))
print (response)