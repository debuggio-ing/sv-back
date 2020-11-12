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


#
# add dead/alive condition to the game logic
def cast_avada_kedavra(game_id: int, target: Optional[int]):
    pass

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
