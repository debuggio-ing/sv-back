from app.database.crud import *
from fastapi import HTTPException


# Set nickname for the solicited user.
def set_nickname(user_email: str, nickname: str):
    change_nickname(user_email=user_email, nickname=nickname)
