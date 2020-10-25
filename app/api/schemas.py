from typing import Optional, List
from pydantic import BaseModel, EmailStr
from enum import Enum, IntEnum


# REVISAR LOS NOMBRES DE LAS VARIABLES, NO SON FINALES

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

# Información para registrar un usuario


class UserReg(BaseModel):
    username: str
    #age: Optional[int] = None
    email: EmailStr
    password: str

# Información que provée el usuario en el Login


class UserAuth(BaseModel):
    email: str
    password: str


class UserGames(BaseModel):
    email: str
    games: List[int]

# Este nombre es muy precario


class RecoverAccount(BaseModel):
    email: EmailStr

# Información devuelta del usuario


class UserPublic(BaseModel):
    id: int  # creo que con jwt este atributo se vuelve irrelevante
    # pero lo dejamos hasta que implementemos la autenticación
    username: str
    email: EmailStr
    #password: str
    # photo?

# Enumerado de conjuros
# Me parece que es un dato derivado, asi que quizás la api nunca lo utilice
# pero creo que se le puede informar al front los hechizos a mostrar en el
# board


class Spell(str, Enum):
    divination = "Divination"
    avada = "Avada Kedavra"
    crucio = "Crucio"
    imperio = "Imperio"

# Enumerado con los posibles roles


class Role(str, Enum):
    eater = "Death Eater"
    voldemort = "voldemort"
    phoenix = "Order of the Phoenix"

# Información del voto de un jugador


class PlayerVote(BaseModel):
    vote: bool

# Información del rol del jugador


class PlayerRole(BaseModel):
    role: Role

# Información pública para todos los jugadores


class PlayerPublic(BaseModel):
    player_id: int
    vote: bool
    dead: bool
    username: str

# Información sobre el hechizo a utilizar


class CastSpell(BaseModel):
    spell_target: Optional[int]  # player_id
    spell: Spell  # no es necesario realmente (explicado arriba)

#


class ProposedDirector(BaseModel):
    player: int

# Informacíon sobre la decición de proclamación
# bajo las condiciones los jugadores pueden utilizar expelliarmus
# en vez de resolver la sesion legislativa


class LegislativeSession(BaseModel):
    proclamation: List[bool]
    expelliarmus: bool  # ignorado al menos que se den las circunstancias


# Información necesaria para crear una partida
class LobbyReg(BaseModel):
    name: str
    max_players: int


# Información para comenzar la partida
# se va a verificar que la sala contenga la cantidad correcta de jugadores
# a la hora de mandar la señal de inicio de partida
class LobbyStart(BaseModel):
    current_players: int

# Información pública del lobby


class LobbyPublic(BaseModel):
    id: int
    name: str
    current_players: List[str]  # list of usernames
    max_players: int
    # chat

# Muestra el numero de las proclamaciones por equipo


class Score(BaseModel):
    good: int
    bad: int

# Información pública de la partida
# Notese que game_id es compartido con Lobby
# quizás no hace falta diferenciarlos


class GamePublic(BaseModel):
    player_list: List[PlayerPublic]  # con el orden de los jugadores
    minister: str
    director: str
    semaphore: int
    end: bool
    winners: bool
    # al final del juego se muestran los roles de todos los jugadores
    roleReveal: Optional[List[Role]]
    score: Score
