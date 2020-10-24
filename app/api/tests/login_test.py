from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import svapi
from app.database.crud import *


client = TestClient(svapi)


# Try to access the protected endpoint without logging in.
def test_access_protected_endpoint_unlogged():
    response = client.get("/api/games/")

    assert response.status_code == 401
    assert response.json() == {"detail": "Missing Authorization Header"}


# Try to log in.
def test_valid_login():
    if 'test@gmail.com' not in get_emails():
        user = UserReg(
            username='test',
            email='test@gmail.com',
            password='testPassword')
        register_user(user)

    response = client.post(
        "api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": "test@gmail.com",
            "password": "testPassword"})

    assert response.status_code == 200
    assert response.json()["access_token"] != None


# Try to log in with invalid user.
def test_invalid_login():
    response = client.post(
        "api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": "invalid_email@gmail.com",
            "password": "invalid_password"})

    assert response.status_code == 401
    assert response.json() == {'detail': 'Bad email or password'}


# Try to access the protected endpoint after logging in.
def test_access_protected_endpoint_logged():
    if 'test@gmail.com' not in get_emails():
        user = UserReg(
            username='test',
            email='test@gmail.com',
            password='testPassword')
        register_user(user)

    login = client.post(
        "api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": "test@gmail.com",
            "password": "testPassword"})

    token = "Bearer " + login.json()["access_token"]

    response = client.get("api/games/",
                          headers={"Authorization": token}, )

    assert response.status_code == 200
