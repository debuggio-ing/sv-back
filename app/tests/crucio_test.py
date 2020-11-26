from fastapi.testclient import TestClient

from app.debug.spell_database import *
from app.test import test_svapi

testc = TestClient(test_svapi)


from app.debug.test_suite import *
from fastapi import status

crucio_database()

# This function tests if the game is able to respond to a crucio request
def test_get_crucio():
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
    assert response.json() == 3


def test_post_crucio():
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
    assert response.json() == {'role': 'Death Eater'}

    game_state = testc.get("api/games/1", headers={"Authorization": token})

    assert game_state.status_code == 200
    # DEBERIA TESTEAR QUE LOS MUERTOS NO PUEDEN SER NADA
