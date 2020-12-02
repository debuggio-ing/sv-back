from fastapi.testclient import TestClient

from app.debug.populate_database import *
from app.debug.set_db_to_proclaim import *
from app.debug.spell_database import *
from app.debug.test_suite import *
from app.test import test_svapi

users = [
    User(
        nickname="maw",
        email="maw@gmail.com",
        password="password")
]

spell_database("Divination")
for u in users:
    login(user=u)


# This function tests if the game is able to respond to a divination request
def test_get_divination():
    response = get_spell(game_id=1, user=users[0])

    assert response.status_code == 200
    assert response.json()['spell_type'] == 'Divination'
    assert response.json()['cards'] == [{"card_pos": 0, "phoenix": True}, {
        "card_pos": 1, "phoenix": False}, {"card_pos": 4, "phoenix": False}]


def test_post_divination():
    response = post_spell(game_id=1, user=users[0], target=-1)
    assert response.status_code == 200
