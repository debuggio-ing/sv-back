from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.test import test_svapi
from app.database.crud import *

# It's necessary to remove database before running the tests.
lobby = TestClient(test_svapi)

# Setup database
user1 = UserReg(
    username='user1',
    email='1@gmail.com',
    password='testPassword')
if user1.email not in get_emails():
    register_user(user1)

user2 = UserReg(
    username='user2',
    email='2@gmail.com',
    password='testPassword')
if user2.email not in get_emails():
    register_user(user2)

login1 = lobby.post(
    "api/login/",
    headers={
        "Content-Type": "application/json"},
    json={
        "email": user1.email,
        "password": user1.password})

login2 = lobby.post(
    "api/login/",
    headers={
        "Content-Type": "application/json"},
    json={
        "email": user2.email,
        "password": user2.password})

token1 = "Bearer " + login1.json()["access_token"]
max_players = 5
lobby_name = "test_lobby"
create1 = lobby.post(
    "/api/lobbies/new/",
    headers={
        "Authorization": token1},
    json={
        "name": lobby_name,
        "max_players": max_players})

token2 = "Bearer " + login2.json()["access_token"]
lobby1_id = create1.json()["id"]
join = lobby.post(
    "/api/lobbies/" +
    str(lobby1_id) +
    "/join/",
    headers={
        "Authorization": token2})

create2 = lobby.post(
    "/api/lobbies/new/",
    headers={
        "Authorization": token1},
    json={
        "name": lobby_name,
        "max_players": max_players})

# Try to get all lobbies.
def test_get_lobby_list():
    get_all = lobby.get(
        "/api/lobbies/",
        headers={
            "Authorization": token1})

    assert get_all.status_code == 200
    assert get_all.json() == [{"id": lobby1_id,
                               "name": join.json()["name"],
                               "current_players":join.json()["current_players"],
                               "max_players":join.json()["max_players"],
                               "started":join.json()["started"]},
                              {"id": create2.json()["id"],
                               "name":create2.json()["name"],
                               "current_players":create2.json()["current_players"],
                               "max_players":create2.json()["max_players"],
                               "started":join.json()["started"]}]

# Try to get all lobbies not being logged in.
def test_get_lobbies_not_logged_in():
    get_all = lobby.get("/api/lobbies/")

    assert get_all.status_code == 401
    assert get_all.json() == {'detail': 'Missing Authorization Header'}

# Test lobby_from argument.
def test_lobby_from():
    get_all = lobby.get(
        "/api/lobbies/?lobby_from=2",
        headers={
            "Authorization": token1})

    assert get_all.status_code == 200
    assert get_all.json() == [{"id": create2.json()["id"],
                               "name":create2.json()["name"],
                               "current_players":create2.json()["current_players"],
                               "max_players":create2.json()["max_players"],
                               "started":join.json()["started"]}]

# Test lobby_to argument.
def test_lobby_to():
    get_all = lobby.get(
        "/api/lobbies/?lobby_to=1",
        headers={
            "Authorization": token1})

    assert get_all.status_code == 200
    assert get_all.json() == [{"id": lobby1_id,
                               "name": join.json()["name"],
                               "current_players":join.json()["current_players"],
                               "max_players":join.json()["max_players"],
                               "started":join.json()["started"]}]
