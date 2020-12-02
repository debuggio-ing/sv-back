from fastapi.testclient import TestClient
from app.debug.spell_database import *
from app.debug.test_suite import *

spell_database("Imperio")
users = [
    User(
        nickname="maw",
        email="maw@gmail.com",
        password="password"),
    User(
        email="maw2@gmail.com",
        nickname="maw2",
        password="password")]
for u in users:
    response = login(user=u)


def test_get_imperio():
    response = get_spell(game_id=1, user=users[0])
    assert response.status_code == 200
    assert response.json()['spell_type'] == 'Imperio'
    response = get_game_info(game_id=1, user=users[0])
    assert response.status_code == 200


def test_post_imperio():
    # check that the minister can't select himself as minister again
    response = post_spell(game_id=1, user=users[0], target=1)
    assert response.status_code == 409

    # check that the minister can select another player as minister
    response = post_spell(game_id=1, user=users[0], target=6)
    assert response.status_code == 200

    # check that the game has the selected player as minister
    response = get_game_info(game_id=1, user=users[1])
    response.status_code == 200
    assert response.json()['client_minister']

    # check that the former minister is no longer minister
    response = get_game_info(game_id=1, user=users[0])
    response.status_code == 200
    assert not response.json()['client_minister']
