from typing import Optional, List
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from enum import Enum, IntEnum

from models import * 


routes = FastAPI()

#Todo necesita ser ajustado para la autenticación con JWT


#TO-DO
#mejorar el codigo para enriqueser la documentación generada
#todo lo demas

#Esta ruta está por razones de testeo, no va en el producto final
@routes.get("/users/")
def get_user_list(
    user_from: Optional[int] = 0, 
    user_to: Optional[int] = None
):
    return

#Conseguir la informacion publica de un usuario
#solo por motivos de testeo, no estara presente en el producto final
@routes.get("/users/{user_id}/", response_model=UserPublic)
def get_user(user_id: int):
    return 

#Registrar un usuario nuevo
@routes.post("/users/register/",             
            response_model=UserPublic,
            status_code=status.HTTP_201_CREATED)
def create_user(new_user: UserReg) -> int:
    return 1


#Autenticar el usuario y generar el token de autorización
@routes.post("/users/login/")
def authenticate_user(user_auth: UserAuth) -> str:
    return "access_token"


#Ver la lista de salas
@routes.get("/lobbies/")
def get_lobby_list(
    lobby_from: Optional[int] = 0, 
    lobby_to: Optional[int] = None
):
    return


#Ver la información de mi sala
@routes.get("/lobbies/{lobby_id}/", response_model=LobbyPublic)
def get_lobby(lobby_id: int):
    return 


#Crear una nueva sala
@routes.post("/lobbies/new/",             
            response_model=LobbyPublic,
            status_code=status.HTTP_201_CREATED)
def create_lobby(new_lobby: LobbyReg) -> int:
    return 1

#Unirse a una sala
#la información del usuario se obtiene del JWT
@routes.post("/lobbies/{lobby_id}/join/")   
def join_game(lobby_id: int):
    return 1


#Empezar la partida
@routes.post("/lobbies/{lobby_id}/start/")   
def start_game(lobby_id: int, current_players: LobbyStart):
    return 1


#ver el listado de los juegos
@routes.get("/games/")
def get_game_list(
    game_from: Optional[int] = 0, 
    game_to: Optional[int] = None
):
    return


#Ver la información pública del juego
@routes.get("/games/{game_id}/", response_model=GamePublic)
def get_game(game_id: int):
    return 

#el jugador vota
#identificacion a travez del token JWT
@routes.post("/games/{game_id}/vote/", response_model=PlayerVote)
def player_vote(game_id: int):
    return 


#Ver rol del jugador
@routes.get("/games/{game_id}/role/", response_model=PlayerRole)
def get_player_role(game_id: int):
    return 

#El ministro utilizá un hechizo
@routes.post("/games/{game_id}/spell/")
def cast_spell(game_id: int, spell: CastSpell):
    return 

#El ministro o el director pide las cartas de proclamación
@routes.get("/games/{game_id}/proc/", response_model=LegislativeSession)
def get_minister_proc(game_id: int):
    return 

#Elección de cartas de proclamación durante la sesión legislativa
#internamente se dan cartas correspondientes al cargo del jugador
@routes.post("/games/{game_id}/proc/")
def proc_election(game_id: int, election: LegislativeSession):
    return 

#Elección de director
@routes.post("/games/{game_id}/director/")
def director_candidate(game_id: int, candidate: ProposedDirector):
    return 

