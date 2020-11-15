import random

from app.validators.hasher import *
from app.database.models import *
from app.schemas.schemas import *


# Insert user into the database.
@db_session
def register_user(user: UserReg) -> int:
    guser = User.get(email=user.email)
    # Check if user.email is already in use.
    if guser is not None:
        return -1

    code = random.randint(100000, 999999)

    u = User(email=user.email, nickname=user.nickname,
             password=encrypt_password(user.password), verification_code=code)
    commit()

    # send_email(user_email=user.email, code=code)
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


# Get nickname for solicited user.
@db_session
def get_nickname(user_email: str) -> str:
    user = User.get(email=user_email)

    uname = ""
    if user is not None:
        uname = user.nickname

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
                      nickname=get_nickname(user_email=user_email),
                      email=user_email
                      )


# Set nickname for the solicited user.
@db_session
def set_nickname(user_email: str, nickname: str):
    if nickname is not None:
        user = User.get(email=user_email)
        if user is not None:
            user.nickname = nickname

        commit()


# Set picture for the solicited user
@db_session
def set_picture(user_email: str, image: bytes):
    if image is not None:
        user = User.get(email=user_email)
        if user.image is None:
            user.image = Image(image=image, user=user)
        else:
            user.image.image = image
        commit()


# Return the image bytes for the solicited user
@db_session
def get_picture(user_email: str):
    user = User.get(email=user_email)
    image = None
    if user.image is not None:
        image = user.image.image
    return image


# Set password for the solicited user
@db_session
def set_password(user_email: str, password: str):
    if password is not None:
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
