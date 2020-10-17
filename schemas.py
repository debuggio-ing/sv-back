from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    username: str
    password: str

    # class Config:
    #     orm_mode = True
