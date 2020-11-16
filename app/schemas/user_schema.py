from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, EmailStr


# Register user input data
class UserReg(BaseModel):
    nickname: str
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


# User's modification profile input data
class UserProfile(BaseModel):
    nickname: Optional[str]
    password: Optional[str]


# Recover account input data
class RecoverAccount(BaseModel):
    email: EmailStr


# User's public output data
class UserPublic(BaseModel):
    id: int
    nickname: str
    email: EmailStr


# Verify user confirmation.
class UserVerify(BaseModel):
    email: str
    verified: bool
