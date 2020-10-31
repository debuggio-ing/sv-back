from typing import Optional, List
from fastapi import APIRouter, HTTPException, Request, Depends, Response, status
from pydantic import BaseModel, EmailStr
from enum import Enum, IntEnum
from fastapi_jwt_auth import AuthJWT

from app.api.schemas import *
from app.database.models import *
from app.database.crud import *


# Lobbies endpoints' router
r = lobbies_router = APIRouter()


# Return lobbies list.
@r.get("/lobbies/", response_model=List[LobbyPublic])
def get_lobby_list(
    lobby_from: Optional[int] = 0,
    lobby_to: Optional[int] = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()

    required_lobbies = get_all_lobbies_ids(lobby_from, lobby_to)
    lobbies = []
    for lid in required_lobbies:
        lobby = LobbyPublic(id=lid, name=get_lobby_name(lid),
                            current_players=get_lobby_player_list(lid),
                            max_players=get_lobby_max_players(lid),
                            started=get_lobby_started(lid))
        lobbies.append(lobby)

    return lobbies


# Return lobby_id lobby information.
@r.get("/lobbies/{lobby_id}/", response_model=LobbyPublic)
def get_lobby(lobby_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    if lobby_exists(lobby_id):
        lobby = LobbyPublic(id=lobby_id, name=get_lobby_name(lobby_id),
                            current_players=get_lobby_player_list(lobby_id),
                            max_players=get_lobby_max_players(lobby_id),
                            started=get_lobby_started(lobby_id))
    else:
        raise HTTPException(
            status_code=204, detail='No content')
    return lobby


# Create new lobby.
@r.post("/lobbies/new/",
        response_model=LobbyPublic,
        status_code=status.HTTP_201_CREATED)
def create_lobby(new_lobby: LobbyReg, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    user_email = Authorize.get_jwt_identity()

    lobby_id = insert_lobby(new_lobby)
    insert_player(user_email=user_email, lobby_id=lobby_id)

    current_players = get_lobby_player_list(lobby_id)
    lobby = LobbyPublic(
        id=lobby_id,
        name=new_lobby.name,
        current_players=current_players,
        max_players=new_lobby.max_players,
        started=get_lobby_started(lobby_id))

    return lobby


# Join lobby_id lobby.
@r.post("/lobbies/{lobby_id}/join/",
        response_model=LobbyPublic)
def join_game(lobby_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    # Get information from jwt_token.
    user_email = Authorize.get_jwt_identity()
    player_id = insert_player(user_email=user_email, lobby_id=lobby_id)

    # If player is already in lobby return exception.
    if player_id == -1:
        raise HTTPException(status_code=409, detail="User already in lobby.")

    current_players = get_lobby_player_list(lobby_id)
    lobby_name = get_lobby_name(lobby_id)
    lobby_max_players = get_lobby_max_players(lobby_id)
    lobby = LobbyPublic(
        id=lobby_id,
        name=lobby_name,
        current_players=current_players,
        max_players=lobby_max_players,
        started=get_lobby_started(lobby_id))

    return lobby


# Start lobby_id lobby.
@r.post("/lobbies/{lobby_id}/start/", 
                response_model=StartConfirmation)
def start_game(
        lobby_id: int,
        # current_players: LobbyStart,
        Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    if is_lobby_started(lobby_id):
        raise HTTPException(status_code=409,
                            detail="Game has already started.")

    users_in_lobby = get_lobby_player_list(lobby_id)
    if len(users_in_lobby) < 5:
        raise HTTPException(status_code=412,
                            detail="Not enough users in the lobby.")
    set_lobby_started(lobby_id)

    game_id = insert_game(lobby_id)

    return StartConfirmation(started=(game_id != -1))
