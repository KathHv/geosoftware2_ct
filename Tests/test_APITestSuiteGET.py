import requests
import json

'''
GET-Request: List Users, Single User
Request:
Response: 200

'''
BASE_URL = "https://reqres.in/"
params = {"page": 2}
#print (BASE_URL)
response = requests.get(BASE_URL + "api/users?",params=params)

#print (response)
#print (response.json())
print (json.dumps(response.json(), indent=4))

resp = response.json()

'''
GET-Request: Single User not found
Request:
Response: 404
'''
BASE_URL = "https://reqres.in/"
response = requests.get(BASE_URL + "api/users/23")
print (json.dumps(response.json(), indent=4))
resp = response.json()
print (response)

'''
GET-Request: List <Resource>
Request:
Response: 200
'''
BASE_URL = "https://reqres.in/"
response = requests.get(BASE_URL + "api/unknown")
print (json.dumps(response.json(), indent=4))
resp = response.json()
print (response)

'''
GET-Request: Single <Resource>
Request:
Response: 200
'''
BASE_URL = "https://reqres.in/"
response = requests.get(BASE_URL + "api/unknown/2")
print (json.dumps(response.json(), indent=4))
resp = response.json()
print (response)

'''
GET-Request: Single <Resource>
Request:
Response: 404
'''
BASE_URL = "https://reqres.in/"
response = requests.get(BASE_URL + "api/unknown/23")
print (json.dumps(response.json(), indent=4))
resp = response.json()
print (response)

'''
GET-Request: Delayed Response
Request:
Response: 200
'''
BASE_URL = "https://reqres.in/"
response = requests.get(BASE_URL + "api/users?delay=3")
print (json.dumps(response.json(), indent=4))
resp = response.json()
print (response)