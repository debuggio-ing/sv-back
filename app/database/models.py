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


# Created when the user joins a Game
class Player(db.Entity):
    id = PrimaryKey(int, auto=True)
    alive = Required(bool, default=True)
    position = Required(int, default=0)
    role = Optional('GRole')
    curr_vote = Optional('CurrentVote')
    pub_vote = Optional('PublicVote')
    minister = Required(bool, default=False)
    director = Required(bool, default=False)
    user = Required('User')
    lobby = Required('Lobby')
    composite_key(user, lobby)


# Indicates the role of a(some) player(s) in a match
class GRole(db.Entity):
    id = PrimaryKey(int, auto=True)
    players = Set('Player')
    voldemort = Required(bool)
    phoenix = Required(bool)


# Created as a new game
class Lobby(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    max_players = Required(int)
    creation_date = Required(datetime, default=datetime.now)
    player = Set('Player')
    game = Optional('Game')
    chat = Optional('Chat')


# Created with a new game
class Chat(db.Entity):
    id = PrimaryKey(int, auto=True)
    text = Required(str)
    lobby = Required('Lobby')


# Current voting information
class CurrentVote(db.Entity):
    id = PrimaryKey(int, auto=True)
    vote = Required(bool)
    voter_id = Required(int)  # redundancia por ahora
    game = Set('Game')
    player = Set('Player')


# Last public vote result
class PublicVote(db.Entity):
    id = PrimaryKey(int, auto=True)
    vote = Required(bool)
    voter_id = Required(int)  # redundancia por ahora
    game = Set('Game')
    player = Set('Player')


# Created when a game is started
class Game(db.Entity):
    id = PrimaryKey(int, auto=True)
    semaphore = Required(int, min=0, max=3)
    lobby = Required('Lobby')
    cards = Set('Card')
    voting = Required(bool)  # are players currently voting?
    numv = Required(int, default=0)
    last_vote = Optional('PublicVote')  # public voting information
    curr_vote = Optional('CurrentVote')  # if currently voting


# Created when a game is started
class Card(db.Entity):
    id = PrimaryKey(int, auto=True)
    discarded = Required(bool)
    proclaimed = Required(bool)
    order = Required(int)
    is_phoenix = Required(bool)
    Game = Required('Game')
