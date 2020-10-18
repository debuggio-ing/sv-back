from fastapi import Depends, FastAPI, HTTPException
from schemas import *
from models import *
from crud import *

app = FastAPI()

@app.post("/users/")
async def create_user(user: UserSchema):
    insert_user(user)

    return {"hello":"world"}

@app.get("/users/")
async def get_users():
    with db_session:
        users = get_usernames()
        emails = get_emails()

    return dict(zip(users, emails))
