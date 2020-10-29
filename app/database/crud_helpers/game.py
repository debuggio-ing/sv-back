from app.database.models import *
from app.api.schemas import *
from app.database.crud_helpers.player import *
from app.database.crud_helpers.lobby import *
from typing import List
import random


# Create game in the database.
@db_session
def insert_game(lobby_id: int) -> int:
    NUMBER_OF_DEATH_EATERS = 2
    NUMBER_OF_PHOENIX_CARDS = 6

    lobby = Lobby.get(id=lobby_id)

    cards = list((i, i < NUMBER_OF_PHOENIX_CARDS) for i in range(17))
    random.shuffle(cards)

    game_id = -1
    if lobby is not None:
        game = Game(semaphore=0, lobby=lobby, voting=False)

        # create proclamation cards.
        for card in cards:
            ProcCard(position=card[0], phoenix=card[1], game=game)

        players = get_lobby_players_id(lobby.id)

        # choose who will be voldemort and death eaters.
        voldemort = random.randint(0, len(players) - 1)
        death_eaters = random.sample(
            range(len(players)), NUMBER_OF_DEATH_EATERS)

        # set roles.
        set_voldemort(players[voldemort])
        set_death_eaters(list(players[i] for i in death_eaters))
        set_phoenixes([p for p in list(range(len(players)))
                       if p not in death_eaters])

        # set first minister of magic.
        set_minister_of_magic(players[0])

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

    minister_id = -1
    if minister is not None:
        minister_id = minister.id

    return minister_id


@db_session
def get_game_director_id(gid) -> int:
    director = Player.get(lobby=gid, director=True)

    director_id = -1
    if director is not None:
        director_id = director.id

    return director_id


@db_session
def get_game_prev_minister_id(gid) -> int:
    prev_minister = Player.get(lobby=gid, prev_minister=True)

    prev_minister_id = -1
    if prev_minister is not None:
        prev_minister_id = prev_minister.id

    return prev_minister_id


@db_session
def get_game_prev_director_id(gid) -> int:
    prev_director = Player.get(lobby=gid, prev_director=True)

    prev_director_id = -1
    if prev_director is not None:
        prev_director_id = prev_director_id.id

    return prev_director_id


@db_session
def get_game_semaphore(gid) -> int:
    lobby = Lobby.get(id=gid)

    sem = -1
    if lobby is not None and lobby.game is not None:
        sem = lobby.game.semaphore

    return sem


@db_session
def get_game_score(gid) -> Score:
    lobby = Lobby.get(id=gid)
    card_pool = select(c for c in lobby.game.cards)

    bad_score = len(
        select(
            c for c in card_pool if c.proclaimed and c.phoenix == False))
    good_score = len(
        select(
            c for c in card_pool if c.proclaimed and c.phoenix))

    return Score(good=good_score, bad=bad_score)
