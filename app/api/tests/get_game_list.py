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
          "username": "maw",
          "position": 1
        },
        {
          "player_id": 2,
          "alive": True,
          "last_vote": True,
          "voted": False,
          "username": "law",
          "position": 2
        },
        {
          "player_id": 3,
          "alive": True,
          "last_vote": True,
          "voted": True,
          "username": "lau",
          
          "position": 3
        },
        {
          "player_id": 4,
          "alive": True,
          "last_vote": True,
          "voted": True,
          "username": "ulince",
          "position": 4
        },
        {
          "player_id": 5,
          "alive": True,
          "last_vote": True,
          "voted": False,
          "username": "nico",
          "position": 5
        }
    ],
    "voting": True,
    "in_session": False,
    "minister_proclaimed": False,
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
  },
    {
    "player_list": [
        {
          "player_id": 6,
          "alive": True,
          "last_vote": True,
          "voted": True,
          "username": "maw",
          "position": 1
        },
        {
          "player_id": 7,
          "alive": True,
          "last_vote": True,
          "voted": False,
          "username": "law",
          "position": 2
        },
        {
          "player_id": 8,
          "alive": True,
          "last_vote": True,
          "voted": True,
          "username": "lau",
          
          "position": 3
        },
        {
          "player_id": 9,
          "alive": True,
          "last_vote": True,
          "voted": True,
          "username": "ulince",
          "position": 4
        },
        {
          "player_id": 10,
          "alive": True,
          "last_vote": True,
          "voted": False,
          "username": "nico",
          "position": 5
        }
    ],
    "voting": False,
    "in_session": False,
    "minister_proclaimed": False,
    "minister": 6,
    "prev_minister": 8,
    "director": -1,
    "prev_director": 9,
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