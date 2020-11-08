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
    PROC_CARD_NUMBER = 17
    # This number is hidden and therefore its random
    ULTRA_RANDOM_NUMBER = random.randint(0, 4)

    lobby = Lobby.get(id=lobby_id)

    MAX_PLAYERS = lobby.max_players

    player_order = [i for i in range(MAX_PLAYERS)]
    random.shuffle(player_order)

    cards = list((i, i < NUM_PHOENIX_CARDS) for i in range(PROC_CARD_NUMBER))
    random.shuffle(cards)

    game_id = -1
    if lobby is not None:
        game = Game(lobby=lobby)

        player_ids = get_lobby_players_id(lobby.id)

        # Set player order
        for i, pid in enumerate(player_ids):
            player = Player.get(id=pid)
            player.position = player_order[i]

        # Set first player of the list
        game.list_head = ULTRA_RANDOM_NUMBER

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
        set_minister_of_magic(player_ids[ULTRA_RANDOM_NUMBER])
        game.list_head = ((game.list_head + 1) % MAX_PLAYERS)

        commit()
        game_id = game.id

    return game_id


# Return the required game status.
@db_session
def get_game_public_info(gid: int, pid: int):
    return GamePublic(id=gid,
                      player_list=get_game_player_public_list(gid, pid),
                      minister=get_game_minister_id(gid),
                      prev_minister=get_game_prev_minister_id(gid),
                      director=get_game_director_id(gid),
                      prev_director=get_game_prev_director_id(gid),
                      semaphore=get_game_semaphore(gid),
                      score=get_game_score(gid),
                      voting=get_game_voting(gid),
                      in_session=get_game_in_session(gid),
                      minister_proclaimed=get_game_minister_proclaimed(gid),
                      client_minister=is_player_minister(pid),
                      client_director=is_player_director(pid)
                      )


# Returns true if pid is minister.
@db_session
def is_player_minister(player_id: int) -> bool:
    return Player.get(id=player_id).minister


# Returns true if pid is director.
@db_session
def is_player_director(player_id: int) -> bool:
    return Player.get(id=player_id).director


# Returns all game's ids
@db_session
def get_all_games_ids(game_from: int, game_to: int) -> List[int]:
    return list(select(g.id for g in Game))


# Return a list of all players in gid game with the information of concern to c_pid (callers_player_id).
@db_session
def get_game_player_public_list(gid: int, c_pid: int) -> List[PlayerPublic]:
    pid_list = list(select(
        p.id for p in Player if gid == p.lobby.id))

    players = [get_player_public(pid, c_pid) for pid in pid_list]

    return players


# Returns the id of the game's minister.
@db_session
def get_game_minister_id(gid: int) -> int:
    minister = Player.get(lobby=gid, minister=True)

    minister_id = -1
    if minister is not None:
        minister_id = minister.id

    return minister_id


# Returns the id of the game's director.
@db_session
def get_game_director_id(gid: int) -> int:
    director = Player.get(lobby=gid, director=True)

    director_id = -1
    if director is not None:
        director_id = director.id

    return director_id


# Returns the id of the game's previous minister.
@db_session
def get_game_prev_minister_id(gid: int) -> int:
    prev_minister = Player.get(lobby=gid, prev_minister=True)

    prev_minister_id = -1
    if prev_minister is not None:
        prev_minister_id = prev_minister.id

    return prev_minister_id


# Get previous director's player_id
@db_session
def get_game_prev_director_id(gid: int) -> int:
    prev_director = Player.get(lobby=gid, prev_director=True)

    prev_director_id = -1
    if prev_director is not None:
        prev_director_id = prev_director.id

    return prev_director_id


# Get game's semaphore
@db_session
def get_game_semaphore(gid: int) -> int:
    lobby = Lobby.get(id=gid)

    sem = -1
    if lobby is not None and lobby.game is not None:
        sem = lobby.game.semaphore

    return sem


# Check if the game is in election
@db_session
def get_game_voting(gid) -> bool:
    game = Lobby.get(id=gid).game

    ans = False
    if game is not None:
        ans = game.voting

    return ans


# Check if game is in legislative session
@db_session
def get_game_in_session(gid) -> bool:
    game = Lobby.get(id=gid).game

    ans = False
    if game is not None:
        ans = game.in_session

    return ans


# Check if the minister has already proclaimed cards
@db_session
def get_game_minister_proclaimed(gid) -> bool:
    game = Lobby.get(id=gid).game

    ans = False
    if game is not None:
        ans = game.minister_proclaimed

    return ans


# Get game's total proclaimed cards (phoenix = good, death eaters = bad)
@db_session
def get_game_score(gid: int) -> Score:
    lobby = Lobby.get(id=gid)

    bad_score = 0
    good_score = 0
    if lobby is not None and lobby.game is not None:
        card_pool = select(c for c in lobby.game.cards)

        bad_score = len(
            select(
                c for c in card_pool if c.proclaimed and c.phoenix == False))
        good_score = len(
            select(
                c for c in card_pool if c.proclaimed and c.phoenix))

    return Score(good=good_score, bad=bad_score)


# Check if it's time for a government proposal
@db_session
def goverment_proposal_needed(gid: int) -> bool:
    game = Lobby.get(id=gid).game
    return not game.voting and not game.in_session


# Purpose a director specified by the user id dir_id
@db_session
def propose_government(game_id: int, dir_id: int):
    lobby = Lobby.get(id=game_id)

    old_dir_id = get_game_director_id(gid=game_id)
    old_dir = Player.get(id=old_dir_id)

    if old_dir is not None:
        old_dir.director = False

    player = Player.get(id=dir_id)
    player.director = True
    lobby.game.voting = True

    commit()


# Finish the current legislative session
@db_session
def finish_legislative_session(game_id: int):
    game = Game.get(id=game_id)
    game.in_session = False
    game.minister_proclaimed = False
    set_next_minister_candidate(game_id)
    cards = list(select(c for c in ProcCard if c.game.id == game_id))
    if len(cards.filter(lambda c: not(c.proclaimed and c.discarded))) <= 2:
        shuffle_cards(game_id)
    commit()


# Updates the status of the game after the minister discards a card
@db_session
def finish_minister_proclamation(game_id: int):
    game = Game.get(id=game_id)
    game.minister_proclaimed = True
    commit()
