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
    user = Required(User)

class Player(db.Entity):
    id = PrimaryKey(int, auto=True)
    alive = Required(bool)
    secret_role = Required(int)
    position = Required(int)
    minister = Required(bool)
    Director = Required(bool)
    user = Required(User)
    lobby = Required('Lobby')


class Lobby(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    num_players = Required(int)
    max_players = Required(int)
    initial_card_order = Required(str)
    player_order = Required(str)
    creation_date = Required(datetime)
    players = Set(Player)
    match = Optional('Match')
    chat = Optional('Chat')


class Chat(db.Entity):
    id = PrimaryKey(int, auto=True)
    text = Required(str)
    lobby = Required(Lobby)


class Match(db.Entity):
    id = PrimaryKey(int, auto=True)
    game_score = Required(str)
    semaphore = Optional(str)
    lobby = Required(Lobby)
    procl_pool = Optional('Procl_pool')


class Procl_pool(db.Entity):
    id = PrimaryKey(int, auto=True)
    discarded = Required(bool)
    phoenix = Required(bool)
    order = Required(str)
    match = Required(Match)



db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
set_sql_debug(True)
@db_session
def hola():
    u1 = User(mail='laumail', username='lau', password='123456', players=set())
    #commit()
    select(p for p in User).show()