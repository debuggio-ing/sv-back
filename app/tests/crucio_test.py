from app.debug.spell_database import *
from app.debug.test_suite import *

spell_database("Crucio")


users = [
    User(
        nickname="maw",
        email="maw@gmail.com",
        password="password")
]

for u in users:
    login(user=u)


def test_get_crucio():
    response = get_spell(game_id=1, user=users[0])
    assert response.status_code == 200
    assert response.json()['spell_type'] == 'Crucio'


def test_post_crucio():
    response = post_spell(game_id=1, user=users[0], target=2)
    assert response.status_code == 200

    response = get_spell(game_id=1, user=users[0])
    assert response.status_code == 200
    assert response.json()['spell_type'] == 'Crucio'
    assert response.json()['role'] == 'Death Eater'

    response = post_spell(game_id=1, user=users[0], target=-1)
    assert response.status_code == 200

    response = get_spell(game_id=1, user=users[0])
    assert response.status_code == 409
