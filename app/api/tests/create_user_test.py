import random
import string

from fastapi.testclient import TestClient

from app.test import test_svapi

client = TestClient(test_svapi)


def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


# Creamos un usuario nuevo
def test_create_user():

    rstr = get_random_string(8)
    register = client.post(
        "api/register/",
        headers={
            "Content-Type": "application/json"},
        json={
            "nickname": "miguel{}".format(rstr),
            "email": "{}@gmail.com".format(rstr),
            "password": "messirve"})
    assert register.status_code == 201

    # Intentamos loguearnos luego
    response = client.post(
        "api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": "{}@gmail.com".format(rstr),
            "password": "messirve"})

    assert response.status_code == 200
    assert response.json()["access_token"] is not None


# Intentamos registrar un mismo mail 2 veces
def test_duplicate_user():

    reg1 = client.post(
        "api/register/",
        headers={
            "Content-Type": "application/json"},
        json={
            "nickname": "miguel",
            "email": "miguelmasa@gmail.com",
            "password": "messirve"})

    reg2 = client.post(
        "api/register/",
        headers={
            "Content-Type": "application/json"},
        json={
            "nickname": "miguel",
            "email": "miguelmasa@gmail.com",
            "password": "messirve"})

    assert reg2.status_code == 409
