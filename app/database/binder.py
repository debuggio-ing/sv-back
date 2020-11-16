from app.crud.vote import *
from app.crud.game import *
from app.crud.player import *
from app.crud.user import *
from app.crud.lobby import *
from app.crud.card import *
from app.crud.spell import *


def bind_db(test):
    if test:
        db.bind(provider='sqlite', filename='test.sqlite', create_db=True)
    else:
        db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
    db.generate_mapping(create_tables=True)
