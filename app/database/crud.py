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

    if len(select(u.email for u in User if u.email == user.email)) != 0:
        return -1

    u = User(email=user.email, username=user.username, password=encrypt_password(user.password))
    commit()
    return u.id

# Get password hash for solicited user.
@db_session
def get_password_hash(uemail:str) -> str:
    phashlist = list(select(u.password for u in User if u.email == uemail))

    phash = encrypt_password("")
    if len(phashlist) > 0:
        phash = phashlist[0]

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

# Create lobby in the database.
@db_session
def insert_lobby(lobby: LobbyReg) -> int:
    l = Lobby(name=lobby.name, max_players=lobby.max_players, creation_date=datetime.now())
    commit()
    return l.id

# Create player in the database.
@db_session
def insert_player(user_email: str, lobby_id: int) -> int:
    lobby = Lobby.get(id=lobby_id)
    user = User.get(email=user_email)

    p = Player(user=user, lobby=lobby)
    commit()

    return p.id

# Get all players username who are in lobby_id lobby.
@db_session
def get_lobby_player_list(lobby_id: int):
    players = list(select(p.user.username for p in Player if lobby_id == p.lobby.id))

    return players

# Get lobby_id lobby's name.
@db_session
def get_lobby_name(lobby_id: int):
    names = list(select(l.name for l in Lobby if lobby_id == l.id))

    name = ""
    if len(names) > 0:
        name = names[0]

    return name

# Get lobby_id lobby's max_player attribute.
@db_session
def get_lobby_max_players(lobby_id: int):
    mps = list(select(l.max_players for l in Lobby if lobby_id == l.id))

    max_players = 0
    if len(mps) > 0:
        max_players = mps[0]

    return max_players
