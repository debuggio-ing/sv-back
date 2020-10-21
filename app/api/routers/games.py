from fastapi import APIRouter, HTTPException, Request, Depends, Response
from pydantic import BaseModel, Field, BaseSettings
from fastapi_jwt_auth import AuthJWT
from datetime import timedelta
from typing import Literal, Optional

from app.api.schemas import *
from app.database.models import *
from app.database.crud import *

r = games_router = APIRouter()

# ver el listado de los juegos
@r.get("/games/")
def get_game_list(
    game_from: Optional[int] = 0,
    game_to: Optional[int] = None, Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return


# Ver la información pública del juego
@r.get("/games/{game_id}/", response_model=GamePublic)
def get_game(game_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return

# el jugador vota
# identificacion a travez del token JWT


@r.post("/games/{game_id}/vote/", response_model=PlayerVote)
def player_vote(game_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return


# Ver rol del jugador
@r.get("/games/{game_id}/role/", response_model=PlayerRole)
def get_player_role(game_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return

# El ministro utilizá un hechizo


@r.post("/games/{game_id}/spell/")
def cast_spell(game_id: int, spell: CastSpell, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return

# El ministro o el director pide las cartas de proclamación


@r.get("/games/{game_id}/proc/", response_model=LegislativeSession)
def get_minister_proc(game_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return

# Elección de cartas de proclamación durante la sesión legislativa
# internamente se dan cartas correspondientes al cargo del jugador
@r.post("/games/{game_id}/proc/")
def proc_election(
        game_id: int,
        election: LegislativeSession,
        Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return

# Elección de director
@r.post("/games/{game_id}/director/")
def director_candidate(
        game_id: int,
        candidate: ProposedDirector,
        Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return

