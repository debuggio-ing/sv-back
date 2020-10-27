from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.test import test_svapi
from app.database.crud import *

# It's necessary to remove database before running the tests.



testc = TestClient(test_svapi)


populate_test_db()

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


    #Esto es super mejorable
    assert game.json() == [
  {
    "player_list": [
      {
        "player_id": 1,
        "alive": True,
        "last_vote": True,
        "voted": True,
        "username": "maw"
      },
      {
        "player_id": 2,
        "alive": True,
        "last_vote": True,
        "voted": True,#False,
        "username": "law"
      },
      {
        "player_id": 3,
        "alive": True,
        "last_vote": True,
        "voted": True,
        "username": "lau"
      },
      {
        "player_id": 4,
        "alive": True,
        "last_vote": True,
        "voted": True,
        "username": "ulince"
      },
      {
        "player_id": 5,
        "alive": True,
        "last_vote": True,
        "voted": True,#False,
        "username": "nico"
      }
    ],
    "minister": 1,
    "prev_minister": 3,
    "director": 2,
    "prev_director": 4,
    "semaphore": 0,
    "score": {
      "good": 0,
      "bad": 0
    },
    "end": None,
    "winners": None,
    "roleReveal": None
  }
]