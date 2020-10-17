from fastapi import Depends, FastAPI, HTTPException
from pony.orm import *
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    username: str
    password: str

    class Config:
        orm_mode = True

db = Database()

class User(db.Entity):
    # id = Required(int)
    mail = Required(str)
    username = Required(str)
    password = Required(str)

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

app = FastAPI()

@app.post("/users/")
async def create_user(user: UserBase):
    with db_session:
        User(mail = user.email, username = user.username, password = user.password)
        commit()
        select(p for p in User).show()

    return {"Hello": "World"}
