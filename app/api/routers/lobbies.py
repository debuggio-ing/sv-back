from typing import Optional, List
from fastapi import APIRouter, HTTPException, Request, Depends, Response, status
from pydantic import BaseModel, EmailStr
from enum import Enum, IntEnum
from fastapi_jwt_auth import AuthJWT

from app.api.schemas import *
from app.database.models import *
from app.database.crud import *
from typing import Optional
from app.api.routers_helpers.auth_helper import *

# Lobbies endpoints' router
r = lobbies_router = APIRouter()


# Return lobbies list.
@r.post("/lobbies/", response_model=List[LobbyPublic])
def get_lobby_list(
    filterForm: LobbyFilter,
    lobby_from: Optional[int] = 0,
    lobby_to: Optional[int] = None,
    auth: AuthJWT = Depends()
):
    user_email = validate_user(auth=auth)

    # get all lobbies which haven't started
    lobby_id_list = get_all_lobbies_ids(
        lobby_from=lobby_from,
        lobby_to=lobby_to,
        available=filterForm.available,
        user_games=filterForm.user_games,
        started=filterForm.started,
        finished=filterForm.finished,
        all_games=filterForm.all_games,
        user_email=user_email)


    lobbies = []
    for lobby_id in lobby_id_list:
        lobby = get_lobby_public_info(lobby_id=lobby_id, user_email=user_email)
        lobbies.append(lobby)

    return lobbies


# Return lobby_id lobby information.
@r.get("/lobbies/{lobby_id}/", response_model=LobbyPublic)
def get_lobby(lobby_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    user_email = Authorize.get_jwt_identity()

    if lobby_exists(lobby_id):
        lobby = get_lobby_public_info(lobby_id=lobby_id, user_email=user_email)
    else:
        raise HTTPException(
            status_code=404, detail='Lobby not found.')
    return lobby


# Create new lobby.
@r.post("/lobbies/new/",
        response_model=LobbyPublic,
        status_code=status.HTTP_201_CREATED)
def create_lobby(new_lobby: LobbyReg, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    user_email = Authorize.get_jwt_identity()

    lobby_id = insert_lobby(lobby=new_lobby, user_email=user_email)
    insert_player(user_email=user_email, lobby_id=lobby_id)

    current_players = get_lobby_player_list(lobby_id=lobby_id)
    lobby = LobbyPublic(
        id=lobby_id,
        name=new_lobby.name,
        current_players=current_players,
        max_players=new_lobby.max_players,
        started=get_lobby_started(lobby_id=lobby_id),
        finished=get_lobby_finished(lobby_id=lobby_id),
        is_owner=get_lobby_is_owner(lobby_id=lobby_id, user_email=user_email))

    return lobby


# Join lobby_id lobby.
@r.post("/lobbies/{lobby_id}/join/",
        response_model=LobbyPublic)
def join_game(lobby_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    if not lobby_exists(lobby_id):
        raise HTTPException(status_code=404,
                            detail="The game id is incorrect.") 
    # Get information from jwt_token.
    user_email = Authorize.get_jwt_identity()
    insert_player(user_email=user_email, lobby_id=lobby_id)

    current_players = get_lobby_player_list(lobby_id=lobby_id)
    lobby_name = get_lobby_name(lobby_id=lobby_id)
    lobby_max_players = get_lobby_max_players(lobby_id=lobby_id)
    lobby = LobbyPublic(
        id=lobby_id,
        name=lobby_name,
        current_players=current_players,
        max_players=lobby_max_players,
        started=get_lobby_started(lobby_id=lobby_id),
        finished=get_lobby_finished(lobby_id=lobby_id),
        is_owner=get_lobby_is_owner(lobby_id=lobby_id, user_email=user_email))

    return lobby


# Start lobby_id lobby.
@r.post("/lobbies/{lobby_id}/start/",
        response_model=StartConfirmation)
def start_game(lobby_id: int,
               # current_players: LobbyStart,
               Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    user_email = Authorize.get_jwt_identity()

    if not get_lobby_is_owner(lobby_id=lobby_id, user_email=user_email):
        raise HTTPException(status_code=409,
                            detail="User is not game's owner.")

    if is_lobby_started(lobby_id):
        raise HTTPException(status_code=409,
                            detail="Game has already started.")

    users_in_lobby = get_lobby_player_list(lobby_id=lobby_id)
    if len(users_in_lobby) < 5:
        raise HTTPException(status_code=412,
                            detail="Not enough users in the lobby.")
    set_lobby_started(lobby_id=lobby_id)

    game_id = insert_game(lobby_id=lobby_id)

    return StartConfirmation(game_id=game_id)
