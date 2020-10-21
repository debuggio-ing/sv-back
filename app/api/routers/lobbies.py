from typing import Optional, List
from fastapi import APIRouter, HTTPException, Request, Depends, Response, status
from pydantic import BaseModel, EmailStr
from enum import Enum, IntEnum
from fastapi_jwt_auth import AuthJWT

from api.schemas import *
from database.models import *
from database.crud import *

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
def create_lobby(new_lobby: LobbyReg, Authorize: AuthJWT = Depends()) -> int:
    Authorize.jwt_required()
    return 1

# Unirse a una sala
# la información del usuario se obtiene del JWT


@r.post("/lobbies/{lobby_id}/join/")
def join_game(lobby_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return 1


# Empezar la partida
@r.post("/lobbies/{lobby_id}/start/")
def start_game(
        lobby_id: int,
        current_players: LobbyStart,
        Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return 1