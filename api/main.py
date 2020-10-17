from typing import Optional, List
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from enum import Enum, IntEnum


app = FastAPI()

## REVISAR LOS NOMBRES DE LAS VARIABLES, NO SON FINALES

class UserIn(BaseModel):
    username: str
    #age: Optional[int] = None
    mail: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    #password: str

class LobbyIn(BaseModel):
    game_id: int
    name: str
    max_players: int

class LobbyOut(BaseModel):
    game_id: int
    name: str
    current_players: int
    max_players: int

#seguro no hacen falta los _ (guin bajos)
class Role(str, Enum):
    eater = "death_eather"
    voldemort = "voldemort"
    phoenix = "order_of_the_phoenix"

#Hacer los valores mas bonitos
class Spell(str, Enum):
    divination = "divination"
    avada = "avada_kedavra"
    crucio = "crucio"
    imperio = "imperio"

class Proclamation(IntEnum):
    good = 1
    bad = 2

class Player(BaseModel):
    player_id: int
    vote: bool
    role: Role

class Minister(BaseModel):
    player_id: int
    spell_target: int
    spell: Spell
    proc: List[Proclamation]
    expelliarmus: bool

class Director(BaseModel):
    player_id: int
    proc: List[Proclamation]
    expelliarmus: bool

class GameIn(BaseModel):
    game_id: int

class GameOut(BaseModel):
    game_id: int
    player_list: List[Player]
    minister: Minister
    director: Director



@app.get("/users/")
async def get_user_list(
    user_from: Optional[int] = 0, 
    user_to: Optional[int] = None
):
    return

@app.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    return 


@app.post("/users/",             
            response_model=UserOut,
            status_code=status.HTTP_201_CREATED)
async def create_user(new_user: UserIn) -> int:
    return 1


@app.get("/lobbies/")
async def get_lobby_list(
    lobby_from: Optional[int] = 0, 
    lobby_to: Optional[int] = None
):
    return

@app.get("/lobbies/{lobby_id}", response_model=LobbyOut)
async def get_lobby(lobby_id: int):
    return 


@app.post("/lobbies/",             
            response_model=LobbyOut,
            status_code=status.HTTP_201_CREATED)
async def create_lobby(new_lobby: LobbyIn) -> int:
    return 1


@app.get("/games/")
async def get_game_list(
    game_from: Optional[int] = 0, 
    game_to: Optional[int] = None
):
    return

@app.get("/games/{game_id}", response_model=GameOut)
async def get_game(game_id: int):
    return 


@app.post("/games/",             
            response_model=GameOut,
            status_code=status.HTTP_201_CREATED)
async def create_game(new_game: GameIn) -> int:
    return 1


"""
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    res_user = None
    res_user = get_user_by_id(user_id=user_id)
    if not res_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="user not found"
        )
    return res_user
 
@app.get("/users/")
async def get_user_list(
    user_from: Optional[int] = 0, 
    user_to: Optional[int] = None
):
    return USERS[user_from:user_to]

@app.post(
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