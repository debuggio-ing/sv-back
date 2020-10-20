import requests

PROTECTED_ENDPOINT = 'http://127.0.0.1:8000/protected'
LOGIN_ENDPOINT = 'http://127.0.0.1:8000/login'

token = "Bearer not_valid_jwt_access_token"

with requests.Session() as s:
    r1 = requests.get(PROTECTED_ENDPOINT, headers={"Authorization": token})

# r.text == {"detail":"Not enough segments"}
print(r1.text)

# r2 = requests.post(LOGIN_ENDPOINT, data = , headers={"Content-Type":"application/json"})

payload = {"username":"test","password":"test"}
with requests.Session() as s:
    r2 = s.post(LOGIN_ENDPOINT, data=payload, headers={"Content-Type":"application/json"})

print(r2.content)