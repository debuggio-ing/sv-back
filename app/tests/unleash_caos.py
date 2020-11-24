from fastapi.testclient import TestClient

from app.debug.caos_db import *
from app.debug.populate_database import *
from app.debug.set_db_to_proclaim import *
from app.debug.spell_database import *
from app.test import test_svapi

testc = TestClient(test_svapi)


caos_db()


@db_session
def test_caos():
    proclaimed_cards = list(
        select(
            card.position for card in ProcCard if card.proclaimed and card.game.lobby.id == 1))

    login = testc.post(
        "api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": "nico@gmail.com",
            "password": "password"})

    token = "Bearer " + login.json()["access_token"]
    response = testc.post(
        "/api/games/1/vote/",
        headers={
            "Authorization": token},
        json={
            "vote": "false"})

    proclaimed_cards_after = list(select(
        card.position for card in ProcCard if card.proclaimed and card.game.lobby.id == 1))

    assert response.status_code == 200
    assert len(proclaimed_cards) == len(proclaimed_cards_after) - 1
