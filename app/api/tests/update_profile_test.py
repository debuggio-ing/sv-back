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

username1 = "que buen nombre"
password1 = "margaretthatcheris110%SEXY"
username2 = "snowden"
password2 = "nosociallife"


# Modify the user's profile
def test_modify_profile():
    login = testc.post(
        "api/login/",
        headers={"Content-Type": "application/json"},
        json={"email": user1.email, "password": user1.password})

    token = "Bearer " + login.json()["access_token"]

    user = testc.post(
        "/api/users/info/modify/",
        headers={
            "Authorization": token},
        json={
            "username": username1,
            "password": password1})

    user_json = user.json()

    assert user.status_code == 200
    assert user_json['username'] == username1


# Test if the new password works
def test_password_username_change():
    login = testc.post(
        "/api/login/",
        headers={"Content-Type": "application/json"},
        json={"email": user1.email, "password": password1}
    )
    assert login.status_code == 200


# Modify the user's username
def test_modify_username():
    login = testc.post(
        "api/login/",
        headers={"Content-Type": "application/json"},
        json={"email": user1.email, "password": password1})

    token = "Bearer " + login.json()["access_token"]
    user = testc.post(
        "/api/users/info/modify/",
        headers={
            "Authorization": token},
        json={
            "username": username2})

    user_json = user.json()

    assert user.status_code == 200
    assert user_json['username'] == username2


# Modify the user's password
def test_modify_username():
    login = testc.post(
        "api/login/",
        headers={"Content-Type": "application/json"},
        json={"email": user1.email, "password": password1})

    token = "Bearer " + login.json()["access_token"]
    user = testc.post(
        "/api/users/info/modify/",
        headers={
            "Authorization": token},
        json={
            "password": password2})

    assert user.status_code == 200

    # check if the login works
    login1 = testc.post(
        "api/login/",
        headers={"Content-Type": "application/json"},
        json={"email": user1.email, "password": password2})

    assert login1.status_code == 200
