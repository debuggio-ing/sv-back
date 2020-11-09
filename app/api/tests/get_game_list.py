from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.test import test_svapi
from app.database.crud import *

# It's necessary to remove database before running the tests.


testc = TestClient(test_svapi)


populate_test_db()

#DEPRECADO, YA NO HACE LO MISMO QUE ANTES
"""
def test_get_game_list():

    login = testc.post(
        "api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": "law@gmail.com",
            "password": "password"})

    token = "Bearer " + login.json()["access_token"]

    game = testc.get("/api/games/", headers={"Authorization": token})

    # Esto es super mejorable
    game_json = game.json()
    game1 = game_json[0]
    game2 = game_json[1]

    assert len(game1['player_list']) == 5
    assert game1['player_list'][0] == {"player_id": 1, "alive": True,
                                       "last_vote": True, "voted": True,
                                       "username": "maw", "position": 1,
                                       "role": "voldemort"}
    assert game1['player_list'][1] == {"player_id": 2, "alive": True,
                                       "last_vote": True, "voted": False,
                                       "username": "law", "position": 2,
                                       "role": 'Death Eater'}
    assert game1['player_list'][2] == {"player_id": 3, "alive": True,
                                       "last_vote": True, "voted": True,
                                       "username": "lau", "position": 3,
                                       "role": 'Order of the Phoenix'}
    assert game1['player_list'][3] == {"player_id": 4, "alive": True,
                                       "last_vote": True, "voted": True,
                                       "username": "ulince", "position": 4,
                                       "role": 'Order of the Phoenix'}
    assert game1['player_list'][4] == {"player_id": 5, "alive": True,
                                       "last_vote": True, "voted": False,
                                       "username": "nico", "position": 5,
                                       "role": 'Order of the Phoenix'}
    assert game1['voting']
    assert game1['in_session'] == False
    assert game1['minister_proclaimed'] == False
    assert game1['minister'] == 1
    assert game1['prev_minister'] == 3
    assert game1['director'] == 2
    assert game1['prev_director'] == 4
    assert game1['semaphore'] == 0
    assert game1['score'] == {"good": 0, "bad": 0}
    assert game1['end'] is None
    assert game1['winners'] is None
    assert game1['roleReveal'] is None
    assert game1['client_minister'] == False
    assert game1['client_director']

    assert len(game2['player_list']) == 5
    assert game2['player_list'][0] == {"player_id": 6, "alive": True,
                                       "last_vote": True, "voted": True,
                                       "username": "maw", "position": 1,
                                       "role": 'voldemort'}
    assert game2['player_list'][1] == {"player_id": 7, "alive": True,
                                       "last_vote": True, "voted": False,
                                       "username": "law", "position": 2,
                                       "role": 'Death Eater'}
    assert game2['player_list'][2] == {"player_id": 8, "alive": True,
                                       "last_vote": True, "voted": True,
                                       "username": "lau", "position": 3,
                                       "role": 'Order of the Phoenix'}
    assert game2['player_list'][3] == {"player_id": 9, "alive": True,
                                       "last_vote": True, "voted": True,
                                       "username": "ulince", "position": 4,
                                       "role": 'Order of the Phoenix'}
    assert game2['player_list'][4] == {"player_id": 10, "alive": True,
                                       "last_vote": True, "voted": False,
                                       "username": "nico", "position": 5,
                                       "role": 'Order of the Phoenix'}
    assert game2['voting'] == False
    assert game2['in_session'] == False
    assert game2['minister_proclaimed'] == False
    assert game2['minister'] == 6
    assert game2['prev_minister'] == 8
    assert game2['director'] == -1
    assert game2['prev_director'] == 9
    assert game2['semaphore'] == 0
    assert game2['score'] == {"good": 0, "bad": 0}
    assert game2['end'] is None
    assert game2['winners'] is None
    assert game2['roleReveal'] is None
    assert game2['client_minister'] == False
    assert game2['client_director'] == False
"""
