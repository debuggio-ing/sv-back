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


"""
dead players cant:
-chat
-vote
-be minister
-be director
-be target of spell

"""
# add dead/alive condition to the game logic
@db_session
def cast_avada_kedavra(game_id: int, target: int):

    tplayer = Player.get(id=target)

    # set player to dead
    tplayer.alive = False

    # check if voldemort is dead, then end the game
    if tplayer.role.voldemort:
        tplayer.game.ended = True

    commit()


def cast_imperio(game_id: int, target: int):
    return


#
def cast_crucio(game_id: int, target: int):
    return
