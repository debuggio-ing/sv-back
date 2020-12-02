from fastapi.testclient import TestClient

from app.debug.populate_database import *
from app.debug.set_db_to_proclaim import *
from app.debug.spell_database import *
from app.test import test_svapi


# It's necessary to remove database before running the tests.
testc = TestClient(test_svapi)


populate_test_db()


def test_get_game_public():

    login = testc.post(
        "api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": "law@gmail.com",
            "password": "password"})

    token = "Bearer " + login.json()["access_token"]

    game = testc.get("/api/games/1/", headers={"Authorization": token})

    jgame = game.json()

    assert ("player_list" in jgame and "score" in jgame)
    assert "role" in jgame["player_list"][0]
    assert len(jgame["player_list"]) >= 5
    assert jgame["score"]["good"] == 0 and jgame["score"]["bad"] == 0
    assert any(jgame["minister"] == player["player_id"]
               for player in jgame["player_list"])
    if any(None is not player["role"] for player in jgame["player_list"]):
        # Are roles random? If not this if will always be entered or always not
        # entered
        assert any("Order of the Phoenix" ==
                   player["role"] for player in jgame["player_list"])
        assert any("Voldemort" == player["role"]
                   for player in jgame["player_list"])
        assert any("Death Eater" == player["role"]
                   for player in jgame["player_list"])
