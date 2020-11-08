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
    user_email = Authorize.get_jwt_identity()
    if user_email == None:
        raise HTTPException(status_code=409, detail='Corrupted JWT')

    game_id_list = get_all_games_ids(game_from, game_to)
    games = []
    for gid in game_id_list:
        pid = get_player_id(user_email, gid)
        game = get_game_public_info(gid, pid)
        games.append(game)

    return games


# View public data about a specified game
@r.get("/games/{game_id}/", response_model=GamePublic)
def get_game(game_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    # get user's email
    user_email = Authorize.get_jwt_identity()
    if user_email == None:
        raise HTTPException(status_code=409, detail='Corrupted JWT')

    # get the id of the user in the game (the player_id)
    player_id = get_player_id(user_email, game_id)

    return get_game_public_info(gid=game_id, pid=player_id)


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
        raise HTTPException(
            status_code=401, detail='User not in game or game id incorrect')

    # check if there's a vote ocurring in the game
    if not currently_voting(game_id):
        raise HTTPException(
            status_code=403, detail='There isn\'t a vote ocurring')

    # cast vote
    if is_last_vote(player_id, game_id):
        set_last_player_vote(player_id, game_id, vote.vote)
    else:
        set_player_vote(player_id, game_id, vote.vote)
    return 1


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


# Return to the director the cards selected by the minister
@r.get("/games/{game_id}/dir/proc/")
def get_director_proc(game_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    # get user's email
    user_email = Authorize.get_jwt_identity()
    if user_email == None:
        raise HTTPException(status_code=409, detail='Corrupted JWT')

    # get the id of the user in the game
    player_id = get_player_id(user_email, game_id)
    if player_id == -1:
        raise HTTPException(status_code=401, detail='User not in game')

    # check if it's time for a director to choose
    if not director_chooses_proc(game_id):
        raise HTTPException(status_code=401, detail='It\'s not time to choose')

    # check if the player is the director
    if not is_director(player_id):
        raise HTTPException(status_code=401, detail='Player isn\'nt director')

    # get the cards selected by the minister
    selected_cards = get_selected_cards(game_id)
    cards = []
    for card in selected_cards:
        cards.append(CardToProclaim(
            card_pos=card.position, phoenix=card.phoenix))

    return cards


# Director chooses the cards to proclaim
# At this point expelliarmus is not implemented
# Returns True if game continues or False if game is over
@r.post("/games/{game_id}/dir/proc/", response_model=bool)
def proc_election(
        game_id: int,
        election: LegislativeSession,
        Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    # get user's email
    user_email = Authorize.get_jwt_identity()
    if user_email == None:
        raise HTTPException(status_code=409, detail='Corrupted JWT')

    # get the id of the user in the game
    player_id = get_player_id(user_email=user_email, game_id=game_id)
    if player_id == -1:
        raise HTTPException(status_code=401, detail='User not in game')

    # check if it's time for a director to choose
    if not director_chooses_proc(game_id):
        raise HTTPException(status_code=401, detail='It\'s not time to choose')

    # check if the player is the director
    if not is_director(player_id):
        raise HTTPException(status_code=401, detail='Player isn\'nt director')

    # check if the received proclamation is valid
    proclamation_count = sum(
        map(lambda c: c.to_proclaim, election.proclamation))
    if proclamation_count != 1 or len(election.proclamation) != 2:
        raise HTTPException(
            status_code=401, detail='Invalid selection of cards')

    # proclaim card if it's not proclaimed
    if proclaim_card(election.proclamation, game_id) == False:
        raise HTTPException(
            status_code=401, detail='Invalid selection of cards')

    # finish legislative session and release the director
    finish_legislative_session(game_id)
    discharge_director(player_id)

    # check if game is over
    score = get_game_score(game_id)

    return score.good == 5 or score.bad == 6


# Nominate director in specified game
@r.post("/games/{game_id}/director/{candidate_id}/")
def director_candidate(
        game_id: int,
        candidate_id: int,
        Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    # get user's email
    user_email = Authorize.get_jwt_identity()
    if user_email == None:
        raise HTTPException(status_code=409, detail='Corrupted JWT')

    # Esta en el juego?
    pid = get_player_id(user_email, game_id)
    if pid == -1:
        raise HTTPException(
            status_code=401, detail='User not in game or game id incorrect')

    # Es el ministro?
    if not get_game_minister_id(game_id) == pid:
        raise HTTPException(
            status_code=409, detail='You are not the minister!')

    # Es hora de elegir gobierno?
    if not goverment_proposal_needed(game_id):
        raise HTTPException(
            status_code=409, detail='No es momento de proponer director')

    propose_goverment(game_id, candidate_id)

    return
