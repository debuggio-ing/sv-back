from app.database.models import *
from app.api.schemas import *
from app.database.crud_helpers.user import *


# Create lobby in the database.
@db_session
def insert_lobby(lobby: LobbyReg, user_email: str) -> int:
    user_id = get_user_id(user_email)

    lobby_id = -1
    if user_id != -1:
        l = Lobby(name=lobby.name,
              max_players=lobby.max_players,
              creation_date=datetime.now(),
              owner_id=user_id)
        commit()
        lobby_id = l.id

    return lobby_id


# Get lobby_id lobby's owner_id attribute.
@db_session
def get_lobby_is_owner(lobby_id: int, user_email: str) -> int:
    lobby = Lobby.get(id=lobby_id)
    user_id = get_user_id(user_email=user_email)

    is_owner = False
    if lobby is not None and user_id != -1:
        is_owner = lobby.owner_id == user_id

    return is_owner


# Get all players username who are in lobby_id lobby.
@db_session
def get_lobby_player_list(lobby_id: int):
    players = list(select(
        p.user.username for p in Player if lobby_id == p.lobby.id))

    return players


# Get all player's id who are in lobby_id lobby.
@db_session
def get_lobby_players_id(lobby_id: int):
    players = list(select(
        p.id for p in Player if lobby_id == p.lobby.id))

    return players


# Get lobby_id lobby's name.
@db_session
def get_lobby_name(lobby_id: int):
    lobby = Lobby.get(id=lobby_id)

    name = ""
    if lobby is not None:
        name = lobby.name

    return name


# Get lobby_id lobby's max_player attribute.
@db_session
def get_lobby_max_players(lobby_id: int):
    lobby = Lobby.get(id=lobby_id)

    max_players = 0
    if lobby is not None:
        max_players = lobby.max_players

    return max_players


# Get lobby_id lobby's started attribute.
@db_session
def get_lobby_started(lobby_id: int) -> bool:
    lobby = Lobby.get(id=lobby_id)

    started = 0
    if lobby is not None:
        started = lobby.started

    return started


@db_session
def set_lobby_started(lobby_id: int):
    lobby = Lobby.get(id=lobby_id)

    if lobby is not None:
        lobby.started = True


# Get all lobbies ids.
@db_session
def get_all_lobbies_ids(lobby_from: Optional[int], lobby_to: Optional[int]):
    max_id = max(l.id for l in Lobby)
    if lobby_to is None and max_id is not None:
        # If there's an active lobby, set lobby_to = max_id.
        lobby_to = max_id
    elif lobby_to is None and max_id is None:
        # If there's no active lobby, set lobby_to = 0.
        lobby_to = 0

    # Get all lobies with id within range.
    lobbies_ids = list(select(l.id for l in Lobby if
                              l.id >= lobby_from and l.id <= lobby_to))

    return lobbies_ids


# Check if lobby id==lid exists 
@db_session
def lobby_exists(lid):
    return Lobby.get(id=lid) is not None


# Check if lobby has started.
@db_session
def is_lobby_started(lobby_id: int) -> bool:
    lobby = Lobby.get(id=lobby_id)  

    started = False
    if lobby is not None and lobby.game is not None:
        started = True

    return started
