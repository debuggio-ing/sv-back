from app.models.base import *


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
    messages = Set('Message')
    composite_key(user, lobby)


# Created with a new game
class Chat(db.Entity):
    id = PrimaryKey(int, auto=True)
    text = Required(str)
    lobby = Required('Lobby')
