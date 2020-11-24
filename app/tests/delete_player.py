
#El usuario esta en el juego y es owner
#El usuario esta en el juego y no es owner
#El usuario no esta en el juego 
#El juego ya comenzó
#El lobby es incorrecto
#El player es incorrecto
from app.debug.test_suite import *
from fastapi import status

users = [
    User(
        nickname="a",
        email="a@z.com",
        password="password"),
    User(
        nickname="b",
        email="b@z.com",
        password="password"),
    User(
        nickname="c",
        email="c@z.com",
        password="password"),
    User(
        nickname="d",
        email="d@z.com",
        password="password"),
    User(
        nickname="e",
        email="e@z.com",
        password="password")]

# NEEDS TO BE EXTENDED WITH TESTING FLAG SO THAT THINGS DON'T HAPPEN BY
# RANDOM CHANCE, eg, Proclamation cards order
# So far it works

for user in users:
    register_user(user=user)
    login(user=user)


def check_users_join(lobby_id: int, max_players: int):
    for i in range(len(users)):
        lobby_join = join_lobby(lobby_id=lobby_id, user=users[i])
        if i <= max_players - 1:
            assert lobby_join.status_code == status.HTTP_200_OK
        else:
            assert lobby_join.status_code == status.HTTP_409_CONFLICT


def test_leave_lobby():
    
    lobby_create = create_new_lobby(
        name="asd",
        max_players=5,
        user=users[4])
    lid = lobby_create.json()["id"]
    check_users_join(
        max_players=5,
        lobby_id=lid)
    deplete_match(lid)


def deplete_match(lid):
    for i in range(len(users)):
        leave_join = leave_match(lobby_id=lid, user=users[i])
        response = get_lobby_info(lid, users[i], user_id=users[i].uid)
        if i < 4:
            assert len(response.json()['current_players']) == response.json()['max_players'] -i-1

    response = get_lobbies(users[4])
    assert response.json() == []

