from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field, BaseSettings
from fastapi_jwt_auth import AuthJWT
from datetime import timedelta
from typing import Literal

# Source:
# https://pypi.org/project/fastapi-jwt-auth/

# dotenv file parsing requires python-dotenv to be installed
# This can be done with either pip install python-dotenv
class Settings(BaseSettings):
    authjwt_access_token_expires: timedelta = timedelta(minutes=15)
    authjwt_refresh_token_expires: timedelta = timedelta(days=30)
    # literal type only available for python 3.8
    authjwt_blacklist_enabled: Literal['true', 'false']
    authjwt_secret_key: str
    authjwt_algorithm: str = 'HS256'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@AuthJWT.load_env
def get_settings():
    return [
        ("authjwt_access_token_expires", timedelta(minutes=2)),
        ("authjwt_refresh_token_expires", timedelta(days=5)),
        ("authjwt_blacklist_enabled", "false"),
        ("authjwt_secret_key", "debuggioSuperRandomGeneratedKey"),
        ("authjwt_algorithm", "HS256")
    ]


app = FastAPI()


class User(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
@app.post('/login', status_code=200)
def login(user: User, Authorize: AuthJWT = Depends()):
    if user.username != 'test' or user.password != 'test':
        raise HTTPException(status_code=401, detail='Bad username or password')

    # Identity must be between string or integer.
    access_token = Authorize.create_access_token(identity=user.username)
    return {"access_token": access_token}


@app.get('/protected', status_code=200)
def protected(Authorize: AuthJWT = Depends()):
    # Protect an endpoint with jwt_required.
    Authorize.jwt_required()

    # Access the identity of the current user with get_jwt_identity.
    current_user = Authorize.get_jwt_identity()
    return {"logged_in_as": current_user}

# Endpoint used to refresh access token.
@app.post('/refresh', status_code=200)
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_identity()
    return {
        'access_token': Authorize.create_access_token(
            identity=current_user)}
