from datetime import datetime
from pony.orm import *
from app.database.models import *
from app.api.schemas import *
from app.api.hasher import *


db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)


# Insert user into the database.
@db_session
def register_user(user: UserReg) -> int:
    guser = User.get(email=user.email)
    if guser is not None:

        return -1

    u = User(
        email=user.email,
        username=user.username,
        password=encrypt_password(
            user.password))
    commit()
    return u.id

# Get password hash for solicited user.
@db_session
def get_password_hash(uemail: str) -> str:
    user = User.get(email=uemail)

    phash = encrypt_password("")
    if user != None:
        phash = user.password

    return phash

# Get all users from the database.
@db_session
def get_users_for_login():
    users = dict(select((u.email, u.password) for u in User))
    return users

# Get all emails from the database.
@db_session
def get_emails():
    emails = list(select(u.email for u in User))
    return emails

@db_session
def get_player_status() -> PlayerPublic:
    return

@db_session
def get_game_status(game_id: int) -> GamePublic:

    lobby = Lobby.get(id=game_id)
    game = lobby.game
    ans = GamePublic()
    return


@db_session
def get_player_id(user_email: str, game_id: int):


    user = User.get(email=user_email)
    lobby = Lobby.get(id=game_id)

    player = Player.get(user=user, lobby=lobby)

    pid = -1
    if  player is not None:
        pid = player.id

    return pid

@db_session
def currently_voting(game_id: int):

    lobby = Lobby.get(id=game_id)
    return lobby.game.voting

@db_session
def is_last_vote(player_id: int, game_id: int):

    lobby = Lobby.get(id=game_id)
    game = lobby.game
    player = Player.get(id=player_id)
    max_players = lobby.max_players

    current_votes = lobby.game.numv
    already_vote = CurrentVote.get(voter_id=player_id)

    if already_vote is None:
        current_votes += 1

    return current_votes == max_players

@db_session
def set_last_player_vote(player_id: int, game_id: int, vote: bool):

    set_player_vote(player_id, game_id, vote)
    update_public_vote(game_id)
    clean_current_vote(game_id)

    commit()


@db_session
def set_player_vote(player_id: int, game_id: int, vote: bool):


    player = Player.get(id=player_id, lobby=game_id)
    lobby = Lobby.get(id=game_id)
    game = lobby.game

    if player.curr_vote is None:
        player.curr_vote = CurrentVote(game=game, player=player, vote=vote, voter_id=player_id)
        lobby.game.numv += 1
    else:
        player.curr_vote.vote = vote

    commit()

@db_session
def update_public_vote(game_id: int):

    lobby = Lobby.get(id=game_id)
    game = lobby.game

    delete(v for v in PublicVote)

    votes = (select((v.vote, v.voter_id) for v in CurrentVote))[:]

    for v in votes:
        pv = PublicVote(game=game, vote=v[0], voter_id=v[1])

    lobby.game.voting = False
    commit()

@db_session
def clean_current_vote(game_id: int):

    lob = Lobby.get(id=game_id)

    delete(v for v in CurrentVote)

    lob.game.numv = 0

    commit()


@db_session
def populate_test_db():
    user1 = User(email="maw1@gmail.com", username="maw", password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.")
    user2 = User(email="law@gmail.com", username="law", password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.")
    user3 = User(email="lau@gmail.com", username="lau", password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.")
    user4 = User(email="ulince@gmail.com", username="ulince", password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.")
    user5 = User(email="nico@gmail.com", username="nico", password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.")

    lobby1 = Lobby(name="mortifagos 4ever", max_players=5)
    lobby2 = Lobby(name="larga vida harry", max_players=5)
    lobby3 = Lobby(name="tom laura riddle", max_players=5)

    game1 = Game(lobby=lobby1, voting=True, semaphore=0, numv=3)

    role_vol = GRole(voldemort=True, phoenix=False)
    role_dea = GRole(voldemort=False, phoenix=False)
    role_ord = GRole(voldemort=False, phoenix=True)

    p1 = Player(position=1,user=user1, lobby=lobby1, role=role_vol, minister=False, director=False)
    p2 = Player(position=2,user=user2, lobby=lobby1, role=role_dea, minister=False, director=False)
    p3 = Player(position=3,user=user3, lobby=lobby1, role=role_ord, minister=False, director=False)
    p4 = Player(position=4,user=user4, lobby=lobby1, role=role_ord, minister=False, director=False)
    p5 = Player(position=5,user=user5, lobby=lobby1, role=role_ord, minister=False, director=False)

    curr_vote1 = CurrentVote(game=game1, player=p1, vote=True, voter_id=1)
    curr_vote3 = CurrentVote(game=game1, player=p3, vote=True, voter_id=3)
    curr_vote4 = CurrentVote(game=game1, player=p4, vote=True, voter_id=4)

    last_vote1 = PublicVote(game=game1, player=p1, vote=True, voter_id=1)
    last_vote2 = PublicVote(game=game1, player=p2, vote=True, voter_id=2)
    last_vote3 = PublicVote(game=game1, player=p3, vote=True, voter_id=3)
    last_vote4 = PublicVote(game=game1, player=p4, vote=True, voter_id=4)
    last_vote4 = PublicVote(game=game1, player=p5, vote=True, voter_id=5)


@db_session
def delete_db():
    delete(r for r in GRole)
    delete(g for g in Game)
    delete(l for l in Lobby)
    delete(u for u in User)
    delete(p for p in Player)
    delete(v for v in PublicVote)
    delete(v for v in CurrentVote)


# Create lobby in the database.
@db_session
def insert_lobby(lobby: LobbyReg) -> int:
    l = Lobby(
        name=lobby.name,
        max_players=lobby.max_players,
        creation_date=datetime.now())
    commit()
    return l.id

# Create player in the database.
@db_session
def insert_player(user_email: str, lobby_id: int) -> int:
    lobby = Lobby.get(id=lobby_id)
    user = User.get(email=user_email)

    player_id = -1
    if lobby != None and user not in lobby.player.user:
        p = Player(user=user, lobby=lobby)
        commit()
        player_id = p.id

    return player_id

# Get all players username who are in lobby_id lobby.
@db_session
def get_lobby_player_list(lobby_id: int):
    players = list(
        select(
            p.user.username for p in Player if lobby_id == p.lobby.id))

    return players

# Get lobby_id lobby's name.
@db_session
def get_lobby_name(lobby_id: int):
    lobby = Lobby.get(id=lobby_id)

    name = ""
    if lobby != None:
        name = lobby.name

    return name

# Get lobby_id lobby's max_player attribute.
@db_session
def get_lobby_max_players(lobby_id: int):
    lobby = Lobby.get(id=lobby_id)

    max_players = 0
    if lobby != None:
        max_players = lobby.max_players

    return max_players

# Get all lobbies ids.
@db_session
def get_all_lobbies_ids(lobby_from: Optional[int], lobby_to: Optional[int]):
    max_id = max(l.id for l in Lobby)
    if lobby_to is None and max_id is not None:
        # If there's an active lobby, set lobby_to = max_id.
        lobby_to = max_id
    elif lobby_to is None and max_id is None:
        # If there's no active lobby, set lobby_to = 0.
        lobby_to = 0

    # Get all lobies with id within range.
    lobbies_ids = list(select(l.id for l in Lobby if
                              l.id >= lobby_from and l.id <= lobby_to))

    return lobbies_ids
