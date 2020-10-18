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
    voldemort = Required(bool)
    phoenix = Required(bool)


class Lobby(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    max_players = Required(int)
    creation_date = Required(datetime)
    created_by = Required('Player')
    players = Set('Player')
    match = Optional('Match')
    chat = Optional('Chat')


class Chat(db.Entity):
    id = PrimaryKey(int, auto=True)
    text = Required(str)
    lobby = Required('Lobby')


class Match(db.Entity): #complete
    id = PrimaryKey(int, auto=True)
    semaphore = Required(int) 
    lobby = Required('Lobby')
    cards = Set('Card')


class Card(db.Entity):
    id = PrimaryKey(int, auto=True)
    discarded = Required(bool)
    proclaimed = Required(bool)
    order = Required(int)
    is_phoenix = Required(bool)
    match = Required('Match')
