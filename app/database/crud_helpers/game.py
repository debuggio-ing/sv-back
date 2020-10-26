from app.database.models import *
from app.api.schemas import *


# Return the required game status.
@db_session
def get_game_status(game_id: int) -> GamePublic:

    lobby = Lobby.get(id=game_id)
    game = lobby.game
    ans = GamePublic()
    return
