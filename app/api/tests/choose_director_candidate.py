from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.test import test_svapi
from app.database.crud import *

testc = TestClient(test_svapi)


populate_test_db()

# Posibles casos:
# El jugador incorrecto manda el request
# Elige correctamente
# Se elije a si mismo
# Elije alguien invalido (en otra sprint)
# No es momento de elegir (hay q testear flipeando los booleanos del
# estado de juego)


# el correcto elige un correcto
def test_choose_candidate():
    login = testc.post(
        "api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": "maw@gmail.com",
            "password": "password"})

    token = "Bearer " + login.json()["access_token"]
    vote_response = testc.post("/api/games/2/director/10/",
                               headers={"Authorization": token},
                               json={"vote": "false"})

    assert vote_response.status_code == 200

    game_state = testc.get("api/games/2", headers={"Authorization": token})

    start_json = game_state.json()
    player_list = start_json['player_list']

    assert start_json['director'] == player_list[4]['player_id']


"""
    game = testc.get(
        "api/games/1/",
        headers={"Authorization": token}
    )

    game.json()[]
"""
