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
    player = Player.get(id=pid)

    vote = False
    if player is not None and player.pub_vote is not None:
        vote = player.pub_vote.vote

    return vote


# Return the required player status.
@db_session
def get_player_public(pid: int) -> PlayerPublic:
    player = Player.get(id=pid)

    pp = PlayerPublic(player_id=pid,
                      alive=player.alive,
                      voted=get_player_vote_status(pid),
                      last_vote=get_player_last_vote(pid),
                      username=player.user.username,
                      position=player.position)
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


# Set player role as voldemort
@db_session
def set_voldemort(player_id: int):
    player = Player.get(id=player_id)

    if player is not None:
        role = GRole(voldemort=True, phoenix=False)
        player.role = role
        commit()


# Set players roles as death eaters
@db_session
def set_death_eaters(players: List[int]):
    role = GRole(voldemort=False, phoenix=False)

    for player_id in players:
        player = Player.get(id=player_id)

        if player is not None:
            player.role = role

    commit()


# Set players roles as phoenixes
@db_session
def set_phoenixes(players: List[int]):
    role = GRole(voldemort=False, phoenix=True)

    for player_id in players:
        player = Player.get(id=player_id)

        if player is not None:
            player.role = role

    commit()


# Set player as minister of magic
@db_session
def set_minister_of_magic(player_id: int):
    player = Player.get(id=player_id)

    if player is not None:
        player.minister = True

    commit()


# Return player_id player role.
@db_session
def get_player_id_role(player_id: int) -> (bool, bool):
    player = Player.get(id=player_id)

    voldemort = phoenix = False
    if player is not None and player.role is not None:
        voldemort = player.role.voldemort
        phoenix = player.role.phoenix

    return (voldemort, phoenix)


# Check if the player identified by player_id is the director
@db_session
def is_director(player_id: int) -> bool:
    return Player.get(id=player_id).director


# Check if it's time for the director to choose a proclamation card
@db_session
def director_chooses_proc(game_id):
    lobby = Lobby.get(id=game_id)
    game = lobby.game
    return game and game.in_session and game.minister_proclaimed


# Discharge director
@db_session
def discharge_director(player_id):
    Player.get(id=player_id).director = False
    commit()