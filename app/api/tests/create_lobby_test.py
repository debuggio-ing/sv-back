from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import svapi
from app.database.crud import *


lobby = TestClient(svapi)


# Try to crate a lobby.
def test_create_lobby():
    if 'test@gmail.com' not in get_emails():
        user = UserReg(
            username='test',
            email='test@gmail.com',
            password='testPassword')
        register_user(user)

    login = lobby.post(
        "api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": "test@gmail.com",
            "password": "testPassword"})

    token = "Bearer " + login.json()["access_token"]
    response = lobby.post("/api/lobbies/new/", headers={"Authorization": token}, json={"name":"test_lobby","max_players":5})

    assert response.status_code == 201
    assert response.json() == {'current_players': ['test'], 'max_players': 5, 'name': 'test_lobby'}

# Try to crate a lobby not being logged in.
def test_create_lobby_unlogged():
    response = lobby.post("/api/lobbies/new/", json={"name":"test_lobby","max_players":5})

    assert response.status_code == 401
    assert response.json() == {'detail': 'Missing Authorization Header'}
