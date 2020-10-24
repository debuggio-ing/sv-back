from fastapi import APIRouter, HTTPException, Request, Depends, Response
from pydantic import BaseModel, Field, BaseSettings
from fastapi_jwt_auth import AuthJWT
from datetime import timedelta
from typing import Literal

from app.api.schemas import *
from app.database.models import *
from app.database.crud import *
from app.api.hasher import *

# IMPORTANTE RECORDAR ESTO
# dotenv file parsing requires python-dotenv to be installed


#Enrutador de endpoints de autenticación
r = auth_router = APIRouter()


# Modelo para la configuración del módulo AuthJWT
class Settings(BaseSettings):
    authjwt_access_token_expires: timedelta
    authjwt_refresh_token_expires: timedelta
    # literal type only available for python 3.8
    authjwt_blacklist_enabled: Literal['true', 'false']
    authjwt_secret_key: str
    authjwt_algorithm: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@AuthJWT.load_env
def get_settings():
    return [
        ("authjwt_access_token_expires", timedelta(minutes=5)),
        ("authjwt_refresh_token_expires", timedelta(days=7)),
        ("authjwt_blacklist_enabled", "false"),
        ("authjwt_secret_key", "debuggioSuperRandomGeneratedKey"),
        ("authjwt_algorithm", "HS256")
    ]

# Autenticar el usuario y generar el token de autorización
@r.post("/login/")
def authenticate_user(
        user_auth: UserAuth,
        Authorize: AuthJWT = Depends()) -> str:

    # Get all user's emails and passwords.
    tokens = {}

    # Crate an access token if it's a valid user.
    if check_password(user_auth.email, user_auth.password):
        tokens = {
            'access_token': Authorize.create_access_token(
                identity=user_auth.email), 'refresh_token': Authorize.create_refresh_token(
                identity=user_auth.email)}
    else:
        raise HTTPException(status_code=401, detail='Bad email or password')

    return tokens

# Endpoint donde se refresca el Refresh Token
@r.post("/refresh/", status_code=200)
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_identity()
    return {
        'access_token': Authorize.create_access_token(
            identity=current_user)}
