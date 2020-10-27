from app.database.models import *
from app.api.schemas import *


# Return the required game status.
@db_session
def get_game_status(game_id: int) -> GamePublic:

    lobby = Lobby.get(id=game_id)
    game = lobby.game
    ans = GamePublic()
    return

@db_session
def get_all_games_ids(game_from: int, game_to: int):
    return []

@db_session
def get_game_player_public_list(gid):
    p_entities_list = list(select(
        p.id for p in Player if gid == p.lobby.id))

    players = [get_player_public(pid) for pid in p_entities_list]

    return players

@db_session
def get_game_minister(gid):
    return

@db_session
def get_game_director(gid):
    return

@db_session
def get_game_semaphore(gid):
    return

@db_session
def get_game_score(gid):
    return