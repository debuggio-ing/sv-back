from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.test import test_svapi
from app.database.crud import *

# It's necessary to remove database before running the tests.
testc = TestClient(test_svapi)

# Setup database
NUM_OF_PLAYERS = 6

tokens = []
users = []
for x in range(NUM_OF_PLAYERS):
    user = UserReg(nickname="user" + str(x), email=str(x) + '@gmail.com',
                   password='testPassword')
    if user.email not in get_emails():
        register_user(user)
    users.append(user)

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


create2 = testc.post(
    "/api/lobbies/new/",
    headers={
        "Authorization": tokens[0]},
    json={
        "name": lobby_name,
        "max_players": max_players})
lobby2_id = create2.json()["id"]

for i in range(1, len(tokens) - 1):
    join1 = testc.post("/api/lobbies/" + str(lobby1_id) + "/join/",
                       headers={"Authorization": tokens[i]})
    join2 = testc.post("/api/lobbies/" + str(lobby2_id) + "/join/",
                       headers={"Authorization": tokens[i]})


start1 = testc.post("/api/lobbies/" + str(lobby1_id) + "/start/",
                    headers={"Authorization": tokens[0]})

start2 = testc.post("/api/lobbies/" + str(lobby2_id) + "/start/",
                    headers={"Authorization": tokens[0]})


# Try to get all user games.
def test_get_user_games():
    user_games = testc.get(
        "/api/users/games/",
        headers={
            "Authorization": tokens[0]})

    user_games_json = user_games.json()

    assert user_games.status_code == 200
    assert user_games_json["email"] == users[0].email
    assert user_games_json["games"] == [lobby1_id, lobby2_id]


# Try to get user games but user was not inside any game.
def test_get_user_games_empty():
    user_games = testc.get(
        "/api/users/games/",
        headers={
            "Authorization": tokens[-1]})

    user_games_json = user_games.json()

    assert user_games.status_code == 200
    assert user_games_json["email"] == users[-1].email
    assert user_games_json["games"] == []


# Try to get user games and user was inside only one game.
def test_get_user_games_one_entry():
    join1 = testc.post("/api/lobbies/" + str(lobby1_id) + "/join/",
                       headers={"Authorization": tokens[-1]})

    user_games = testc.get(
        "/api/users/games/",
        headers={
            "Authorization": tokens[-1]})

    user_games_json = user_games.json()

    assert user_games.status_code == 200
    assert user_games_json["email"] == users[-1].email
    assert user_games_json["games"] == [lobby1_id]
