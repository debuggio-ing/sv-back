from typing import Optional, List
from fastapi import APIRouter, HTTPException, Request, Depends, Response, status
from pydantic import BaseModel, EmailStr
from enum import Enum, IntEnum
from fastapi_jwt_auth import AuthJWT

from app.api.schemas import *
from app.database.models import *
from app.database.crud import *

r = lobbies_router = APIRouter()

# Ver la lista de salas
@r.get("/lobbies/")
def get_lobby_list(
    lobby_from: Optional[int] = 0,
    lobby_to: Optional[int] = None,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return


# Ver la información de mi sala
@r.get("/lobbies/{lobby_id}/", response_model=LobbyPublic)
def get_lobby(lobby_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return


# Crear una nueva sala
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
        max_players=new_lobby.max_players)

    return lobby

# Unirse a una sala
# la información del usuario se obtiene del JWT


@r.post("/lobbies/{lobby_id}/join/", response_model=LobbyPublic
        )
def join_game(lobby_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    user_email = Authorize.get_jwt_identity()
    player_id = insert_player(user_email=user_email, lobby_id=lobby_id)

    if player_id == -1:
        raise HTTPException(status_code=409, detail="User already in lobby.")

    current_players = get_lobby_player_list(lobby_id)
    lobby_name = get_lobby_name(lobby_id)
    lobby_max_players = get_lobby_max_players(lobby_id)
    lobby = LobbyPublic(
        id=lobby_id,
        name=lobby_name,
        current_players=current_players,
        max_players=lobby_max_players)

    return lobby


# Empezar la partida
@r.post("/lobbies/{lobby_id}/start/")
def start_game(
        lobby_id: int,
        current_players: LobbyStart,
        Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return 1
