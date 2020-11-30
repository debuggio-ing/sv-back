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
        tplayer.lobby.game.ended = True
        tplayer.lobby.game.phoenix_win = True
        print("GAME OVER, Phoenix won? {}".format(game.phoenix_win))

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


@db_session
def cast_crucio(game_id: int, target: int):
    game = Lobby.get(id=game_id).game
    if game.in_crucio:
        game.in_crucio = False
        game.last_tortured = -1
    else:
        game.in_crucio = True
        Player.get(id=target).crucied = True
        game.last_tortured = target
    commit()


# Returns the role of the last target in the game
@db_session
def torture_player(game_id: int):
    game = Lobby.get(id=game_id).game
    target = game.last_tortured
    player_role = None
    if game.in_crucio:
        if Player.get(id=target).role.phoenix:
            player_role = Role.phoenix
        else:
            player_role = Role.eater
    return player_role
