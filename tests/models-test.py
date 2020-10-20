from ..models import *


db.bind(provider='sqlite', filename=':memory:', create_db=True)
db.generate_mapping(create_tables=True)
set_sql_debug(True)


@db_session
def create_users():
    u1 = User(mail='laumail', username='lau', password='123456', players=set())
    u2 = User(mail='lawmail', username='law',
              password='password', players=set())
    u3 = User(mail='ulincemail', username='ulince',
              password='1234567', players=set())
    u4 = User(mail='mawmail', username='maw', password='123467', players=set())
    u5 = User(mail='nicomail', username='nico',
              password='password', players=set())
    u6 = User(mail='einsteinmail', username='einsten',
              password='emc2', players=set())
    u7 = User(mail='newtonmail', username='newton',
              password='fma', players=set())
    commit()


@db_session
def create_img():
    i1 = Image(height=12, width=456, filename='notempty',
               user=User.select(lambda u: u.username == 'lau').get())
    i2 = Image(height=124, width=456, filename='notempty2',
               user=User.select(lambda u: u.username == 'law').get())
    i3 = Image(height=124, width=456, filename='notempty3',
               user=User.select(lambda u: u.username == 'newton').get())


@db_session
def create_lobbies():
    l1 = Lobby(name="fisicos", max_players=5, creation_date=datetime.now())


@db_session
def join_lobby():
    p1 = Player(alive=True, order=0, minister=False, director=False, user=User.select(
        lambda u: u.username == 'newton').get(), lobby=Lobby.select(lambda l: l.id == 1).get())


@db_session
def show_users():
    select(u for u in User).show()
