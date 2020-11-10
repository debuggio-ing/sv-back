from app.database.models import *

from app.database.crud import *
from fastapi import HTTPException

from app.database.models import *
from app.api.schemas import *

from app.database.crud_helpers.player import *
from app.database.crud_helpers.lobby import *
from app.database.crud_helpers.card import *
from typing import List, Optional
#


#
def cast_spell(game_id: int, target: Optional[int]):
    negative_procs = get_number_neg_procs(game_id=game_id)
    number_players = get_number_players(game_id=game_id)

    if number_players in [5, 6] and negative_procs == 3:
        cast_divination(game_id=game_id)
    elif negative_procs > 3:
        cast_avada_kedavra(game_id=game_id, target=target)

    discharge_director(player_id=player_id)
    finish_legislative_session(game_id)


#
# add dead/alive condition to the game logic
def cast_avada_kedavra(game_id: int, target: Optional[int]):

    # check if avada kedavra

    # set player to dead

    # check if voldemort is dead, then end the game

    # set next minister candidate

    # set in_session a false

    # update game status and card deck

    #


def cast_imperio(game_id: int, target: int):
    return


#
def cast_crucio(game_id: int, target: int):
    return


#
def cast_divination(game_id: int):
    return
