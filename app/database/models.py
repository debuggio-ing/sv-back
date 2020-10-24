from datetime import datetime
from sys import maxsize
from pony.orm import *


db = Database()


# Created when a new user is registered
class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    email = Required(str, unique=True)
    username = Required(str, unique=True)
    password = Required(str)
    image = Optional('Image')
    players = Set('Player')
    email_verified = Required(bool, default=True, sql_default='1')
    last_login = Required(datetime, default=datetime.now)
    register_date = Required(datetime, default=datetime.now)

# Created when the user uploads a profile image
class Image(db.Entity):
    id = PrimaryKey(int, auto=True)
    height = Required(int)
    width = Required(int)
    filename = Required(str)
    user = Required('User')


# Created when the user joins a match
class Player(db.Entity):
    id = PrimaryKey(int, auto=True)
    alive = Required(bool, default=True)
    order = Required(int, default=0)
    secret_role = Optional('Role')
    minister = Required(bool, default=False)
    director = Required(bool, default=False)
    user = Required('User')
    lobby = Required('Lobby')
    composite_key(user, lobby)


# Created when the user is assigned a role
class Role(db.Entity):
    id = PrimaryKey(int, auto=True)
    player = Required('Player')
    voldemort = Required(bool)
    phoenix = Required(bool)


# Created as a new game
class Lobby(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    max_players = Required(int)
    creation_date = Required(datetime)
    players = Set('Player')
    match = Optional('Match')
    chat = Optional('Chat')


# Created with a new game
class Chat(db.Entity):
    id = PrimaryKey(int, auto=True)
    text = Required(str)
    lobby = Required('Lobby')


# Created when a game is started
class Match(db.Entity):
    id = PrimaryKey(int, auto=True)
    semaphore = Required(int, min=0, max=3)
    lobby = Required('Lobby')
    cards = Set('Card')


# Created when a game is started
class Card(db.Entity):
    id = PrimaryKey(int, auto=True)
    discarded = Required(bool)
    proclaimed = Required(bool)
    order = Required(int)
    is_phoenix = Required(bool)
    match = Required('Match')
