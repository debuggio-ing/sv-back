from app.crud.card import *
from app.crud.vote import *
from app.crud.game import *

# add dead/alive condition to the game logic


@db_session
def cast_avada_kedavra(game_id: int, target: int):
    tplayer = Player.get(id=target)
    lobby = Lobby.get(id=game_id)

    # set player to dead
    tplayer.alive = False

    lobby.game.dead_players += 1

    # check if voldemort is dead, then end the game
    if tplayer.role.voldemort:
        tplayer.game.ended = True

    commit()
    return 1

# Sets next minister candidate without modifying the correct order of
# candidates


@db_session
def cast_imperio(game_id: int, target: int):
    lobby = Lobby.get(id=game_id)
    minister_id = get_game_minister_id(game_id=game_id)
    if minister_id == target:
        return -1
    discharge_former_minister(game_id=game_id)
    new_minister = Player.get(id=target)
    new_minister.minister = True
    commit()
    return 1


def cast_crucio(game_id: int, target: int):
    return
