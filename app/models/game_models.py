from app.models.base import *


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
    # director asked for expelliarmus?
    expelliarmus = Required(bool, default=False)
    # is the match waiting for a cucio curse?
    in_crucio = Required(bool, default=False)
    # last player_id that has been cruciated
    last_tortured = Required(int, default=-1)
    last_proc_negative = Required(
        bool, default=False)  # last proclamation was bad
    voting = Required(bool, default=False)  # are players currently voting?
    num_votes = Required(int, default=0)
    ended = Required(bool, default=False)
    phoenix_win = Required(bool, default=False)
    dead_players = Required(int, default=0)


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


# Indicates the role of a(some) player(s) in a match
class GRole(db.Entity):
    id = PrimaryKey(int, auto=True)
    players = Set('Player')
    voldemort = Required(bool)
    phoenix = Required(bool)


# Created when a game is started
class ProcCard(db.Entity):
    id = PrimaryKey(int, auto=True)
    discarded = Required(bool, default=False)
    proclaimed = Required(bool, default=False)
    selected = Required(bool, default=False)  # selected in legislative session
    position = Required(int)
    phoenix = Required(bool)
    game = Required('Game')


# Storing chat's messages.
class Message(db.Entity):
    id = PrimaryKey(int, auto=True)
    sender = Required('Player')
    message = Required(str)
