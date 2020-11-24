from app.crud.vote import *
from app.validators.constants import *


# Create player in the database.
@db_session
def insert_player(user_email: str, lobby_id: int) -> int:
    lobby = Lobby.get(id=lobby_id)
    user = User.get(email=user_email)
    existing_player = Player.get(lobby=lobby_id, user=user)
    player_id = -1
    if existing_player:
        return existing_player.id
    if lobby is not None and not existing_player and len(
            list(select(p for p in lobby.player))) < lobby.max_players and not lobby.started:
        p = Player(user=user, lobby=lobby)
        commit()
        player_id = p.id

    return player_id


# Returns player_id player's vote status.
@db_session
def get_player_vote_status(player_id: int) -> bool:
    cv = CurrentVote.get(player=player_id)
    return cv is not None


# Returns player_id player's last public vote.
@db_session
def get_player_last_vote(player_id: int) -> bool:
    pv = PublicVote.get(voter_id=player_id)
    if pv is None:
        return False
    return pv.vote


# Return the required player_id status according to the caller player_id.
@db_session
def get_player_public(player_id: int, c_player_id: int) -> PlayerPublic:
    player = Player.get(id=player_id)
    if can_know_roles(c_player_id, player_id):
        if player.role.phoenix:
            role = Role("Order of the Phoenix")
        elif player.role.voldemort:
            role = Role("voldemort")
        else:
            role = Role("Death Eater")
        return PlayerPublic(player_id=player_id,
                            alive=player.alive,
                            voted=get_player_vote_status(player_id),
                            last_vote=get_player_last_vote(player_id),
                            nickname=player.user.nickname,
                            position=player.position,
                            role=role)
    else:
        return PlayerPublic(player_id=player_id,
                            alive=player.alive,
                            voted=get_player_vote_status(player_id),
                            last_vote=get_player_last_vote(player_id),
                            nickname=player.user.nickname,
                            position=player.position)


# Can player a know the role of player b?
def can_know_roles(player_id_a: int, player_id_b: int) -> bool:
    if player_id_a == player_id_b:
        return True
    player_a = Player.get(id=player_id_a)

    result = False
    if player_a.role.voldemort:
        result = VOLDEMORT_PERMISSIONS[player_a.lobby.max_players]
    elif not player_a.role.phoenix:
        result = True
    return result


# Return the required player id.
@db_session
def get_player_id(user_email: str, game_id: int) -> int:
    user = User.get(email=user_email)
    lobby = Lobby.get(id=game_id)

    player_id = -1
    if lobby is not None and lobby is not None:
        player = Player.get(user=user, lobby=lobby)
        # If there's no player with user_email in game_id,
        # it returns default the value.
        if player is not None:
            player_id = player.id

    return player_id


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

    return voldemort, phoenix


# Check if the player identified by player_id is the director
@db_session
def is_director(player_id: int) -> bool:
    return Player.get(id=player_id).director


# Check if it's time for the director to choose a proclamation card
@db_session
def director_chooses_proc(game_id: int) -> bool:
    lobby = Lobby.get(id=game_id)
    game = lobby.game
    return game and game.in_session and game.minister_proclaimed


# Discharge director
@db_session
def discharge_director(game_id: int):
    director = Player.get(lobby=game_id, director=True)

    if director is not None:
        director.director = False

    commit()


# Check if it's time for the minister to choose a proclamation card
@db_session
def minister_chooses_proc(game_id: int) -> bool:
    lobby = Lobby.get(id=game_id)
    game = lobby.game
    return game and game.in_session and not game.minister_proclaimed


# Checks if player is alive
@db_session
def get_player_alive(player_id: int) -> bool:
    player = Player.get(id=player_id)
    return player.alive


# Checks if the player is in the game
@db_session
def get_player_in_game(player_id: int, game_id: int) -> bool:
    player = Player.get(id=player_id, lobby=game_id)

    return player is not None
