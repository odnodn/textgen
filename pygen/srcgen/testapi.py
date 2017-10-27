import requests
server = 'http://localhost:5000'

#r = requests.post(server +'/api/users', json = {"user": {"username": "mo2","email": "mo2@mo.mo","password": "momo"} })

r = requests.get(server +'/api/authors' )
print ( r.json())

