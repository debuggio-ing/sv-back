from app.models.user_models import *
from app.models.game_models import *
from app.models.lobby_models import *
from app.schemas.game_schema import *

import math


# Checks if the game has a vote ocurring
@db_session
def currently_voting(game_id: int):
    lobby = Lobby.get(id=game_id)
    return lobby.game.voting


# Checks if the vote about to cast is the last vote
@db_session
def is_last_vote(player_id: int, game_id: int):
    lobby = Lobby.get(id=game_id)
    game = lobby.game
    player = Player.get(id=player_id)
    max_players = lobby.max_players

    current_votes = lobby.game.num_votes
    already_vote = CurrentVote.get(voter_id=player_id)
    dead_players = lobby.game.dead_players

    if already_vote is None:
        current_votes += 1

    return current_votes == (max_players - dead_players)


# DO NOT USE: fix database for demo.
@db_session
def demo_database(game_id: int):
    assigned = 0
    pos = 3
    lobby = Lobby.get(id=game_id)
    while assigned < 2 and pos <= 17:
        card = ProcCard.get(position=pos, game=lobby.game.id)
        if not card.proclaimed:
            card.selected = True
            assigned += 1
        pos += 1

    lobby.game.minister_proclaimed = True

    commit()


# Casts last player's vote
@db_session
def set_last_player_vote(player_id: int, game_id: int, vote: bool):
    set_player_vote(player_id, game_id, vote)

    update_public_vote(game_id)
    process_vote_result(game_id)
    clean_current_vote(game_id)

    commit()


# Cast a player's vote
@db_session
def set_player_vote(player_id: int, game_id: int, vote: bool):

    lobby = Lobby.get(id=game_id)
    cv = CurrentVote.get(player=player_id, game=game_id)
    if cv is None:
        CurrentVote(game=game_id, player=player_id,
                    vote=vote, voter_id=player_id)
        lobby.game.num_votes += 1
    else:
        cv.vote = vote

    commit()


# Updates the result of the election and set the voting fase to False
@db_session
def update_public_vote(game_id: int):
    lobby = Lobby.get(id=game_id)
    game = lobby.game

    delete(v for v in PublicVote if v.game == game_id)

    votes = (select((v.vote, v.voter_id)
                    for v in CurrentVote if v.game == game_id))[:]

    for v in votes:
        player = Player.get(id=v[1])
        pv = PublicVote(
            game=game_id, vote=v[0], voter_id=v[1], player=player.id)

    commit()


@db_session
def unleash_chaos(game_id: int):
    card = select(
        c for c in ProcCard if c.game.lobby.id == game_id and not(
            c.proclaimed or c.discarded)).order_by(
        lambda c: c.position).limit(1)[0]
    card.proclaimed = True

# Set voting results.


@db_session
def process_vote_result(game_id: int):
    lobby = Lobby.get(id=game_id)
    game = lobby.game
    max_players = lobby.max_players

    result = len(
        select(v for v in PublicVote if v.game == game_id and v.vote))
    if result < math.ceil((max_players + 1) / 2):
        set_next_minister_candidate(game_id)
        if(game.semaphore == 3):
            unleash_chaos(game_id)
        game.semaphore = (game.semaphore + 1) % 4
        dir = Player.get(lobby=lobby, director=True)
        dir.director = False
    else:
        game.in_session = True
        # select cards for legislative session
        cards = list(
            select(
                c for c in ProcCard if c.game.lobby.id == game_id and not (
                    c.proclaimed or c.discarded)).order_by(
                lambda c: c.position).limit(3))
        for c in cards:
            c.selected = True

    game.voting = False
    commit()


# Set next minister as candidate in gid game.
@db_session
def set_next_minister_candidate(gid: int):
    lobby = Lobby.get(id=gid)

    discharge_former_minister(game_id=gid)
    # set new minister
    new_minister = Player.get(lobby=lobby, position=lobby.game.list_head)

    while new_minister is None or not new_minister.alive:
        lobby.game.list_head = (lobby.game.list_head + 1) % lobby.max_players
        new_minister = Player.get(lobby=lobby, position=lobby.game.list_head)

    new_minister.minister = True
    # update list head
    lobby.game.list_head = (lobby.game.list_head + 1) % lobby.max_players

    commit()


@db_session
def discharge_former_minister(game_id: int):

    lobby = Lobby.get(id=game_id)
    # discharge former minister
    ex_minister = Player.get(lobby=lobby, minister=True)
    if ex_minister is not None:
        ex_minister.minister = False

    commit()

# Deletes every entry in the current vote


@db_session
def clean_current_vote(game_id: int):

    lob = Lobby.get(id=game_id)

    delete(v for v in CurrentVote if v.game == game_id)

    lob.game.num_votes = 0

    commit()
