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

create2 = lobby.post(
    "/api/lobbies/new/",
    headers={
        "Authorization": token1},
    json={
        "name": lobby_name,
        "max_players": max_players})


# Try to get all lobbies.
def test_get_lobby_list():
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
    assert get_all.json() == [{"id": lobby1_id,
                                'owner_alias': "user1",

                               "name": join.json()["name"],
                               "current_players":join.json()["current_players"],
                               "max_players":join.json()["max_players"],
                               "started":join.json()["started"],
                               "finished":create2.json()["finished"],
                               "is_owner":True,
                               "messages":[]},
                              {"id": create2.json()["id"],
                              'owner_alias': "user1",
                               "name":create2.json()["name"],
                               "current_players":create2.json()["current_players"],
                               "max_players":create2.json()["max_players"],
                               "started":create2.json()["started"],
                               "finished":create2.json()["finished"],
                               "is_owner":True,
                               "messages":[]}]


# Try to get all lobbies not being logged in.
def test_get_lobbies_not_logged_in():
    get_all = lobby.post(
        "/api/lobbies/",
        json={
            "available": "true",
            "started": "false",
            "finished": "false",
            "user_games": "false",
            "all_games": "true"})

    assert get_all.status_code == 401
    assert get_all.json() == {'detail': 'Missing Authorization Header'}


# Test lobby_from argument.
def test_lobby_from():
    get_all = lobby.post(
        "/api/lobbies/?lobby_from=2",
        json={
            "available": "true",
            "started": "false",
            "finished": "false",
            "user_games": "false",
            "all_games": "true"},
        headers={
            "Authorization": token1})

    assert get_all.status_code == 200
    assert get_all.json() == [{"id": create2.json()["id"],
                                'owner_alias': "user1",
                               "name":create2.json()["name"],
                               "current_players":create2.json()["current_players"],
                               "max_players":create2.json()["max_players"],
                               "started":create2.json()["started"],
                               "finished":create2.json()["finished"],
                               "is_owner":create2.json()["is_owner"],
                               "messages":[]}]


# Test lobby_to argument.
def test_lobby_to():
    get_all = lobby.post(
        "/api/lobbies/?lobby_to=1",
        json={
            "available": "true",
            "started": "false",
            "finished": "false",
            "user_games": "false",
            "all_games": "true"},
        headers={
            "Authorization": token1})

    assert get_all.status_code == 200
    assert get_all.json() == [{"id": lobby1_id,
                                'owner_alias': "user1",
                               "name": join.json()["name"],
                               "current_players":join.json()["current_players"],
                               "max_players":join.json()["max_players"],
                               "started":join.json()["started"],
                               "finished":create2.json()["finished"],
                               "is_owner":True,
                               "messages":[]}]
