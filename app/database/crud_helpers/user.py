from app.database.models import *
from app.api.schemas import *
from app.api.hasher import *


# Insert user into the database.
@db_session
def register_user(user: UserReg) -> int:
    guser = User.get(email=user.email)
    # Check if user.email is already in use.
    if guser is not None:
        return -1

    u = User(email=user.email, username=user.username,
             password=encrypt_password(user.password))
    commit()
    return u.id


# Get password hash for solicited user.
@db_session
def get_password_hash(uemail: str) -> str:
    user = User.get(email=uemail)

    # Return default password if there's no user
    # with that email.
    phash = encrypt_password("")
    if user is not None:
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


# Get all user_id user active games.
@db_session
def get_active_games(user_email: str):
    user = User.get(email=user_email)

    games = []
    if user is not None:
        games = list(
            select(g.id for g in Game
                   if user in g.lobby.player.user and g.lobby.active))

    return games
