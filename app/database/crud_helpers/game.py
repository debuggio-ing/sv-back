from app.database.models import *
from app.api.schemas import *
from app.database.crud_helpers.player import *
from app.database.crud_helpers.lobby import *
from typing import List
import random


# Create game in the database.
@db_session
def insert_game(lobby_id: int) -> int:
    NUM_DEATH_EATERS = 2
    NUM_PHOENIX_CARDS = 6

    lobby = Lobby.get(id=lobby_id)

    MAX_PLAYERS = lobby.max_players 

    player_order = [i for i in range(MAX_PLAYERS)]
    random.shuffle(player_order)

    cards = list((i, i < NUM_PHOENIX_CARDS) for i in range(17))
    random.shuffle(cards)

    game_id = -1
    if lobby is not None:
        game = Game(lobby=lobby)

        player_ids = get_lobby_players_id(lobby.id)

        #Set player order
        for i, pid in enumerate(player_ids):
            player = Player.get(id=pid)
            player.position = player_order[i]

        #Set first player of the list
        game.list_head = 2 #yo considero que el 2 es random

        # create proclamation cards.
        for card in cards:
            ProcCard(position=card[0], phoenix=card[1], game=game)


        # choose who will be and death eaters.
        death_eaters = random.sample(range(len(player_ids)), NUM_DEATH_EATERS)

        # set roles.
        set_phoenixes([player_ids[i]
                       for i in range(len(player_ids)) if i not in death_eaters])
        set_death_eaters(list(player_ids[i] for i in death_eaters[1:]))
        set_voldemort(player_ids[death_eaters[0]])

        # set first minister of magic.
        set_minister_of_magic(player_ids[2])
        game.list_head = ((game.list_head+1)%MAX_PLAYERS)

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
                      score=get_game_score(gid),
                      voting=get_game_voting(gid),
                      in_session=get_game_in_session(gid),
                      minister_proclaimed=get_game_minister_proclaimed(gid)
                      )



@db_session
def get_all_games_ids(game_from: int, game_to: int) -> List[int]:
    return list(select(g.id for g in Game))


@db_session
def get_game_player_public_list(gid: int) -> List[PlayerPublic]:
    pid_list = list(select(
        p.id for p in Player if gid == p.lobby.id))

    players = [get_player_public(pid) for pid in pid_list]

    return players


@db_session
def get_game_minister_id(gid: int) -> int:
    minister = Player.get(lobby=gid, minister=True)

    minister_id = -1
    if minister is not None:
        minister_id = minister.id

    return minister_id


@db_session
def get_game_director_id(gid: int) -> int:
    director = Player.get(lobby=gid, director=True)

    director_id = -1
    if director is not None:
        director_id = director.id

    return director_id


@db_session
def get_game_prev_minister_id(gid: int) -> int:
    prev_minister = Player.get(lobby=gid, prev_minister=True)

    prev_minister_id = -1
    if prev_minister is not None:
        prev_minister_id = prev_minister.id

    return prev_minister_id


@db_session
def get_game_prev_director_id(gid: int) -> int:
    prev_director = Player.get(lobby=gid, prev_director=True)

    prev_director_id = -1
    if prev_director is not None:
        prev_director_id = prev_director.id

    return prev_director_id


@db_session
def get_game_semaphore(gid: int) -> int:
    lobby = Lobby.get(id=gid)

    sem = -1
    if lobby is not None and lobby.game is not None:
        sem = lobby.game.semaphore

    return sem

@db_session
def get_game_voting(gid) -> bool:
    game = Lobby.get(id=gid).game

    ans = -1
    if game is not None:
        ans = game.voting

    return ans


@db_session
def get_game_in_session(gid) -> bool:
    game = Lobby.get(id=gid).game

    ans = -1
    if game is not None:
        ans = game.in_session

    return ans


@db_session
def get_game_minister_proclaimed(gid) -> bool:
    game = Lobby.get(id=gid).game

    ans = -1
    if game is not None:
        ans = game.minister_proclaimed

    return ans

@db_session
def get_game_score(gid: int) -> Score:
    lobby = Lobby.get(id=gid)
    card_pool = select(c for c in lobby.game.cards)

    bad_score = len(
        select(
            c for c in card_pool if c.proclaimed and c.phoenix == False))
    good_score = len(
        select(
            c for c in card_pool if c.proclaimed and c.phoenix))

    return Score(good=good_score, bad=bad_score)


@db_session
def goverment_proposal_needed(gid: int) -> bool:
    game = Lobby.get(id=gid).game    
    return not game.voting and not game.in_session

@db_session
def propose_goverment(gid: int, dir_id: int):
    lobby = Lobby.get(id=gid)

    player = Player.get(id=dir_id)
    player.director = True
    lobby.game.voting = True
