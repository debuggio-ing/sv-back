from fastapi import APIRouter, HTTPException, Request, Depends, Response
from pydantic import BaseModel, Field, BaseSettings
from fastapi_jwt_auth import AuthJWT
from datetime import timedelta
from typing import Literal, Optional

from app.api.schemas import *
from app.database.models import *
from app.database.crud import *

r = games_router = APIRouter()


# List games in database
@r.get("/games/")
def get_game_list(
    game_from: Optional[int] = 0,
    game_to: Optional[int] = None, Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    game_id_list = get_all_games_ids(game_from, game_to)
    games = []
    for gid in game_id_list:
        game = GamePublic(id=gid,
                        player_list=get_game_player_public_list(gid),
                        minister=get_game_minister_id(gid),
                        prev_minister=get_game_prev_minister_id(gid),
                        director=get_game_director_id(gid),
                        prev_director=get_game_prev_director_id(gid),
                        semaphore=get_game_semaphore(gid),
                        score=get_game_score(gid))
        games.append(game)

    return games


# View public data about a specified game
@r.get("/games/{game_id}/", response_model=GamePublic)
def get_game(game_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return get_game_public_info(game_id)


# Player vote in game
@r.post("/games/{game_id}/vote/")
def player_vote(game_id: int, vote: PlayerVote, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    # get user's email
    user_email = Authorize.get_jwt_identity()
    if user_email == None:
        raise HTTPException(status_code=409, detail='Corrupted JWT')

    # get the id of the user in the game (the player_id)
    player_id = get_player_id(user_email, game_id)
    if player_id == -1:
        raise HTTPException(status_code=401, detail='User not in game or game id incorrect')


    # check if there's a vote ocurring in the game
    if not currently_voting(game_id):
        raise HTTPException(
            status_code=403, detail='There isn\'t a vote ocurring')

    # Check if player is Alive
    # TO-DO


    # cast vote
    if is_last_vote(player_id, game_id):
        set_last_player_vote(player_id, game_id, vote.vote)
    else:
        set_player_vote(player_id, game_id, vote.vote)
    return


# Return player's role in the specified game
@r.get("/games/{game_id}/role/", response_model=PlayerRole)
def get_player_role(game_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return


# Cast spell in specified game
@r.post("/games/{game_id}/spell/")
def cast_spell(game_id: int, spell: CastSpell, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return


# Return minister's proclamation cards
@r.get("/games/{game_id}/proc/", response_model=LegislativeSession)
def get_minister_proc(game_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return


# Select cards to proclaim in the specified game
@r.post("/games/{game_id}/proc/")
def proc_election(
        game_id: int,
        election: LegislativeSession,
        Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return


# Nominate director in specified game
@r.post("/games/{game_id}/director/")
def director_candidate(
        game_id: int,
        candidate: ProposedDirector,
        Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    # get user's email
    user_email = Authorize.get_jwt_identity()
    if user_email == None:
        raise HTTPException(status_code=409, detail='Corrupted JWT')

    #Esta en el juego?
    pid = get_player_id(user_email, game_id)
    if pid == -1:
        raise HTTPException(status_code=401, detail='User not in game or game id incorrect')

    #Es el ministro?
    if not get_game_minister_id(game_id) == pid:
        raise HTTPException(status_code=409, detail='You are not the minister!')

    #Es hora de elegir gobierno?
    if not goverment_proposal_needed(game_id):
        raise HTTPException(status_code=409, detail='No es momento de proponer director')

    propose_goverment(game_id, candidate.player)

    return
