from typing import List, Optional
from pydantic import BaseModel

class UserSchema(BaseModel):
    email: str
    username: str
    password: str

    # "Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict,
    # but an ORM model (or any other arbitrary object with attributes)."
    # source: https://fastapi.tiangolo.com/tutorial/sql-databases/
    # class Config:
    #     orm_mode = True
