from app.debug.expelliarmus_db import *
from app.debug.test_suite import *

users = [
        User(
            nickname="maw",
            email="maw@gmail.com",
            password="password"
        ),
        User(
            email="law@gmail.com",
            nickname="law",
            password="password",
            ),
        User(
            email="lau@gmail.com",
            nickname="lau",
            password="password"
        ),
        User(
            email="ulince@gmail.com",
            nickname="ulince",
            password="password",
           ),
        User(
            email="nico@gmail.com",
            nickname="nico",
            password="password"
        )]


def test_expelliarmus_ok():
    expelliarmus_db()
    for u in users:
        login(u)

    # check that minister can discard one card
    response = post_proclamation_cards(game_id=1, election=6, expelliarmus=False, user=users[0])
    assert response.status_code == 200

    # check that the game is expecting the director to proclaim
    response = get_game_info(game_id=1, user=users[0])
    assert response.status_code == 200
    assert response.json()["minister_proclaimed"] and response.json()["in_session"]

    # check that the minister can't ask for expelliarmus
    response = post_proclamation_cards(game_id=1, election=19999, expelliarmus=True, user=users[0])
    assert response.status_code == 401

    # check that the director can ask for expelliarmus
    response = post_proclamation_cards(game_id=1, election=19999, expelliarmus=True, user=users[1])
    assert response.status_code == 200

    # check that the minister can't discard one more card
    response = post_proclamation_cards(game_id=1, election=7, expelliarmus=False, user=users[0])
    assert response.status_code == 401

    # check that the game is in expelliarmus
    response = get_game_info(game_id=1, user=users[0])
    assert response.json()["expelliarmus"] and not response.json()["minister_proclaimed"]

    # # check that the director can't cast expelliarmus
    response = post_proclamation_cards(game_id=1, election=19999, expelliarmus=True, user=users[1])
    assert response.status_code == 401

    # check that the minister can cast expelliarmus
    response = post_proclamation_cards(game_id=1, election=19999, expelliarmus=True, user=users[0])
    assert response.status_code == 200

    # check that the game left the legislative session
    response = get_game_info(game_id=1, user=users[0])
    assert response.status_code == 200
    assert not (response.json()["expelliarmus"] or response.json()["in_session"] or response.json()["minister_proclaimed"] or response.json()["director_proclaimed"])
    assert response.json()["score"]["bad"] == 5 and response.json()["score"]["good"] == 0 and response.json()["semaphore"] == 1


