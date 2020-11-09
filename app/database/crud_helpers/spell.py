from app.database.models import *

#
def in_casting_phase(game_id: int) -> bool:

    return in_legislative_session(game_id) and
                get_director_proclaimed(game_id) and
                get_last_proc_negative(game_id)


# Check if game in legislative session
def in_legislative_session(game_id) -> bool:
    game = Lobby.get(id=game_id).game
    return game.in_session


# Check if game in legislative session
def get_director_proclaimed(game_id) -> bool:
    game = Lobby.get(id=game_id).game
    return game.director_proclaimed


# Check if game in legislative session
def get_last_proc_negative(game_id) -> bool:
    game = Lobby.get(id=game_id).game
    return game.last_proc_negative


# 
def is_target_correct(game_id=game_id, target=spell.target)


#
def cast_spell(game_id: int, spell: str, target: int):
    if spell == "Avada Kedravra":
        cast_avada_kedavra(game_id=game_id)
    elif spell == "Crucio":
        cast_crucio(game_id=game_id)
    elif spell == "Divination":
        cast_divination(game_id=game_id)
    elif spell == "Imperio":
        cast_imperio(game_id=game_id)
    

#
def cast_avada_kedavra(game_id: int, target: int):

    #check if avada kedavra

    #set player to dead

    #check if voldemort is dead, then end the game

    #set next minister candidate

    #set in_session a false

    # update game status and card deck
    discharge_director(player_id=player_id)
    finish_legislative_session(game_id)


#
def cast_imperio(game_id: int, target: int):
    return


#
def cast_crucio(game_id: int, target: int):
    return


#
def cast_divination(game_id: int):
    return