from fastapi.testclient import TestClient

from app.database.crud import *
from app.test import test_svapi

testc = TestClient(test_svapi)


spell_database("Divination")


# This function tests if the game is able to respond to a divination request
def test_get_divination():
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
    assert response.json() == [{"card_pos": 0, "phoenix": True}, {
        "card_pos": 1, "phoenix": False}, {"card_pos": 4, "phoenix": False}]
