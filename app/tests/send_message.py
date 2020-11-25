from fastapi.testclient import TestClient

from app.debug.test_suite import *
from app.test import test_svapi

testc = TestClient(test_svapi)


NUM_OF_PLAYERS = 5


users = []
for x in range(NUM_OF_PLAYERS):
    user = User(nickname="user" + str(x), email=str(x) + '@gmail.com',
                password="123456789")
    register_user(user=user)
    login(user=user)

    users.append(user)


new_lobby = create_new_lobby(name="lobby_test", max_players=5, user=users[0])

lobby_id = new_lobby.json()["id"]
for x in range(1, len(users)):
    join_lobby(lobby_id=lobby_id, user=users[x])

# Send a message to a valid game.


def test_send_message():
    message = "holaa"

    send_msg = send_message(game_id=lobby_id, user=users[0], message=message)

    result = send_msg.json()

    assert send_msg.status_code == 200
    assert result['msg'] == message


# Send a message to a INvalid game.
def test_send_message_invalid_game():
    message = "holaa"

    send_msg = send_message(game_id=789, user=users[0], message=message)

    result = send_msg.json()
    assert send_msg.status_code == 409


# Send a message with no user.
def test_send_message_no_user():
    message = "holaa"

    send_msg = testc.post(
        "api/games/" +
        str(lobby_id) +
        "/chat/send/?msg=" + message,
        json={"msg": message})

    result = send_msg.json()
    assert send_msg.status_code == 401
