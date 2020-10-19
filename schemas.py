from typing import List, Optional
from pydantic import BaseModel

# Create pydantic user schema for input parsing.
class UserSchema(BaseModel):
    email: str
    username: str
    password: str
