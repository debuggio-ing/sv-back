from fastapi import Depends, FastAPI, HTTPException
from pony.orm import *

from app.api.routers.games import games_router
from app.api.routers.lobbies import lobbies_router
from app.api.routers.users import users_router
from app.api.routers.auth import auth_router
from app.database.models import *


db = Database(provider='sqlite', filename=':memory:', create_db=True)
define_entities(db)
db.generate_mapping(create_tables=True)

svapi = FastAPI(
    title="Secret-Voldemort", docs_url="/api/docs", openapi_url="/api", redoc_url="/api/redoc"
)

svapi.include_router(users_router, prefix="/api", tags=["users"])
svapi.include_router(games_router, prefix="/api", tags=["games"])
svapi.include_router(lobbies_router, prefix="/api", tags=["lobbies"])
svapi.include_router(auth_router, prefix="/api", tags=["auth"])