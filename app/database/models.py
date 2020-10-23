from datetime import datetime
from sys import maxsize
from pony.orm import *


db = Database()


# Created when a new user is registered
class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    email = Required(str, unique=True)
    username = Required(str)
    password = Required(str)
    image = Optional('Image')
    players = Set('Player')
    email_verified = Required(bool, default=False, sql_default='1')
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
    alive = Required(bool)
    order = Required(int)
    secret_role = Required('Role')
    minister = Required(bool)
    director = Required(bool)
    vote = Required('Vote')
    user = Required('User')
    lobby = Required('Lobby')
    composite_key(user, lobby)


class Role(db.Entity):
    id = PrimaryKey(int, auto=True)
    players = Set('Player')
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

# currently voting information
class CurrentVote(db.Entity):
    id = PrimaryKey(int, auto=True) #la pone el player_id
    vote = Required(bool)
    games = Required('Match')
    player = Set(Player)

# Last public vote result
class PublicVote(db.Entity):
    id = PrimaryKey(int, auto=True) #la pone el player_id
    vote = Required(bool)
    games = Required('Match')
    player = Set(Player)


# Created when a game is started
class Match(db.Entity):
    id = PrimaryKey(int, auto=True)
    semaphore = Required(int, min=0, max=3)
    lobby = Required('Lobby')
    cards = Set('Card')
    voting = Required(bool) #are players currently voting?
    last_vote = Required('PublicVote') #public voting information
    curr_vote = Required('CurrentVote') #if currently voting


# Created when a game is started
class Card(db.Entity):
    id = PrimaryKey(int, auTrueto=True)
    discarded = Required(bool)
    proclaimed = Required(bool)
    order = Required(int)
    is_phoenix = Required(bool)
    match = Required('Match')
