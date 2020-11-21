from app.models.game_models import *
from app.models.lobby_models import *
from app.schemas.game_schema import *


# add a message to the database
@db_session
def insert_message(player_id: int, message: str):
    player = Player.get(id=player_id)

    Message(sender=player, message=message)

    commit()


# return all messages from game/lobby.
@db_session
def get_messages(id: int):
    lobby = Lobby.get(id=id)

    msgs = list(
        select(
            m for m in Message if m.sender.lobby.id == id).order_by(
            lambda msg: desc(
                msg.id)).limit(6))

    messages = list(map(lambda x: MessageSchema(
        sender=x.sender.user.nickname, message=x.message), msgs))
    messages.reverse()

    return messages
