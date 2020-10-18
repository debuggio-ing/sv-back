from datetime import datetime
from pony.orm import *


db = Database()


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    mail = Required(str, unique=True)
    username = Required(str, unique=True)
    password = Required(str, hidden=True)
    image = Optional('Image')
    players = Set('Player')


class Image(db.Entity):
    id = PrimaryKey(int, auto=True)
    height = Required(int)
    width = Required(int)
    filename = Required(str, unique=True)
    user = Required('User')


class Player(db.Entity):
    id = PrimaryKey(int, auto=True)
    alive = Required(bool)
    order = Required(int)
    secret_role = Optional('Role')
    minister = Required(bool)
    director = Required(bool)
    user = Required('User')
    lobby = Required('Lobby')
    composite_key(user, lobby)


class Role(db.Entity):
    id = PrimaryKey(int, auto=True)
    player = Required('Player')


class Voldemort(Role):
    pass


class Phoenix(Role):
    pass


class DeathEatear(Role):
    pass


class Lobby(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    max_players = Required(int)
#    initial_card_order = Required(str)
    creation_date = Required(datetime)
    players = Set('Player')
    match = Optional('Match')
    chat = Optional('Chat')


class Chat(db.Entity):
    id = PrimaryKey(int, auto=True)
    text = Required(str)
    lobby = Required('Lobby')


class Match(db.Entity):
    id = PrimaryKey(int, auto=True)
    game_score = Required(str)  # rethink
    semaphore = Optional(str)  # rethink
    lobby = Required('Lobby')
    procl_pool = Optional('Procl_pool')


class Procl_pool(db.Entity):
    id = PrimaryKey(int, auto=True)
    discarded = Required(bool)
    phoenix = Required(bool)
    order = Required(str)
    match = Required('Match')
