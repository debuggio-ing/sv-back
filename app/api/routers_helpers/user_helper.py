from app.database.crud import *
from fastapi import HTTPException


# Set username for the solicited user.
def set_username(user_email: str, username: str):
    if change_username(user_email=user_email, username=username) == -1:
        raise HTTPException(status_code=409, detail="Username already in use")
