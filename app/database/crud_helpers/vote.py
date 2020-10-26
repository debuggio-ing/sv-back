from app.database.models import *
from app.api.schemas import *


@db_session
def currently_voting(game_id: int):
    lobby = Lobby.get(id=game_id)
    return lobby.game.voting


@db_session
def is_last_vote(player_id: int, game_id: int):

    lobby = Lobby.get(id=game_id)
    game = lobby.game
    player = Player.get(id=player_id)
    max_players = lobby.max_players

    current_votes = lobby.game.numv
    already_vote = CurrentVote.get(voter_id=player_id)

    if already_vote is None:
        current_votes += 1

    return current_votes == max_players


@db_session
def set_last_player_vote(player_id: int, game_id: int, vote: bool):
    set_player_vote(player_id, game_id, vote)
    update_public_vote(game_id)
    clean_current_vote(game_id)

    commit()


@db_session
def set_player_vote(player_id: int, game_id: int, vote: bool):
    player = Player.get(id=player_id, lobby=game_id)
    lobby = Lobby.get(id=game_id)
    game = lobby.game

    if player.curr_vote is None:
        player.curr_vote = CurrentVote(
            game=game, player=player, vote=vote, voter_id=player_id)
        lobby.game.numv += 1
    else:
        player.curr_vote.vote = vote

    commit()


@db_session
def update_public_vote(game_id: int):
    lobby = Lobby.get(id=game_id)
    game = lobby.game

    delete(v for v in PublicVote)

    votes = (select((v.vote, v.voter_id) for v in CurrentVote))[:]

    for v in votes:
        pv = PublicVote(game=game, vote=v[0], voter_id=v[1])

    lobby.game.voting = False
    commit()


@db_session
def clean_current_vote(game_id: int):

    lob = Lobby.get(id=game_id)

    delete(v for v in CurrentVote)

    lob.game.numv = 0

    commit()
