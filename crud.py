from pony.orm import *
from schemas import *
from models import *

db.generate_mapping(create_tables=True)

@db_session
def insert_user(user: UserSchema):
    User(mail = user.email, username = user.username, password = user.password)
    commit()

@db_session
def get_usernames():
    users = list(select(u.username for u in User))
    return users

@db_session
def get_emails():
    emails = list(select(u.mail for u in User))
    return emails
