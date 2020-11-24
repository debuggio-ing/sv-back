from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, EmailStr


# Confirmation if the game started
class StartConfirmation(BaseModel):
    game_id: int


# Enumerado de conjuros
# Me parece que es un dato derivado, asi que quizás la api nunca lo utilice
# pero creo que se le puede informar al front los hechizos a mostrar en el
# board
class Spell(str, Enum):
    divination = "Divination"
    avada = "Avada Kedavra"
    crucio = "Crucio"
    imperio = "Imperio"


# [ENUM class] Players' possible roles
class Role(str, Enum):
    eater = "Death Eater"
    voldemort = "voldemort"
    phoenix = "Order of the Phoenix"


# Player's input vote
class PlayerVote(BaseModel):
    vote: bool


# Players' output role
class PlayerRole(BaseModel):
    role: Role


# Player output public data
class PlayerPublic(BaseModel):
    player_id: int
    alive: bool
    voted: bool  # if the player already voted this round
    last_vote: bool  # last public vote
    position: int
    nickname: str
    role: Optional[Role]


# Cast spell input data
class CastSpell(BaseModel):
    target: int


# Proposed director input data
class ProposedDirector(BaseModel):
    player: int


# Legislative session input data
class Legislation(BaseModel):
    election: int
    expelliarmus: bool


# Card output data
class CardToProclaim(BaseModel):
    card_pos: int
    phoenix: bool


# Game's proclamations' status
class Score(BaseModel):
    good: int
    bad: int


# Message input data
class MessageIn(BaseModel):
    msg:str


# Message output data
class MessageSchema(BaseModel):
    sender: str
    message: str


# Game's public output data
class GamePublic(BaseModel):
    player_list: List[PlayerPublic]  # players order
    voting: bool
    in_session: bool  # currently in legislative session
    expelliarmus: bool # did the director ask for expelliarmus?
    minister_proclaimed: bool  # did the minister pass the proc cards?
    director_proclaimed: bool  # did the director pass the proc cards?
    last_proc_negative: bool
    minister: int
    prev_minister: int
    director: int
    prev_director: int
    semaphore: int
    score: Score
    end: Optional[bool]
    winners: Optional[bool]
    # players' role reaveal party at the end of the game
    roleReveal: Optional[List[Role]]
    client_minister: bool
    client_director: bool
    messages: List[MessageSchema]
