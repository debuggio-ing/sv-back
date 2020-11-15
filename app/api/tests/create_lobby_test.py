from fastapi.testclient import TestClient
from app.test import test_svapi
from app.database.crud import *
from fastapi.testclient import TestClient

from app.database.crud import *
from app.test import test_svapi

lobby = TestClient(test_svapi)


# Try to crate a lobby.
def test_create_lobby():
    user = UserReg(
        nickname='test',
        email='test@gmail.com',
        password='testPassword')
    if 'test@gmail.com' not in get_emails():
        register_user(user)

    login = lobby.post(
        "api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": user.email,
            "password": user.password})

    token = "Bearer " + login.json()["access_token"]
    lobby_name = "test_lobby"
    lobby_mp = 5
    response = lobby.post(
        "/api/lobbies/new/",
        headers={
            "Authorization": token},
        json={
            "name": lobby_name,
            "max_players": lobby_mp})

    assert response.status_code == 201

    print(response.json())
    assert response.json() == {
        'id': response.json()['id'],
        'current_players': [user.nickname],
        'max_players': lobby_mp,
        'name': lobby_name,
        'started': False,
        "finished": False,
        'is_owner': True}


# Try to crate a lobby not being logged in.
def test_create_lobby_unlogged():
    response = lobby.post(
        "/api/lobbies/new/",
        json={
            "name": "test_lobby",
            "max_players": 5})

    assert response.status_code == 401
    assert response.json() == {'detail': 'Missing Authorization Header'}
