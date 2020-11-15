from fastapi.testclient import TestClient

from app.debug.populate_database import *
from app.debug.set_db_to_proclaim import *
from app.debug.spell_database import *
from app.test import test_svapi

client = TestClient(test_svapi)


# Try to join a valid lobby
def test_join_valid_lobby():
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

    login1 = client.post(
        "api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": user1.email,
            "password": user1.password})

    login2 = client.post(
        "api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": user2.email,
            "password": user2.password})

    token1 = "Bearer " + login1.json()["access_token"]
    max_players = 5
    lobby_name = "test_lobby"
    create = client.post(
        "/api/lobbies/new/",
        headers={
            "Authorization": token1},
        json={
            "name": lobby_name,
            "max_players": max_players})

    token2 = "Bearer " + login2.json()["access_token"]
    lobby_id = create.json()["id"]
    join = client.post(
        "/api/lobbies/" +
        str(lobby_id) +
        "/join/",
        headers={
            "Authorization": token2})

    assert join.status_code == 200
    assert join.json() == {
        'current_players': [
            user1.nickname,
            user2.nickname],
        'id': lobby_id,
        'max_players': max_players,
        'name': lobby_name,
        'started': False,
        'finished': False,
        'is_owner': False}


# Try to join the lobby with no jwt available.
def test_join_lobby_with_no_jwt():
    user = UserReg(
        nickname='user1',
        email='1@gmail.com',
        password='testPassword')
    if user.email not in get_emails():
        register_user(user1)

    login = client.post(
        "api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": "1@gmail.com",
            "password": "testPassword"})

    token = "Bearer " + login.json()["access_token"]
    create = client.post("/api/lobbies/new/", headers={"Authorization": token},
                         json={"name": "test_lobby", "max_players": 5})

    lobby_id = create.json()["id"]
    join = client.post("/api/lobbies/" + str(lobby_id) + "/join/")

    assert join.status_code == 401
    assert join.json() == {'detail': 'Missing Authorization Header'}


# Try to join the lobby with wrong id.
def test_join_lobby_with_wrong_id():
    user = UserReg(
        nickname='user1',
        email='1@gmail.com',
        password='testPassword')
    if user.email not in get_emails():
        register_user(user1)

    login = client.post(
        "api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": "1@gmail.com",
            "password": "testPassword"})

    token = "Bearer " + login.json()["access_token"]
    create = client.post("/api/lobbies/new/", headers={"Authorization": token},
                         json={"name": "test_lobby", "max_players": 5})

    lobby_id = 50000
    join = client.post(
        "/api/lobbies/" +
        str(lobby_id) +
        "/join/",
        headers={
            "Authorization": token})

    assert join.status_code == 404
