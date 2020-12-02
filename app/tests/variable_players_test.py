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
        password="password"),
    User(
        nickname="f",
        email="f@z.com",
        password="password"),
    User(
        nickname="g",
        email="g@z.com",
        password="password"),
    User(
        nickname="h",
        email="h@z.com",
        password="password"),
    User(
        nickname="i",
        email="i@z.com",
        password="password"),
    User(
        nickname="j",
        email="j@z.com",
        password="password"),
    User(
        nickname="k",
        email="k@z.com",
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


def test_lobby_sizes():
    for max_players in range(5, 11):
        lobby_create = create_new_lobby(
            name="lobby{}".format(
                max_players - 5),
            max_players=max_players,
            user=users[0])
        check_users_join(
            max_players=max_players,
            lobby_id=lobby_create.json()["id"])
    begin_matches()


def begin_matches():
    response = get_lobbies(user=users[0])
    lobbies = response.json()
    for lobby in lobbies:
        begin_response = start_match(lobby_id=lobby["id"], user=users[0])
        assert begin_response.status_code == status.HTTP_200_OK
