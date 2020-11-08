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

token1 = "Bearer " + login1.json()["access_token"]


# Try to get all lobbies with no lobbies created.
def test_get_empty_lobby_list():
    get_all = lobby.get(
        "/api/lobbies/",
        headers={
            "Authorization": token1})

    assert get_all.status_code == 200
    assert get_all.json() == []
