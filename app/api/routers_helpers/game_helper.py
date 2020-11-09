from app.database.crud import *
from fastapi import HTTPException

from app.database.models import *
from app.api.schemas import *

from app.database.crud_helpers.player import *
from app.database.crud_helpers.lobby import *
from app.database.crud_helpers.card import *
from typing import List, Optional


# Gets player from game and returns its id or raises and exception
def get_player(email: str, game_id: int):
    player_id = get_player_id(email, game_id)
    if player_id == -1:
        raise HTTPException(status_code=409, detail='User not in Lobby/Game')
    return player_id


# Check if game is over
def is_game_over(game_id):
    score = get_game_score(game_id)
    return score.good == 5 or score.bad == 6


# Checks if minister can proclaim a card
def is_min_proc_time(game_id: int, player_id: int):
    return minister_chooses_proc(game_id) and get_is_player_minister(player_id)


# Checks if director or user can proclaim a card. It raises an exception on failure
# It returns true on success
def is_dir_proc_time(game_id: int, player_id: int):
    # check if it's time for a director to choose
    if not director_chooses_proc(game_id=game_id):
        raise HTTPException(status_code=401, detail='It\'s not time to choose')

    # check if the player is the director
    if not is_player_director(player_id=player_id):
        raise HTTPException(status_code=401, detail='Player isn\'nt director')
    return True


# Update the status of the card which position is election and its game is
# game_id
def minister_discards(election: int, game_id: int):
    # check if the card to discard is valid
    if election not in get_selected_cards_pos(game_id=game_id):
        raise HTTPException(
            status_code=401, detail='Illegal selection of cards')
    # update status of card
    discard_card(card_pos=election, game_id=game_id)


# Update the status of selected cards in the game specified by game_id
def director_proclaims(election: int, game_id: int):
    # check if the card to proclaim is valid
    if election not in set(get_selected_cards_pos(game_id=game_id)):
        raise HTTPException(
            status_code=401, detail='Illegal selection of cards')
    # update the status of the selected cards in the game
    proclaim_card(card_pos=election, game_id=game_id)


# Checks if the player can propose and if it's time to select a government
# Raises exception on failure
def can_propose_gvt(game_id: int, player_id: int):
    # check if the player is the minister
    if not get_game_minister_id(game_id) == player_id:
        raise HTTPException(
            status_code=409, detail='You are not the minister!')

    # check if it's time to propose a government
    if not goverment_proposal_needed(game_id):
        raise HTTPException(
            status_code=409, detail='It\'s not time to select a government')


# Checks
# Raises
def is_player_minister(player_id: int):
    if not get_is_player_minister(player_id=player_id):
        raise HTTPException(
            status_code=409, detail='You are not the minister!')


# Checks
# Raises
def in_casting_phase(game_id: int) -> bool:

    if in_legislative_session(game_id) and get_director_proclaimed(game_id) and get_last_proc_negative(game_id):
        raise HTTPException(
            status_code=409, detail='It\'s not time to cast a spell')


    