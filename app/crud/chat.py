from app.models.game_models import *
from app.models.lobby_models import *


# add a message to the database
@db_session
def insert_message(player_id: int, message: str):
    player = Player.get(id=player_id)

    Message(sender=player, message=message)

    commit()


# return all game_id messages.
@db_session
def get_game_messages(game_id: int):
    lobby = Lobby.get(id=game_id)

    messages = list(select(m for m in Message if m.game.lobby.id == game_id))

    print(messages)

    return messages


# return all lobby_id messages.
@db_session
def get_lobby_messages(lobby_id: int):
    lobby = Lobby.get(id=lobby_id)

    messages = list(
        select(
            m.message for m in Message if m.sender.lobby.id == lobby_id))

    print(messages)

    return messages
