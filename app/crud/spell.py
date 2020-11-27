from app.crud.card import *
from app.crud.lobby import *
from app.crud.player import *

from app.schemas.game_schema import Role, PlayerRole
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


def cast_imperio(game_id: int, target: int):
    return


@db_session
def cast_crucio(game_id: int, target: int) -> PlayerRole:

    pr = None
    Player.get(id=target).crucied = True
    if Player.get(id=target).role.phoenix:
        pr = PlayerRole(role=Role.phoenix)
    if Player.get(id=target).role.voldemort:
        pr = PlayerRole(role=Role.voldemort)
    else:
        pr = PlayerRole(role=Role.eater)

    return pr

@db_session
def get_crucied_players(game_id: int) -> List[int]:

    cplayers = list(
        select(
            p for p in Player
                if p.lobby.id == game_id 
                    and p.crucied))
    return cplayers