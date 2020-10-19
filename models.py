from pony.orm import *

db = Database()

# PonyORM User class.
class User(db.Entity):
    mail = Required(str)
    username = Required(str)
    password = Required(str)

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
