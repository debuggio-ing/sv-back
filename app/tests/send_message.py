from fastapi.testclient import TestClient

from app.debug.populate_database import *
from app.debug.set_db_to_proclaim import *
from app.debug.spell_database import *
from app.test import test_svapi

testc = TestClient(test_svapi)


NUM_OF_PLAYERS = 5

tokens = []
for x in range(NUM_OF_PLAYERS):
    user = UserReg(nickname="user" + str(x), email=str(x) + '@gmail.com',
                   password="123456789")
    if user.email not in get_emails():
        register_user(user)

    login = testc.post("api/login/",
                       headers={"Content-Type": "application/json"},
                       json={"email": user.email, "password": user.password})

    token = "Bearer " + login.json()["access_token"]
    tokens.append(token)

create_lobby = testc.post("/api/lobbies/new/",
                          headers={"Authorization": tokens[0]},
                          json={"name": "lobby_test", "max_players": 5})
lobby_id = create_lobby.json()["id"]
for x in range(1, len(tokens)):
    join = testc.post(
        "/api/lobbies/" + str(lobby_id) + "/join/",
        headers={"Authorization": tokens[x]})
start = testc.post(
    "api/lobbies/" +
    str(lobby_id) +
    "/start/",
    headers={
        "Authorization": tokens[0]})


# Send a message to a valid game.
def test_send_message():
    message = "holaa"

    send_msg = testc.post(
        "api/games/" +
        str(lobby_id) +
        "/chat/send/?msg="+message,
        headers={
            "Authorization": tokens[0],
            "msg": message})

    result = send_msg.json()
    assert result['message_sent'] == "holaa"
    assert send_msg.status_code == 200


# Send a message to a INvalid game.
def test_send_message_invalid_game():
    message = "holaa"

    send_msg = testc.post(
        "api/games/789/chat/send/?msg="+message,
        headers={
            "Authorization": tokens[0],
            "msg": message})

    result = send_msg.json()
    assert send_msg.status_code == 409


# Send a message with no user.
def test_send_message_no_user():
    message = "holaa"

    send_msg = testc.post(
        "api/games/" +
        str(lobby_id) +
        "/chat/send/?msg="+message)

    result = send_msg.json()
    assert send_msg.status_code == 401
