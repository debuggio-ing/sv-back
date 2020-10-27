from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.test import test_svapi
from app.database.crud import *

# It's necessary to remove database before running the tests.



testc = TestClient(test_svapi)


populate_test_db()

def get_game_public():

    login = testc.post(
        "api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": "law@gmail.com",
            "password": "password"})

    token = "Bearer " + login.json()["access_token"]

    game = testc.get("/api/games/", headers={"Authorization": token})

    assert game.json()["semaphore"] == 0
    assert game.json()["minister"] == 1
    assert game.json()["director"] == 2
    assert game.json()["prev_minister"] == 3
    assert game.json()["prev_director"] == 4
    assert game.json()["player_list"][0]["player_id"] == 1