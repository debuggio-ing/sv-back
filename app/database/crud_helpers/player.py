from app.database.models import *
from app.api.schemas import *


# Create player in the database.
@db_session
def insert_player(user_email: str, lobby_id: int) -> int:
    lobby = Lobby.get(id=lobby_id)
    user = User.get(email=user_email)

    player_id = -1
    if lobby is not None and user not in lobby.player.user:
        p = Player(user=user, lobby=lobby)
        commit()
        player_id = p.id

    return player_id

@db_session
def get_player_vote_status(pid: int) -> bool:

    pl = Player.get(id=pid)
    return pl.curr_vote is not None

@db_session
def get_player_last_vote(pid: int) -> bool:
    pl = Player.get(id=pid)
    return pl.pub_vote.vote


# Return the required player status.
@db_session
def get_player_public(pid: int) -> PlayerPublic:
    player = Player.get(id=pid)

    pp = PlayerPublic(player_id=pid,
                    alive=player.alive,
                    voted=get_player_vote_status(pid),
                    last_vote=get_player_last_vote(pid),
                    username=player.user.username)
    return pp


# Return the required player id.
@db_session
def get_player_id(user_email: str, game_id: int) -> int:
    user = User.get(email=user_email)
    lobby = Lobby.get(id=game_id)

    player = Player.get(user=user, lobby=lobby)

    # If there's no player with user_email in game_id,
    # it returns default the value.
    pid = -1
    if player is not None:
        pid = player.id

    return pid
