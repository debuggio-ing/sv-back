from typing import Optional, List
from fastapi import APIRouter, HTTPException, Request, Depends, Response, status
from pydantic import BaseModel, EmailStr
from enum import Enum, IntEnum
from fastapi_jwt_auth import AuthJWT

from app.api.schemas import *
from app.database.models import *
from app.database.crud import *

r = users_router = APIRouter()

# Registrar un usuario nuevo
@r.post("/register/",
             status_code=status.HTTP_201_CREATED)
def create_user(new_user: UserReg) -> int:
    
    id = register_user(new_user)
    if id == -1:
        raise HTTPException(status_code=409, detail="Email already in use")
    return id

# Conseguir la informacion publica de un usuario
# solo por motivos de testeo, no estara presente en el producto final
@r.get("/users/{user_id}/", response_model=UserPublic)
def get_user(user_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return

# Ver la lista de juegos a los que el jugador se unió.
@r.get("/users/{user_id}/games", response_model=UserGames)
def get_user_games(user_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return


# Recuperación de cuenta
@r.post("/recover/")
def recover_user(email: RecoverAccount):
    return 1

#Endpoint para recibir las futuras verificaciones de email
@r.post("/verify/", status_code=200)
def verify_email():
    return