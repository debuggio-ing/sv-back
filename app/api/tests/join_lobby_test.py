from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import svapi
from app.database.crud import *


client = TestClient(svapi)

def test_join_lobby():
    if '1@gmail.com' not in get_emails():
        user = UserReg(username='user1',email='1@gmail.com',password='testPassword')
        register_user(user)

    if '2@gmail.com' not in get_emails():
        user = UserReg(username='user2',email='2@gmail.com',password='testPassword')
        register_user(user)

    login1 = client.post("api/login/",headers={"Content-Type": "application/json"},
        json={"email": "1@gmail.com","password": "testPassword"})

    login2 = client.post("api/login/",headers={"Content-Type": "application/json"},
        json={"email": "2@gmail.com","password": "testPassword"})

    # assert (login1.json()["access_token"][:6], login2.json()["access_token"][:6]) == "hola"
    token1 = "Bearer " + login1.json()["access_token"]
    create = client.post("/api/lobbies/new/", headers={"Authorization": token1},
     json={"name":"test_lobby","max_players":5})

    # assert create.json()['id'] == 4
    token2 = "Bearer " + login2.json()["access_token"]
    lobby_id = create.json()["id"]
    # assert "/api/lobbies/"+ str(lobby_id) + "/new/" == "sdfgsdfg"
    join = client.post("/api/lobbies/"+ str(lobby_id) + "/join/", headers={"Authorization": token2})

    assert join.json() == {"hola":4}