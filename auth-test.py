from fastapi import FastAPI
from fastapi.testclient import TestClient
from auth import *

client = TestClient(app)


def test_access_protected_endpoint_unlogged():
    response = client.get("/protected")

    assert response.status_code == 401
    assert response.json() == {"detail": "Missing Authorization Header"}


def test_login():
    response = client.post("/login",
                           headers={"Content-Type": "application/json"},
                           json={"username": "test", "password": "test"})

    assert response.status_code == 200
    assert len(response.json()["access_token"]) == 275


def test_access_protected_endpoint_logged():
    login = client.post("/login",
                        headers={"Content-Type": "application/json"},
                        json={"username": "test", "password": "test"})

    token = "Bearer " + login.json()["access_token"]

    response = client.get("/protected",
                          headers={"Authorization": token}, )

    assert response.status_code == 200
    assert response.json() == {"logged_in_as": "test"}
