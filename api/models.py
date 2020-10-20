from typing import Optional, List
from pydantic import BaseModel, EmailStr
from enum import Enum, IntEnum



## REVISAR LOS NOMBRES DE LAS VARIABLES, NO SON FINALES

'''
Las clases estan divididas según los siguientes criterios (priorizados):
1. Endpoint en los que participan
2. Si es parte de una request o una respuesta
3. Intentar ocultar información que no debería poder accederse 
       (i.e.: en vez de reutilizar una clase que comparte más información, 
       creamos una distinta más pequeña)

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


#Información para registrar un usuario
class UserReg(BaseModel):
    username: str
    #age: Optional[int] = None
    email: EmailStr
    password: str

#Información que provée el usuario en el Login
class UserAuth(BaseModel):
    email: str
    password: str

#Información devuelta del usuario
class UserOut(BaseModel):
    id: int #creo que con jwt este atributo se vuelve irrelevante
            #pero lo dejamos hasta que implementemos la autenticación
    username: str
    email: EmailStr
    #password: str
    #photo?

#Enumerado de conjuros
#Me parece que es un dato derivado, asi que quizás la api nunca lo utilice
#pero creo que se le puede informar al front los hechizos a mostrar en el board
class Spell(str, Enum):
    divination = "Divination"
    avada = "Avada Kedavra"
    crucio = "Crucio"
    imperio = "Imperio"

#Enumerado con los posibles roles
class Role(str, Enum):
    eater = "Death Eater"
    voldemort = "voldemort"
    phoenix = "Order of the Phoenix"

#Información que se puede requerir por el usuario
class PlayerOut(BaseModel):
    player_id: int
    vote: bool
    role: Role
    username: str

#Información pública para todos los jugadores
class PlayerPublic(BaseModel):
    player_id: int
    vote: bool
    username: str

#Información sobre el hechizo a utilizar
class MinisterSpell(BaseModel):
    spell_target: int #player_id
    spell: Spell #no es necesario realmente (explicado arriba)

#Informacíon sobre la decición de proclamación
#bajo las condiciones los jugadores pueden utilizar expelliarmus 
#en vez de resolver la sesion legislativa
class MinisterProc(BaseModel):
    proc: List[bool]
    expelliarmus: bool #ignorado al menos que se den las circunstancias

#Lo mismo pero para el director
class DirectorProc(BaseModel):
    proc: List[bool]
    expelliarmus: bool #ignorado al menos que se den las circunstancias

#Información necesaria para crear una partida
class LobbyReg(BaseModel):
    game_id: int
    name: str
    max_players: int

#Información para comenzar la partida
#se va a verificar que la sala contenga la cantidad correcta de jugadores
#a la hora de mandar la señal de inicio de partida
class LobbyStart(BaseModel):
    game_id: int
    current_players: int

#Información pública del lobby
class LobbyPublic(BaseModel):
    game_id: int
    name: str
    current_players: List[str] #list of usernames
    max_players: int
    #chat

#Información necesaria para pedir información sobre el juego
#Notese que game_id es compartido con Lobby
class GameIn(BaseModel):
    game_id: int

#Información pública de la partida
class GamePublic(BaseModel):
    game_id: int
    player_list: List[PlayerPublic] #con el orden de los jugadores
    minister: str
    director: str




