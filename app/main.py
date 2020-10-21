from fastapi import Depends, FastAPI, HTTPException

from api.routers.games import games_router
from api.routers.lobbies import lobbies_router
from api.routers.users import users_router
from api.routers.auth import auth_router


app = FastAPI(
    title="Secret-Voldemort", docs_url="/api/docs", openapi_url="/api", redoc_url="/api/redoc"
)

app.include_router(users_router, prefix="/api", tags=["users"])
app.include_router(games_router, prefix="/api", tags=["games"])
app.include_router(lobbies_router, prefix="/api", tags=["lobbies"])
app.include_router(auth_router, prefix="/api", tags=["auth"])
