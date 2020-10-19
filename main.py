from fastapi import Depends, FastAPI, HTTPException
from schemas import *
from models import *
from crud import *

app = FastAPI()

# Create user and store it into the database endpoint.
@app.post("/users/")
async def create_user(user: UserSchema):
    insert_user(user)

    return {"username created":user.username}

# Get all users endpoint.
@app.get("/users/")
async def get_users():
    with db_session:
        users = get_usernames()
        emails = get_emails()

    return dict(zip(users, emails))
