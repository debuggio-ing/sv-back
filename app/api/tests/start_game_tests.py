from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.test import test_svapi
from app.database.crud import *


testc = TestClient(test_svapi)


def test_start_game():
    # Setup database
    user1 = UserReg(username='user1', email='1@gmail.com',
        password='testPassword')
    if user1.email not in get_emails():
        register_user(user1)

    login = testc.post("api/login/",
        headers={"Content-Type": "application/json"},
        json={"email": user1.email, "password": user1.password})

    token = "Bearer " + login.json()["access_token"]

    create_lobby = lobby.post("/api/lobbies/new/",
        headers={"Authorization": token},
        json={"name": "lobby_test", "max_players": 7})

    lobby_id = create_lobby.json()[lobby_id]
    start = testc.post("api/lobbies/" + str(lobby_id) + "/start/",
        headers={"Authorization": token})

    print(start.json())

    assert 200 == 300


