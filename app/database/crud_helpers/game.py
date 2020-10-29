from app.database.models import *
from app.api.schemas import *
from app.database.crud_helpers.player import *
from typing import List


# Create game in the database.
@db_sesion
def insert_game(lobby_id: int) -> int:
    lobby = Lobby.get(id=lobby_id)

    cards = list((i,i<6) for i in range(17))
    random.shuffle(cards)

    game_id = -1
    if lobby is not None:
        game = Game(semaphore=0, lobby=lobby, voting=False)

        for cards in cards:
            ProcCard(position=card[0], phoenix=card[1], game=game)

        commit()
        game_id = game.id

    return game_id


# Return the required game status.
@db_session
def get_game_public_info(gid):
    return GamePublic(id=gid,
            player_list=get_game_player_public_list(gid),
            minister=get_game_minister_id(gid),
            prev_minister=get_game_prev_minister_id(gid),
            director=get_game_director_id(gid),
            prev_director=get_game_prev_director_id(gid),
            semaphore=get_game_semaphore(gid),
            score=get_game_score(gid))


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
