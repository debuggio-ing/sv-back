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


# Get username for solicited user.
@db_session
def get_username(user_email: str) -> str:
    user = User.get(email=user_email)

    uname = ""
    if user is not None:
        uname = user.username

    return uname


# Get all users from the database.
@db_session
def get_users_for_login():
    users = dict(select((u.email, u.password) for u in User))
    return users


# Get user_email user id.
@db_session
def get_user_id(user_email: str) -> int:
    user = User.get(email=user_email)

    user_id = -1
    if user is not None:
        user_id = user.id

    return user_id


# Get all emails from the database.
@db_session
def get_emails():
    emails = list(select(u.email for u in User))
    return emails


# Get all user_email user active games.
@db_session
def get_active_games(user_email: str):
    user = User.get(email=user_email)

    games = []
    if user is not None:
        games = list(
            select(g.id for g in Game
                   if user in g.lobby.player.user and g.lobby.active))

    return games


# Return the required user's information.
@db_session
def get_user_public(user_email: str):
    return UserPublic(id=get_user_id(user_email),
                      username=get_username(user_email=user_email),
                      email=user_email
                      )


# Set username for the solicited user.
@db_session
def change_username(user_email: str, username: str):
    user = User.get(email=user_email)
    user2 = User.get(username=username)
    if user2 is not None:
        return -1

    if user is not None:
        user.username = username

    commit()


# Set password for the solicited user
@db_session
def set_password(user_email: str, password: str):
    user = User.get(email=user_email)

    if user is not None:
        user.password = encrypt_password(password)
    commit()


# Get verification code for solicited user.
@db_session
def get_verification_code(user_email: str):
    user = User.get(email=user_email)

    code = 0
    if user is not None:
        code = user.verification_code

    return code


# Set user as verified.
@db_session
def set_user_email_verified(user_email: str):
    user = User.get(email=user_email)

    if user is not None:
        user.email_verified = True

    commit()


# Return whether user email is verified.
@db_session
def get_is_email_verified(user_email: str):
    user = User.get(email=user_email)

    is_verified = False
    if user is not None:
        is_verified = user.email_verified

    return is_verified
