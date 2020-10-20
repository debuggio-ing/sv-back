from typing import Optional, List
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from enum import Enum, IntEnum

from models import * 


routes = FastAPI()


#Esta ruta está por razones de testeo, no va en el producto final
@routes.get("/users/")
async def get_user_list(
    user_from: Optional[int] = 0, 
    user_to: Optional[int] = None
):
    return

@routes.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    return 


@routes.post("/users/",             
            response_model=UserOut,
            status_code=status.HTTP_201_CREATED)
async def create_user(new_user: UserIn) -> int:
    return 1


@routes.get("/lobbies/")
async def get_lobby_list(
    lobby_from: Optional[int] = 0, 
    lobby_to: Optional[int] = None
):
    return

@routes.get("/lobbies/{lobby_id}", response_model=LobbyOut)
async def get_lobby(lobby_id: int):
    return 


@routes.post("/lobbies/",             
            response_model=LobbyOut,
            status_code=status.HTTP_201_CREATED)
async def create_lobby(new_lobby: LobbyIn) -> int:
    return 1


@routes.get("/games/")
async def get_game_list(
    game_from: Optional[int] = 0, 
    game_to: Optional[int] = None
):
    return

@routes.get("/games/{game_id}", response_model=GameOut)
async def get_game(game_id: int):
    return 


@routes.post("/games/",             
            response_model=GameOut,
            status_code=status.HTTP_201_CREATED)
async def create_game(new_game: GameIn) -> int:
    return 1


"""
@routes.get("/users/{user_id}")
async def get_user(user_id: int):
    res_user = None
    res_user = get_user_by_id(user_id=user_id)
    if not res_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="user not found"
        )
    return res_user
 
@routes.get("/users/")
async def get_user_list(
    user_from: Optional[int] = 0, 
    user_to: Optional[int] = None
):
    return USERS[user_from:user_to]

@routes.post(
    "/users/", 
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED
)
async def create_user(new_user: UserIn) -> int:
    new_id = len(USERS) + 1
    user_dict = new_user.dict()
    user_dict.update({"id": new_id})
    USERS.append(user_dict)
    return UserOut(
        id=new_id, 
        name=new_user.name, 
        operation_result="Succesfully created!")


"""