from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.test import test_svapi
from app.database.crud import *


# It's necessary to remove database before running the tests.
testc = TestClient(test_svapi)


populate_test_db()


def test_get_user_info():
    login = testc.post(
        "api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": "law@gmail.com",
            "password": "password"})

    token = "Bearer " + login.json()["access_token"]

    user = testc.get("/api/users/info/", headers={"Authorization": token})

    assert user.status_code == 200

    assert user.json() == {
        "id": 2,
        "username": "law",
                    "email": "law@gmail.com",
    }
