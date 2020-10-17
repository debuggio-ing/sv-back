from fastapi import Depends, FastAPI, HTTPException
from pony.orm import *

from models import *
from schemas import *

app = FastAPI()
db.generate_mapping(create_tables=True)

@app.post("/users/")
async def create_user(user: UserBase):
    with db_session:
        User(mail = user.email, username = user.username, password = user.password)
        commit()
        select(p for p in User).show()

    return {"Hello": "World"}
