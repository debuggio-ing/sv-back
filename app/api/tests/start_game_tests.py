from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.test import test_svapi
from app.database.crud import *


testc = TestClient(test_svapi)


def test_start_game():
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

    create_lobby = testc.post("/api/lobbies/new/",
        headers={"Authorization": tokens[0]},
        json={"name": "lobby_test", "max_players": 7})
    lobby_id = create_lobby.json()["id"]

    for x in range(1, len(tokens)):
        join = testc.post(
            "/api/lobbies/" +
            str(lobby_id) +
            "/join/",
            headers={
                "Authorization": tokens[x]})

    start = testc.post("api/lobbies/" + str(lobby_id) + "/start/",
        headers={"Authorization": tokens[0]})

    start_json = start.json()
    player_list = start_json['player_list']

    num_voldemort = num_phoenixes = num_death_eaters = 0

    for player in player_list:
        (v, p) = get_player_id_role(player['player_id'])

        if v:
            num_voldemort += 1

        if p:
           num_phoenixes += 1
        else:
            num_death_eaters += 1

    assert start.status_code == 200
    assert start_json['director'] == -1
    assert start_json['minister'] == player_list[0]['player_id']
    assert start_json['end'] == None
    assert len(player_list) == NUM_OF_PLAYERS
    assert num_phoenixes == 3
    assert num_death_eaters == 2
    assert num_voldemort == 1
    assert start_json['prev_director'] == -1
    assert start_json['prev_minister'] == -1
    assert start_json['roleReveal'] == None
    assert start_json['score'] == {'bad':0, 'good':0}
    assert start_json['semaphore'] == 0
    assert start_json['winners'] == None


def test_start_game_with_not_enough_players():
    # Setup database
    user1 = UserReg(username='user1', email='1@gmail.com',
        password='testPassword')
    if user1.email not in get_emails():
        register_user(user1)

    login = testc.post("api/login/",
        headers={"Content-Type": "application/json"},
        json={"email": user1.email, "password": user1.password})

    token = "Bearer " + login.json()["access_token"]

    create_lobby = testc.post("/api/lobbies/new/",
        headers={"Authorization": token},
        json={"name": "lobby_test", "max_players": 7})

    lobby_id = create_lobby.json()["id"]
    start = testc.post("api/lobbies/" + str(lobby_id) + "/start/",
        headers={"Authorization": token})

    assert start.status_code == 412
    assert start.json() == {'detail': 'Not enough users in the lobby.'}