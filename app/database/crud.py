from pony.orm import *
from app.database.models import *
from app.api.schemas import *

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

# Insert user into the database.
@db_session
def register_user(user: UserReg) -> int:

    if len(select(u.email for u in User if u.email == user.email)) != 0:
        return -1

    u = User(email=user.email, username=user.username, password=user.password)
    commit()
    return u.id

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
