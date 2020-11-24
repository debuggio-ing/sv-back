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


# Try to get a lobby
def test_get_lobby():
    get_lobby = lobby.get(
        "api/lobbies/{}/".format(lobby1_id),
        headers={"Authorization": token1})

    join_json = join.json()
    get_lobby_json = get_lobby.json()

    assert get_lobby.status_code == 200
    assert get_lobby_json['current_players'] == join_json["current_players"]
    assert get_lobby_json['id'] == lobby1_id
    assert get_lobby_json['max_players'] == join_json["max_players"]
    assert get_lobby_json['name'] == join_json["name"]
    assert get_lobby_json['started'] == join_json["started"]
    assert get_lobby_json['finished'] == join_json["finished"]
    assert get_lobby_json['is_owner']


# Try to get a lobby not being logged in
def test_get_lobby_not_logged_in():
    get_lobby = lobby.get("api/lobbies/{}/".format(lobby1_id))

    assert get_lobby.status_code == 401
    assert get_lobby.json() == {'detail': 'Missing Authorization Header'}


# Try to get inexistent lobby (needs the testing database to not have the
# lobby_id == 9999)
def test_get_inexistent_lobby():
    get_lobby = lobby.get(
        "api/lobbies/{}/".format(9999),
        headers={"Authorization": token1}
    )

    assert get_lobby.status_code == 404
    assert get_lobby.json() == {'detail': 'Lobby not found.'}
