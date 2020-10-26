from fastapi import Depends, FastAPI, HTTPException
from pony.orm import *

from app.api.routers.games import games_router
from app.api.routers.lobbies import lobbies_router
from app.api.routers.users import users_router
from app.api.routers.auth import auth_router

from app.database.models import *

from fastapi.middleware.cors import CORSMiddleware
from app.database.crud import create_db

svapi = FastAPI(
    title="Secret-Voldemort", docs_url="/api/docs", openapi_url="/api", redoc_url="/api/redoc"
)
origins = [
    "http://localhost",
    "http://localhost:8080"
]
svapi.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_db(True)

svapi.include_router(users_router, prefix="/api", tags=["users"])
svapi.include_router(games_router, prefix="/api", tags=["games"])
svapi.include_router(lobbies_router, prefix="/api", tags=["lobbies"])
svapi.include_router(auth_router, prefix="/api", tags=["auth"])

