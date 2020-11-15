from fastapi.testclient import TestClient

from app.debug.spell_database import *
from app.test import test_svapi

testc = TestClient(test_svapi)


spell_database("Avada Kedavra")


# This function tests if the game is able to respond to a kadavra request
def test_get_kadavra():
    login = testc.post(
        "api/login/",
        headers={"Content-Type": "application/json"},
        json={"email": "maw@gmail.com", "password": "password"})

    token = "Bearer " + login.json()["access_token"]

    response = testc.get(
        "/api/games/1/spell/",
        headers={
            "Authorization": token})

    assert response.status_code == 200
    assert response.json() == 1


def test_post_kadavra():
    login = testc.post(
        "api/login/",
        headers={"Content-Type": "application/json"},
        json={"email": "maw@gmail.com", "password": "password"})

    token = "Bearer " + login.json()["access_token"]

    response = testc.post(
        "/api/games/1/spell/",
        headers={
            "Authorization": token},
        json={"target": 2})

    assert response.status_code == 200
    assert response.json() == 1

    game_state = testc.get("api/games/1", headers={"Authorization": token})

    start_json = game_state.json()
    player_list = start_json['player_list']

    assert False == player_list[1]['alive']

    # DEBERIA TESTEAR QUE LOS MUERTOS NO PUEDEN SER NADA
