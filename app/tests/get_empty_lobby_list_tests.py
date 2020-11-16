from fastapi.testclient import TestClient

from app.debug.populate_database import *
from app.debug.set_db_to_proclaim import *
from app.debug.spell_database import *
from app.test import test_svapi

# It's necessary to remove database before running the tests.
lobby = TestClient(test_svapi)

# Setup database
user1 = UserReg(
    nickname='user1',
    email='1@gmail.com',
    password='testPassword')
if user1.email not in get_emails():
    register_user(user1)

user2 = UserReg(
    nickname='user2',
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

token1 = "Bearer " + login1.json()["access_token"]


# Try to get all lobbies with no lobbies created.
def test_get_empty_lobby_list():
    get_all = lobby.post(
        "/api/lobbies/",
        json={
            "available": "true",
            "started": "false",
            "finished": "false",
            "user_games": "false",
            "all_games": "true"},
        headers={
            "Authorization": token1})

    assert get_all.status_code == 200
    assert get_all.json() == []
