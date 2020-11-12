from app.database.crud import *
from fastapi import HTTPException


# Set nickname for the solicited user.
def set_nickname(user_email: str, nickname: str):
    if change_nickname(user_email=user_email, nickname=nickname) == -1:
        raise HTTPException(status_code=409, detail="nickname already in use")
