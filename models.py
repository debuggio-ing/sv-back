from pony.orm import *

db = Database()

class User(db.Entity):
    # id = Required(int)
    mail = Required(str)
    username = Required(str)
    password = Required(str)

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
