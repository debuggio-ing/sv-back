from fastapi.testclient import TestClient

from app.debug.spell_database import *
from app.test import test_svapi
from app.debug.test_suite import *


spell_database("Avada Kedavra")

users = [
    User(
        nickname="maw",
        email="maw@gmail.com",
        password="password")
]
for u in users:
    login(user=u)


# This function tests if the game is able to respond to a kadavra request
def test_get_kadavra():
    response = get_spell(game_id=1, user=users[0])
    assert response.status_code == 200
    assert response.json()['spell_type'] == 'Avada Kedavra'


def test_post_kadavra():
    response = post_spell(game_id=1, user=users[0], target=2)

    assert response.status_code == 200
    assert response.json() == 1

    response = get_game_info(game_id=1, user=users[0])

    assert not response.json()['player_list'][1]['alive']
