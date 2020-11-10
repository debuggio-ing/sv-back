from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.test import test_svapi
from app.database.crud import *

# It's necessary to remove database before running the tests.
testc = TestClient(test_svapi)


# Setup database
user1 = UserReg(
    username='user1',
    email='1@gmail.com',
    password='testPassword')
if user1.email not in get_emails():
    register_user(user1)


def test_verify_email():
    assert not get_is_email_verified(user_email=user1.email)

    response = testc.post(
        "/api/verify/?input_code=100000&user_email=" + user1.email)

    assert response.status_code == 200
    assert get_is_email_verified(user_email=user1.email)
    assert response.json() == {"email": user1.email, "verified": True}
