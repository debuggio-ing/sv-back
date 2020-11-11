from typing import Optional, List
from fastapi import APIRouter, HTTPException, Request, Depends, Response, status
from pydantic import BaseModel, EmailStr
from enum import Enum, IntEnum
from fastapi_jwt_auth import AuthJWT
from app.api.routers_helpers.auth_helper import *
from app.api.routers_helpers.user_helper import *
from app.api.schemas import *
from app.database.models import *
from app.database.crud import *


# Users endpoints' router
r = users_router = APIRouter()


# Create new user.
@r.post("/register/",
        status_code=status.HTTP_201_CREATED)
def create_user(new_user: UserReg) -> int:
    id = register_user(user=new_user)
    if id == -1:
        raise HTTPException(status_code=409, detail="Email already in use")

    return id


# Return user information.
@r.get("/users/info/", response_model=UserPublic)
def get_user(auth: AuthJWT = Depends()):
    user_email = validate_user(auth=auth)

    return get_user_public(user_email=user_email)


# Return user information.
@r.post("/users/info/modify/", response_model=UserPublic)
def modify_user_info(new_profile: UserProfile, auth: AuthJWT = Depends()):
    user_email = validate_user(auth=auth)
    if new_profile.username is not None and new_profile.password is not None:
        # update both the username and password
        set_username(user_email=user_email, username=new_profile.username)
        set_password(user_email=user_email, password=new_profile.password)
    elif new_profile.username is not None:
        # update username
        set_username(user_email=user_email, username=new_profile.username)
    elif new_profile.password is not None:
        # update password
        set_password(user_email=user_email, password=new_profile.password)
    else:
        # illegal request
        raise HTTPException(status_code=400, detail="Illegal request")

    return get_user_public(user_email=user_email)


# Return all lobbies that user with jwt is in.
@r.get("/users/games/", response_model=UserGames)
def get_user_active_games(auth: AuthJWT = Depends()):
    user_email = validate_user(auth=auth)
    games = get_active_games(user_email)

    return UserGames(email=user_email, games=games)


# Send email to recover account.
@r.post("/recover/")
def recover_user(email: RecoverAccount):
    return 1


# Verify email.
@r.post("/verify/", status_code=200)
def verify_email(user_email: str, input_code: int) -> bool:
    code = get_verification_code(user_email=user_email)

    if code != input_code:
        raise HTTPException(status_code=409, detail="Invalid code.")

    set_user_email_verified(user_email=user_email)

    return UserVerify(email=user_email, verified=True)
