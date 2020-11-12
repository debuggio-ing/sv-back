from app.database.models import *


# This function can be extended with a parameter to select how many players the game will have
@db_session
def create_cards(game):
    for i in range(17):
        # the position of the next cards are 0,6,12
        c = ProcCard(game=game, proclaimed=i % 3, discarded=i % 2, selected=False, position=i, phoenix=(i in [0, 12]))
    commit()


# This functions creates players in a game given the users and the lobby
@db_session
def create_players(users, lobby):
    role_vol = GRole(voldemort=True, phoenix=False)
    role_dea = GRole(voldemort=False, phoenix=False)
    role_ord = GRole(voldemort=False, phoenix=True)
    players = []
    # can be extended generalize these tests (will save time in the future)
    order_players = 3
    for u in users:
        if users.index(u) in range(order_players):
            players.append(Player(position=users.index(u), user=u, lobby=lobby, role= role_ord))
        elif users.index(u) == order_players:
            players.append(Player(position=users.index(u), user=u, lobby=lobby, role=role_dea))
        else:
            players.append(Player(position=users.index(u), user=u, lobby=lobby, role=role_vol))
    players[0].minister = True
    players[1].director = True
    commit()


# This function creates the entire database according to the spell to test
@db_session
def spell_database(spell:str):
    users = [User(email="maw@gmail.com",username="maw",password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.",        verification_code=111111), User(        email="law@gmail.com",        username="law",        password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.",        verification_code=111111),        User(            email="lau@gmail.com",            username="lau",           password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.",            verification_code=111111),        User(            email="ulince@gmail.com",            username="ulince",           password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.",            verification_code=111111),       User(           email="nico@gmail.com",           username="nico",           password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.",           verification_code=111111)       ]
    commit()
    lobby = Lobby(name="mortifagos 4ever", max_players=5, owner_id=users[0].id)
    create_players(users=users, lobby=lobby)

    if spell == "Divination":
        game = Game(lobby=lobby, in_session=True, minister_proclaimed=True, director_proclaimed=True)
        create_cards(game=game)
    elif spell == "Avada Kedavra":
        pass
