from fastapi import APIRouter, status

from app.validators.auth_validator import *
from app.validators.game_validator import *

from typing import Optional


# Lobbies endpoints' router
r = lobbies_router = APIRouter()


# Return lobbies list.
@r.post("/lobbies/", response_model=List[LobbyPublic])
def get_lobby_list(
    filterForm: LobbyFilter,
    lobby_from: Optional[int] = 0,
    lobby_to: Optional[int] = None,
    auth: AuthJWT = Depends()
):
    user_email = validate_user(auth=auth)

    # get all lobbies which haven't started
    lobby_id_list = get_all_lobbies_ids(
        lobby_from=lobby_from,
        lobby_to=lobby_to,
        available=filterForm.available,
        user_games=filterForm.user_games,
        started=filterForm.started,
        finished=filterForm.finished,
        all_games=filterForm.all_games,
        user_email=user_email)

    lobbies = []
    for lobby_id in lobby_id_list:
        lobby = get_lobby_public_info(lobby_id=lobby_id, user_email=user_email)
        lobbies.append(lobby)

    return lobbies


# Return lobby_id lobby information.
@r.get("/lobbies/{lobby_id}/", response_model=LobbyPublic)
def get_lobby(lobby_id: int, auth: AuthJWT = Depends()):
    user_email = validate_user(auth=auth)

    if lobby_exists(lobby_id):
        lobby = get_lobby_public_info(lobby_id=lobby_id, user_email=user_email)
    else:
        raise HTTPException(
            status_code=404, detail='Lobby not found.')
    return lobby


# Create new lobby.
@r.post("/lobbies/new/",
        response_model=LobbyPublic,
        status_code=status.HTTP_201_CREATED)
def create_lobby(new_lobby: LobbyReg, auth: AuthJWT = Depends()):
    user_email = validate_user(auth=auth)

    lobby_id = insert_lobby(lobby=new_lobby, user_email=user_email)
    insert_player(user_email=user_email, lobby_id=lobby_id)

    current_players = get_lobby_player_list(lobby_id=lobby_id)
    lobby = get_lobby_public_info(lobby_id=lobby_id, user_email=user_email)

    return lobby


# Join lobby_id lobby.
@r.post("/lobbies/{lobby_id}/join/",
        response_model=LobbyPublic)
def join_game(lobby_id: int, auth: AuthJWT = Depends()):
    user_email = validate_user(auth=auth)

    if not lobby_exists(lobby_id=lobby_id):
        raise HTTPException(status_code=404,
                            detail="The game id is incorrect.")

    if insert_player(user_email=user_email, lobby_id=lobby_id) == -1:
        raise HTTPException(status_code=409,
                            detail="The game id is full.")

    current_players = get_lobby_player_list(lobby_id=lobby_id)
    lobby_name = get_lobby_name(lobby_id=lobby_id)
    lobby_max_players = get_lobby_max_players(lobby_id=lobby_id)
    lobby = get_lobby_public_info(lobby_id=lobby_id, user_email=user_email)

    return lobby


# Start lobby_id lobby.
@r.post("/lobbies/{lobby_id}/start/",
        response_model=StartConfirmation)
def start_game(lobby_id: int,
               # current_players: LobbyStart,
               auth: AuthJWT = Depends()):
    user_email = validate_user(auth=auth)

    if not get_lobby_is_owner(lobby_id=lobby_id, user_email=user_email):
        raise HTTPException(status_code=409,
                            detail="User is not game's owner.")

    if is_lobby_started(lobby_id):
        raise HTTPException(status_code=409,
                            detail="Game has already started.")

    users_in_lobby = get_lobby_player_list(lobby_id=lobby_id)
    if len(users_in_lobby) < 5:
        raise HTTPException(status_code=412,
                            detail="Not enough users in the lobby.")
    set_lobby_started(lobby_id=lobby_id)

    game_id = insert_game(lobby_id=lobby_id)

    return StartConfirmation(game_id=game_id)


# Deletes the player from the lobby.
@r.post("/lobbies/{lobby_id}/leave/",
        response_model=StartConfirmation)
def leave_game(lobby_id: int,
               # current_players: LobbyStart,
               auth: AuthJWT = Depends()):
    user_email = validate_user(auth=auth)
    player_id = get_player(email=user_email, game_id=game_id)

    if is_lobby_started(lobby_id):
        raise HTTPException(status_code=409,
                            detail="Game has already started.")
    
    delete_player_from_game(player_id=player_id, game_id=lobby_id)

    return StartConfirmation(game_id=lobby_id)
