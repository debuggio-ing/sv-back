from fastapi import FastAPI
from fastapi.testclient import TestClient
from ..routes import *


client = TestClient(routes)


# Try to access the protected endpoint without logging in.
def test_access_protected_endpoint_unlogged():
    response = client.get("/protected/")

    assert response.status_code == 401
    assert response.json() == {"detail": "Missing Authorization Header"}


# Try to log in.
def test_login():
    if 'test@gmail.com' not in get_emails():
        user = UserReg(
            username='test',
            email='test@gmail.com',
            password='testPassword')
        register_user(user)

    response = client.post(
        "/users/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": "test@gmail.com",
            "password": "testPassword"})

    assert response.status_code == 200
    assert len(response.json()["access_token"]) == 288


# Try to access the protected endpoint after logging in.
def test_access_protected_endpoint_logged():
    if 'test@gmail.com' not in get_emails():
        user = UserReg(
            username='test',
            email='test@gmail.com',
            password='testPassword')
        register_user(user)

    login = client.post(
        "/users/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": "test@gmail.com",
            "password": "testPassword"})

    token = "Bearer " + login.json()["access_token"]

    response = client.get("/protected/",
                          headers={"Authorization": token}, )

    assert response.status_code == 200
    assert response.json() == {"logged_in_as": "test@gmail.com"}
