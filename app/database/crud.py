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
    phash = list(select(u.password for u in User if u.email == uemail))
    return phash[0]

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

# 
@db_session
def insert_lobby(lobby: LobbyReg) -> int:
    l = Lobby(name=lobby.name, max_players=lobby.max_players, creation_date=datetime.now())
    commit()
    return l.id

@db_session
def insert_player(user_email: str, lobby_id: int) -> int:
    lobby = select(l for l in Lobby if l.id == lobby_id)
    user = select(u for u in User if u.email == user_email)

    p = Player(user=user, lobby=lobby)
    commit()

    select(u for u in Player).show()

    return p.id