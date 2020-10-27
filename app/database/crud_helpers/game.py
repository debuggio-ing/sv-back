from app.database.models import *
from app.api.schemas import *
from app.database.crud_helpers.player import *
from typing import List


@db_session
def get_all_games_ids(game_from: int, game_to: int) -> List[int]:
    
    return list(select(g.id for g in Game))


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
def get_game_prev_minister_id(gid) -> int:
    pminister = Player.get(lobby=gid, prev_minister=True)
    return pminister.id


@db_session
def get_game_prev_director_id(gid) -> int:
    pdirector = Player.get(lobby=gid, prev_director=True)
    return pdirector.id


@db_session
def get_game_semaphore(gid) -> int:
    lobby = Lobby.get(id=gid)
    sem = lobby.game.semaphore
    return sem


@db_session
def get_game_score(gid) -> Score:
    lobby = Lobby.get(id=gid)
    card_pool = select(c for c in lobby.game.cards)

    bad_score = len(select(c for c in card_pool if c.proclaimed == True and c.phoenix == False))
    good_score = len(select(c for c in card_pool if c.proclaimed == True and c.phoenix == True))

    return Score(good=good_score, bad=bad_score)
