
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import svapi
from app.database.crud import *

game = TestClient(svapi)

populate_test_db()


def test_redo_vote():


    login = game.post(
        "api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": "law@gmail.com",
            "password": "password"})

    token = "Bearer " + login.json()["access_token"]
    response = game.post("/api/games/1/vote/", headers={"Authorization": token}, json={"vote":"false"})

    assert response.status_code == 200

def test_last_vote():


    login = game.post(
        "api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": "nico@gmail.com",
            "password": "password"})

    token = "Bearer " + login.json()["access_token"]
    response = game.post("/api/games/1/vote/", headers={"Authorization": token}, json={"vote":"false"})

    assert response.status_code == 200

    #delete_db()