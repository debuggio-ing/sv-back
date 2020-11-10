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
    verification_code = Required(int, default=100000)


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
    minister = Required(bool, default=False)
    prev_minister = Required(bool, default=False)
    director = Required(bool, default=False)
    prev_director = Required(bool, default=False)
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
    active = Required(bool, default=True)  # set to false if game has finished.
    owner_id = Required(int)
    player = Set('Player')
    game = Optional('Game')
    started = Required(bool, default=False)
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
    game = Required(int)
    player = Required(int)


# Last public vote result
class PublicVote(db.Entity):
    id = PrimaryKey(int, auto=True)
    vote = Required(bool)
    voter_id = Required(int)  # redundancia por ahora
    game = Required(int)
    player = Required(int)


# Created when a game is started
class Game(db.Entity):
    id = PrimaryKey(int, auto=True)
    semaphore = Required(int, min=0, max=3, default=0)
    list_head = Required(int, default=0)
    lobby = Required('Lobby')
    cards = Set('ProcCard')
    in_session = Required(bool, default=False)  # in legislative session
    minister_proclaimed = Required(bool, default=False)  # minister chose cards
    director_proclaimed = Required(bool, default=False)  # director chose cards
    last_proc_negative = Required(
        bool, default=False)  # last proclamation was bad
    voting = Required(bool, default=False)  # are players currently voting?
    num_votes = Required(int, default=0)
    ended = Required(bool, default=False)


# Created when a game is started


class ProcCard(db.Entity):
    id = PrimaryKey(int, auto=True)
    discarded = Required(bool, default=False)
    proclaimed = Required(bool, default=False)
    selected = Required(bool, default=False)  # selected in legislative session
    position = Required(int)
    phoenix = Required(bool)
    game = Required('Game')
    composite_key(position, game)
