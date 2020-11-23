from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, EmailStr

from app.schemas.game_schema import *


# Create lobby input data
class LobbyReg(BaseModel):
    name: str
    max_players: int


# Start lobby input data
class LobbyStart(BaseModel):
    current_players: int  # redundant


# Lobby's public output data
class LobbyFilter(BaseModel):
    available: bool
    started: bool
    finished: bool
    user_games: bool
    all_games: bool


# Lobby's public output data
class LobbyPublic(BaseModel):
    id: int
    name: str
    current_players: List[str]  # list of nicknames
    max_players: int
    started: bool
    finished: bool
    # is_owner is true if player who sends the request is lobby's owner.
    is_owner: bool
    messages: List[MessageSchema]
