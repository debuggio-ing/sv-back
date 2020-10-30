from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.test import test_svapi
from app.database.crud import *

# It's necessary to remove database before running the tests.
testc = TestClient(test_svapi)

# Setup database
NUM_OF_PLAYERS = 5

tokens = []
for x in range(NUM_OF_PLAYERS):
    user = UserReg(username="user" + str(x), email=str(x)+'@gmail.com',
        password='testPassword')
    if user.email not in get_emails():
        register_user(user)
    
    login = testc.post("api/login/",
        headers={"Content-Type": "application/json"},
        json={"email": user.email, "password": user.password})

    token = "Bearer " + login.json()["access_token"]
    tokens.append(token)

max_players = 5
lobby_name = "test_lobby"
create1 = testc.post(
    "/api/lobbies/new/",
    headers={
        "Authorization": tokens[0]},
    json={
        "name": lobby_name,
        "max_players": max_players})

lobby1_id = create1.json()["id"]
join = testc.post(
    "/api/lobbies/" +
    str(lobby1_id) +
    "/join/",
    headers={
        "Authorization": tokens[1]})

create2 = testc.post(
    "/api/lobbies/new/",
    headers={
        "Authorization": tokens[0]},
    json={
        "name": lobby_name,
        "max_players": max_players})

# Try to get all lobbies.
def test_get_lobby_list():
    get_all = testc.get(
        "/api/users/games/",
        headers={
            "Authorization": tokens[0]})

    assert get_all.status_code == 200