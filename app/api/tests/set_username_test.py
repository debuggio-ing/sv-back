from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.test import test_svapi
from app.database.crud import *


# It's necessary to remove database before running the tests.
testc = TestClient(test_svapi)

# Setup database
user1 = UserReg(
    username='user1',
    email='a@gmail.com',
    password='123456789')
if user1.email not in get_emails():
    register_user(user1)


def test_modify_user_info():
    login = testc.post(
        "api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": user1.email,
            "password": user1.password})

    token = "Bearer " + login.json()["access_token"]
    username = "que buen nombre"

    user = testc.post("/api/users/info/modify/?username=" + username,
                      headers={"Authorization": token})

    user_json = user.json()

    assert user.status_code == 200
    assert user_json['username'] == username
