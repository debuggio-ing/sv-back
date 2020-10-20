from pony.orm import *
from schemas import *
from models import *

db.generate_mapping(create_tables=True)

# Insert user into the database.
@db_session
def insert_user(user: UserSchema):
    User(mail = user.email, username = user.username, password = user.password)
    commit()

# Get all users from the database.
@db_session
def get_usernames():
    users = list(select(u.username for u in User))
    return users

# Get all emails from the database.
@db_session
def get_emails():
    emails = list(select(u.mail for u in User))
    return emails
