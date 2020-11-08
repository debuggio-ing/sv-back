from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.test import test_svapi
from app.database.crud import *

test_client = TestClient(test_svapi)


db_to_proclaim()

# Possible cases
# 1)Correct player gets proclamation cards
# Correct player posts wrong cards
# Correct player posts correct cards and game doesnt end
# Correct player posts correct cards and game ends
# Incorrect player sends request post / get
# Player sends request to wrong game
# Player sends request in the wrong moment of the game


# Minister gets proclamation cards
def test_min_get_cards():
    login = test_client.post(
        "api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": "maw@gmail.com",
            "password": "password"})
    token = "Bearer " + login.json()["access_token"]

    response = test_client.get(
        "api/games/1/proc/", headers={"Authorization": token})

    assert response.status_code == 200

    cards = response.json()
    assert cards == [{"card_pos": 0, "phoenix": True},
                     {"card_pos": 1, "phoenix": True},
                     {"card_pos": 2, "phoenix": False}]


# Minister discards specified card
def test_min_discard():
    login = test_client.post(
        "api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": "maw@gmail.com",
            "password": "password"})
    token = "Bearer " + login.json()["access_token"]

    discard_response = test_client.post(
        "api/games/1/proc/?election=2",
        headers={
            "Authorization": token,
            "Content-Type": "application/json"})

    assert discard_response.status_code == 200

    game_over = discard_response.json()
    assert not game_over


# Director gets proclamation cards
def test_dir_get_cards():
    login = test_client.post(
        "api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": "law@gmail.com",
            "password": "password"})
    token = "Bearer " + login.json()["access_token"]

    response = test_client.get(
        "api/games/1/proc/",
        headers={
            "Authorization": token})

    assert response.status_code == 200

    cards = response.json()

    assert cards == [{"card_pos": 0, "phoenix": True},
                     {"card_pos": 1, "phoenix": True}]


# Director proclaims card
def test_dir_proclaim():
    login = test_client.post(
        "api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": "law@gmail.com",
            "password": "password"})
    token = "Bearer " + login.json()["access_token"]

    response = test_client.post(
        "api/games/1/proc/?election=1",
        headers={
            "Authorization": token})

    assert response.status_code == 200

    game_over = response.json()

    assert not game_over
