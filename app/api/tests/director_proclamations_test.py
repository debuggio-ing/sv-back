from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.test import test_svapi
from app.database.crud import *

testc = TestClient(test_svapi)


set_db_for_procl()

# Possible cases
# 1)Correct player gets proclamation cards
# Correct player posts wrong cards
# Correct player posts correct cards and game doesnt end
# Correct player posts correct cards and game ends
# Incorrect player sends request post / get
# Player sends request to wrong game
# Player sends request in the wrong moment of the game


# Correct player gets proclamation cards
def test_get_cards():
    login = testc.post("api/login/", headers={"Content-Type": "application/json"}, json={
                       "email": "law@gmail.com", "password": "password"})
    token = "Bearer " + login.json()["access_token"]

    response = testc.get(
        "api/games/1/dir/proc/", headers={"Authorization": token})

    assert response.status_code == 200

    cards = response.json()
    assert cards == [{"card_pos": 1, "phoenix": True}, {"card_pos": 2, "phoenix": False}]
