from fastapi.testclient import TestClient

from app.debug.populate_database import *
from app.debug.set_db_to_proclaim import *
from app.debug.spell_database import *
from app.test import test_svapi

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
        "nickname": "law",
                    "email": "law@gmail.com",
    }
