from pony.orm import *
from .models import *
from api.schemas import *

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

# Insert user into the database.
@db_session
def register_user(user: UserReg):
    User(mail = user.email, username = user.username, password = user.password)
    commit()

# Get all users from the database.
@db_session
def get_users_for_login():
    users = dict(select((u.mail, u.password) for u in User))
    return users

# Get all emails from the database.
@db_session
def get_emails():
    emails = list(select(u.mail for u in User))
    return emails
