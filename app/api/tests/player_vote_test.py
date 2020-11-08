
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.test import test_svapi
from app.database.crud import *

testc = TestClient(test_svapi)


populate_test_db()


def test_not_last_vote():

    login = testc.post(
        "api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": "law@gmail.com",
            "password": "password"})

    token = "Bearer " + login.json()["access_token"]
    vote_response = testc.post(
        "/api/games/1/vote/", headers={"Authorization": token}, json={"vote": "false"})

    assert vote_response.status_code == 200


"""
    game = testc.get(
        "api/games/1/",
        headers={"Authorization": token}
    )

    game.json()[]
"""


def test_redo_vote():

    login = testc.post(
        "api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": "law@gmail.com",
            "password": "password"})

    token = "Bearer " + login.json()["access_token"]
    response = testc.post(
        "/api/games/1/vote/", headers={"Authorization": token}, json={"vote": "true"})

    assert response.status_code == 200


def test_last_vote():

    login = testc.post(
        "api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": "nico@gmail.com",
            "password": "password"})

    token = "Bearer " + login.json()["access_token"]
    response = testc.post(
        "/api/games/1/vote/", headers={"Authorization": token}, json={"vote": "false"})

    assert response.status_code == 200
