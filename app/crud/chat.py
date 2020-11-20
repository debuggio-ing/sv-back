from app.models.game_models import *
from app.models.lobby_models import *


@db_session
def insert_message(player_id: int, message: str):
    player = Player.get(id=player_id)

    Message(sender=player, message=message)

    commit()
