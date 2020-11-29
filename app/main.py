from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth import auth_router
from app.routers.games import games_router
from app.routers.lobbies import lobbies_router
from app.routers.users import users_router
from app.database.binder import *


# svapi is the API object
svapi = FastAPI(
    title="Secret-Voldemort",
    docs_url="/api/docs",
    openapi_url="/api",
    redoc_url="/api/redoc")


bind_db(False)

# origins allowed by the API
origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://debuggio.herokuapp.com"
]


# CORS setup
svapi.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers handled by the API
svapi.include_router(users_router, prefix="/api", tags=["users"])
svapi.include_router(games_router, prefix="/api", tags=["games"])
svapi.include_router(lobbies_router, prefix="/api", tags=["lobbies"])
svapi.include_router(auth_router, prefix="/api", tags=["auth"])
