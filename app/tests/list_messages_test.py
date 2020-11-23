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

start_match(lobby_id=lobby_id, user=users[0])


# Send a message to a valid game.
def test_send_message():
    message1 = "holaa"
    message2 = "que buen juego"

    game = get_game_info(game_id=lobby_id, user=users[0])
    assert game.json()['messages'] == []

    send_message(game_id=lobby_id, user=users[0], message=message1)

    game = get_game_info(game_id=lobby_id, user=users[0])
    game_json = game.json()
    assert game_json['messages'][0]['sender'] == users[0].nickname
    assert game_json['messages'][0]['message'] == message1

    send_message(game_id=lobby_id, user=users[1], message=message2)

    game = get_game_info(game_id=lobby_id, user=users[1])
    game_json = game.json()
    assert game_json['messages'][0]['sender'] == users[0].nickname
    assert game_json['messages'][0]['message'] == message1
    assert game_json['messages'][1]['sender'] == users[1].nickname
    assert game_json['messages'][1]['message'] == message2
