from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field, BaseSettings
from fastapi_jwt_auth import AuthJWT
from datetime import timedelta
from typing import Literal

# IMPORTANTE RECORDAR ESTO
# dotenv file parsing requires python-dotenv to be installed

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
        ("authjwt_access_token_expires", timedelta(minutes=2)),
        ("authjwt_refresh_token_expires", timedelta(days=7)),
        ("authjwt_blacklist_enabled", "false"),
        ("authjwt_secret_key", "debuggioSuperRandomGeneratedKey"),
        ("authjwt_algorithm", "HS256")
    ]
