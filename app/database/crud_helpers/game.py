from app.database.models import *
from app.api.schemas import *
from typing import List

@db_session
def get_all_games_ids(game_from: int, game_to: int) -> List[int]:
    return []

@db_session
def get_game_player_public_list(gid) -> List[PlayerPublic]:
    pid_list = list(select(
        p.id for p in Player if gid == p.lobby.id))

    players = [get_player_public(pid) for pid in pid_list]

    return players

@db_session
def get_game_minister_id(gid) -> int:
    minister = Player.get(lobby=gid, minister=True)
    return minister.id

@db_session
def get_game_director_id(gid) -> int:
    director = Player.get(lobby=gid, director=True)
    return director.id

@db_session
def get_game_semaphore(gid) -> int:
    lobby = Lobby.get(id=gid)
    sem = lobby.game.semaphore
    return sem

@db_session
def get_game_score(gid) -> Score:
    lobby = Lobby.get(id=gid)
    card_pool = select(c.to_dict() for c in lobby.game.cards)

    bad_score = len(select(c for c in card_pool if proclaimed == True and is_phoenix == False))
    good_score = len(select(c for c in card_pool if proclaimed == True and is_phoenix == True))

    return Score(good=good_score, bad=bad_score)
