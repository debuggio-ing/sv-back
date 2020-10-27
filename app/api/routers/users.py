from typing import Optional, List
from fastapi import APIRouter, HTTPException, Request, Depends, Response, status
from pydantic import BaseModel, EmailStr
from enum import Enum, IntEnum
from fastapi_jwt_auth import AuthJWT

from app.api.schemas import *
from app.database.models import *
from app.database.crud import *


# Users endpoints' router
r = users_router = APIRouter()


# Create new user.
@r.post("/register/",
        status_code=status.HTTP_201_CREATED)
def create_user(new_user: UserReg) -> int:

    id = register_user(new_user)
    if id == -1:
        raise HTTPException(status_code=409, detail="Email already in use")
    return id


# Return user_id user information.
@r.get("/users/{user_id}/", response_model=UserPublic)
def get_user(user_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return


# Return all lobies that user_id user is in.
@r.get("/users/{user_id}/games", response_model=UserGames)
def get_user_games(user_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return


# Send email to recover account.
@r.post("/recover/")
def recover_user(email: RecoverAccount):
    return 1


# Verify email.
@r.post("/verify/", status_code=200)
def verify_email():
    return
