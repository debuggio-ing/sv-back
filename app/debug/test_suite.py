from fastapi.testclient import TestClient
from fastapi import status
from app.test import test_svapi

test_client = TestClient(test_svapi)

"""
This testing suite has been made to create situations in games.
It's not meant to be used for testing of error codes.
"""


class User:
    def __init__(
            self,
            nickname: str,
            email: str,
            password: str,
            token: str = ""):
        self.nickname = nickname
        self.email = email
        self.password = password
        self.token = token


# Creates a new user in the database, raises error on failure
def register_user(user: User):
    response = test_client.post(
        "api/register/",
        headers={
            "Content-Type": "application/json"},
        json={
            "nickname": user.nickname,
            "email": user.email,
            "password": user.password})
    assert response.status_code == status.HTTP_201_CREATED


# Updates the token of the user
def login(user: User):
    response = test_client.post(
        "api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": user.email,
            "password": user.password})
    assert response.status_code == status.HTTP_200_OK
    # tokens
    user.token = "Bearer " + response.json()["access_token"]
    return


# Requires that the user object is logged in
# Returns LobbyPublic with the data of lobby identified by lobby_id
def get_lobby_info(lobby_id: int, user: User):
    response = test_client.get(
        "api/lobbies/{}".format(lobby_id),
        headers={
            "Authorization": user.token})
    return response


# Requires that the user is logged in
# Returns [LobbyPublic]
def get_lobbies(user: User):
    response = test_client.post(
        "api/lobbies/",
        headers={
            "Content-Type": "application/json",
            "Authorization": user.token},
        json={
            "available": True,
            "started": False,
            "finished": False,
            "user_games": False,
            "all_games": True})

    return response


# Requires that the user object is logged in
# Creates a new lobby in the database and returns the LobbyPublic of that lobby
def create_new_lobby(name: str, max_players: int, user: User):
    response = test_client.post(
        "api/lobbies/new/",
        headers={
            "Content-Type": "application/json",
            "Authorization": user.token},
        json={
            "name": name,
            "max_players": max_players})
    return response


# Requires that the user object is logged in
# Joins the lobby identified by lobby_id and returns its LobbyPublic
def join_lobby(lobby_id: int, user: User):
    response = test_client.post(
        "api/lobbies/{}/join/".format(lobby_id),
        headers={
            "Authorization": user.token})
    return response


# Requires that the user object is logged in
# Starts the match and returns its game_id
# should it be lobby_id instead?
def start_match(lobby_id: int, user: User):
    response = test_client.post("api/lobbies/{}/start/".format(lobby_id),
                                headers={"Authorization": user.token})
    return response


# Requires that the user object is logged in
# Returns a list of all the games stored in the database
def get_all_games(user: User):
    response = test_client.get("api/games/",
                               headers={"Authorization": user.token})
    return response


# Requires that the user object is logged in
# Returns the GamePublic data for the specified user
def get_game_info(game_id: int, user: User):
    response = test_client.get(
        "api/games/{}/".format(game_id),
        headers={
            "Authorization": user.token})
    return response


# Requires that the user is logged in and a player of the match, and the
# match in the middle of an election
def post_vote(game_id: int, vote: bool, user: User):
    response = test_client.post(
        "api/games/{}/vote/".format(game_id),
        headers={
            "Content-Type": "application/json",
            "Authorization": user.token},
        json={
            "vote": vote})
    return response


# Requires that the user is logged in and a player of the game
# It requires that the game and the player are able to handle a `get spell`
def get_spell(game_id: int, user: User):
    response = test_client.get(
        "api/games/{}/spell/".format(game_id),
        headers={
            "Authorization": user.token})
    return response


# Requires that the user is logged in and a player of the game
# It requires that the game and the player are able to handle a `post spell`
def post_spell(game_id: int, user: User, target: int):
    response = test_client.post(
        "api/games/{}/spell/".format(game_id),
        headers={
            "Content-Type": "application/json",
            "Authorization": user.token},
        json={
            "target": target})
    return response


# Requires that the user is logged in and a player of the game
# It requires that the game and the player are able to handle a `get
# proclamation`
def get_proclamation_cards(game_id: int, user: User):
    response = test_client.get(
        "api/games/{}/proc/".format(game_id),
        headers={
            "Authorization": user.token})
    return response


# Requires that the user is logged in and a player of the game
# It requires that the game and the player are able to handle a `get
# proclamation`
def post_proclamation_cards(
        game_id: int,
        election: int,
        expelliarmus: bool,
        user: User):
    response = test_client.post(
        "api/games/{}/proc/".format(game_id),
        headers={
            "Content-Type": "application/json",
            "Authorization": user.token},
        json={
            "election": election,
            "expelliarmus": expelliarmus})
    return response


# Requires that the user is logged in and a player of the game
# It requires that the game and the player are apl to handle a `post new
# director`
def post_new_candidate(game_id: int, candidate_id: int, user: User):
    response = test_client.post(
        "api/games/{}/director/{}/".format(
            game_id, candidate_id), headers={
            "Authorization": user.token})
    return response


# Send a message to game_id.
def send_message(game_id: int, user: User, message: str):
    response = test_client.post(
        "api/games/" +
        str(game_id) +
        "/chat/send/",
        headers={"Authorization": user.token},
        json={"msg": message})
    return response
