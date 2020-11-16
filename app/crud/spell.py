from app.crud.card import *


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


def cast_crucio(game_id: int, target: int):
    return
