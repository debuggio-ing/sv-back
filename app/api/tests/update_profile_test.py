from fastapi.testclient import TestClient

from app.database.crud import *
from app.test import test_svapi

# It's necessary to remove database before running the tests.
testc = TestClient(test_svapi)

# Setup database
user1 = UserReg(
    nickname='user1',
    email='a@gmail.com',
    password='123456789')
if user1.email not in get_emails():
    register_user(user1)

nickname1 = "que buen nombre"
password1 = "margaretthatcheris110%SEXY"
nickname2 = "snowden"
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
            "nickname": nickname1,
            "password": password1})

    user_json = user.json()

    assert user.status_code == 200
    assert user_json['nickname'] == nickname1


# Test if the new password works
def test_password_nickname_change():
    login = testc.post(
        "/api/login/",
        headers={"Content-Type": "application/json"},
        json={"email": user1.email, "password": password1}
    )
    assert login.status_code == 200


# Modify the user's nickname
def test_modify_nickname():
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
            "nickname": nickname2})

    user_json = user.json()

    assert user.status_code == 200
    assert user_json['nickname'] == nickname2


# Modify the user's password
def test_modify_nickname():
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


# Update user's profile picture
def test_modify_picture():
    login = testc.post(
        "api/login/",
        headers={"Content-Type": "application/json"},
        json={"email": user1.email, "password": password2})
    token = "Bearer " + login.json()["access_token"]
    file_path = ''
    # test request
    # with open(fpath, "wb") as f:
    #     response = client.post("/", files={"file": ("filename", f, "image/jpeg")})

    empty_picture = testc.get(
        "/api/users/picture/",
        headers={
            "Authorization": token})
    assert empty_picture.status_code == 200
    assert empty_picture.content == b''
    for i in [1, 2]:
        with open("app/api/tests/test_pic{}.jpg".format(i), "rb") as image:
            raw_image = image.read()
            # comments are for testing manually, it opens the picture
            # image = Image.open(BytesIO(raw_image)).convert("RGBA")
            # image.show()
            response = testc.post(
                "/api/users/picture/",
                headers={
                    "Authorization": token},
                files={
                    "file": raw_image})
            assert response.status_code == 200

            image = testc.get(
                "/api/users/picture/",
                headers={
                    "Authorization": token})
            assert image.status_code == 200
            assert image.content == raw_image
