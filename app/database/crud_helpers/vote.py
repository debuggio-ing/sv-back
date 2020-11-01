from app.database.models import *
from app.api.schemas import *

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

    if already_vote is None:
        current_votes += 1

    return current_votes == max_players


# Casts the last players' vote
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
    player = Player.get(id=player_id, lobby=game_id)
    lobby = Lobby.get(id=game_id)
    game = lobby.game

    if player.curr_vote is None:
        player.curr_vote = CurrentVote(
            game=game, player=player, vote=vote, voter_id=player_id)
        lobby.game.num_votes += 1
    else:
        player.curr_vote.vote = vote

    commit()


# Updates the result of the election and set the voting fase to False
@db_session
def update_public_vote(game_id: int):
    lobby = Lobby.get(id=game_id)
    game = lobby.game

    delete(v for v in PublicVote if v.game.id == game_id)

    votes = (select((v.vote, v.voter_id) for v in CurrentVote if v.game.id == game_id))[:]

    for v in votes:
        player = Player.get(id=v[1])
        pv = PublicVote(game=game, vote=v[0], voter_id=v[1], player=player)

    commit()

#
@db_session
def process_vote_result(gid: int):

    game = Lobby.get(id=gid).game
    max_players = Lobby.get(id=gid).max_players
    
    result = len(select(v for v in PublicVote if v.game.id == gid and v.vote == True))
    if result < math.ceil((max_players+1)/2):
        set_next_minister_candidate(gid)
        game.semaphore +=1
    else:
        game.in_session = True
    game.voting = False


@db_session
def set_next_minister_candidate(gid: int):
    lobby = Lobby.get(id=gid)
    #me deberia fijar q no sea none dsp
    ex_minister = Player.get(lobby=lobby, minister=True)
    ex_minister.minister = False

    #tmb deberia chequear por errores
    new_minister = Player.get(lobby=lobby, position=lobby.game.list_head)
    new_minister.minister = True

    #actualizar la cabeza de la lista
    lobby.game.list_head = (lobby.game.list_head+1)%lobby.max_players

# Deletes every entry in the current vote
@db_session
def clean_current_vote(game_id: int):

    lob = Lobby.get(id=game_id)

    delete(v for v in CurrentVote if v.game.id == game_id)

    lob.game.num_votes = 0

    commit()
