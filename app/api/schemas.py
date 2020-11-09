from typing import Optional, List
from pydantic import BaseModel, EmailStr
from enum import Enum, IntEnum


'''
Las clases estan divididas según los siguientes criterios (priorizados):
1. Endpoint en los que participan
2. Si es parte de una request o una respuesta
3. Intentar ocultar información que no debería poder accederse
       (i.e.: en vez de reutilizar una clase que comparte más información,
       creamos una distinta más pequeña)
=> Quiźas se puede utilizar el tipo Optional para poder reutilizar clases

Ejemplo de uso:

Estamos jugando, se acaba de resolver que vamos a ser el ministro,
 y ahora nuestro cliente debería mostrarnos las cartas de proclamación
 de las cuales podemos elejir.

El front end manda una GET request a

localhost:8080/<game_id>/minister

internamente (con jwt) se verifica que realmente seamos nosotros
 (el ministro) los que pedimos la información, y responde devolviendo
 una instancia de MinisterProc
'''

# Pensar en el caso de como ocultar la información de los votos hasta que
# se termine


# Register user input data
class UserReg(BaseModel):
    username: str
    email: EmailStr
    password: str


# Login user input data
class UserAuth(BaseModel):
    email: str
    password: str


# Game list output data
class UserGames(BaseModel):
    email: str
    games: List[int]


# Recover account input data
class RecoverAccount(BaseModel):
    email: EmailStr


# User's public output data
class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


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


# Player output pulic data
class PlayerPublic(BaseModel):
    player_id: int
    alive: bool
    voted: bool  # if the player already voted this round
    last_vote: bool  # last public vote
    position: int
    username: str
    role: Optional[Role]


# Cast spell input data
class CastSpell(BaseModel):
    spell_target: int  # if -1 then there's no target
    spell: Spell  # no es necesario realmente (explicado arriba)


# Proposed director input data
class ProposedDirector(BaseModel):
    player: int


# Card output data
class CardToProclaim(BaseModel):
    card_pos: int
    phoenix: bool


# Card input data
class Card(BaseModel):
    card_pos: int
    to_proclaim: bool


# Legislative session's input data
#   * proclamation indicates the cards to proclaim
#   * expelliarmus indicates an expelliarmus spell intent
class LegislativeSession(BaseModel):
    proclamation: List[Card]
    expelliarmus: bool  # ignored unless it's usable


# Create lobby input data
class LobbyReg(BaseModel):
    name: str
    max_players: int


# Start lobby input data
class LobbyStart(BaseModel):
    current_players: int  # redundant


# Lobby's public output data
class LobbyPublic(BaseModel):
    id: int
    name: str
    current_players: List[str]  # list of usernames
    max_players: int
    started: bool
    # is_owner is true if player who sends the request is lobby's owner.
    is_owner: bool
    # chat


# Game's proclamations' statusgo
class Score(BaseModel):
    good: int
    bad: int


# Game's public output data
class GamePublic(BaseModel):
    player_list: List[PlayerPublic]  # players order
    voting: bool
    in_session: bool  # currently in legislative session
    minister_proclaimed: bool  # did the minister pass the proc cards?
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
