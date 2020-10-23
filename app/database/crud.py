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

@db_session
def get_player_id(user_email: str, game_id: int):
    
    idlist = list(select(p.id for p in Player if p.user.email == user_email))

    pid = -1
    if  0 < len(idlist):
        pid = idlist[0]

    return pid

@db_session
def is_last_vote(user_email: str, game_id: int):

    plist = select(lobby.match.curr_vote.player.user.email for lobby in Lobby if lobby.id == game_id)
    
    max_players = get(lobby.max_players for lobby in Lobby if lobby.id == game_id)
    
    if user_email not in plist:
        max_players -= 1

    return len(plist) == max_players

@db_session
def set_player_vote(player_id: int, game_id: int, vote.vote: bool):

    return
