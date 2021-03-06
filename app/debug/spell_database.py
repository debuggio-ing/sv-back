from app.database.binder import *
from app.validators.constants import *

# This function can be extended with a parameter to select how many
# players the game will have


@db_session
def create_cards(game):
    for i in range(17):
        # the position of the next cards are 0,6,12
        c = ProcCard(
            game=game,
            proclaimed=(i in [13, 14, 15]),
            discarded=(i in [2, 3]),
            selected=False,
            position=i,
            phoenix=(
                i in [
                    0,
                    12]))
    commit()


@db_session
def create_cards_avada_kedavra(game):
    for i in range(17):
        # the position of the next cards are 0,6,12
        c = ProcCard(
            game=game,
            proclaimed=(i in [13, 14, 15, 16]),
            discarded=(i in [2, 3, 4]),
            selected=False,
            position=i,
            phoenix=(
                i in [
                    0,
                    12]))
    commit()


@db_session
def create_cards_imperio(game):
    for i in range(17):
        # the position of the next cards are 0,6,12
        c = ProcCard(
            game=game,
            proclaimed=(i in [6, 7, 8]),
            discarded=(i in [2, 3, 4]),
            selected=False,
            position=i,
            phoenix=i in [0, 1, 2, 3, 4, 5])
    commit()


@db_session
def create_cards_crucio(game):
    for i in range(17):
        # the position of the next cards are 0,6,12
        c = ProcCard(
            game=game,
            proclaimed=(i in [15, 16]),
            discarded=(i in [3, 4]),
            selected=False,
            position=i,
            phoenix=(
                i in [
                    0,
                    12]))
    commit()


# This functions creates players in a game given the users and the lobby
@db_session
def create_players(users, lobby, player_amount):
    role_vol = GRole(voldemort=True, phoenix=False)
    role_dea = GRole(voldemort=False, phoenix=False)
    role_ord = GRole(voldemort=False, phoenix=True)
    players = []
    death_eaters = NUM_DEATH_EATERS[player_amount]
    for u in users:
        if users.index(u) in range(death_eaters - 1):
            players.append(
                Player(
                    position=users.index(u),
                    user=u,
                    lobby=lobby,
                    role=role_dea))
        elif users.index(u) == death_eaters:
            players.append(
                Player(
                    position=users.index(u),
                    user=u,
                    lobby=lobby,
                    role=role_vol))
        else:
            players.append(
                Player(
                    position=users.index(u),
                    user=u,
                    lobby=lobby,
                    role=role_ord))
    players[0].minister = True
    players[1].director = True
    commit()


# This function creates the entire database according to the spell to test
@db_session
def spell_database(spell: str):
    users = [
        User(
            email="maw@gmail.com",
            nickname="maw",
            password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.",
            verification_code=111111),
        User(
            email="law@gmail.com",
            nickname="law",
            password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.",
            verification_code=111111),
        User(
            email="lau@gmail.com",
            nickname="lau",
            password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.",
            verification_code=111111),
        User(
            email="ulince@gmail.com",
            nickname="ulince",
            password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.",
            verification_code=111111),
        User(
            email="nico@gmail.com",
            nickname="nico",
            password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.",
            verification_code=111111),
        User(
            email="maw2@gmail.com",
            nickname="maw2",
            password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.",
            verification_code=111111),
        User(
            email="maw3@gmail.com",
            nickname="maw",
            password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.",
            verification_code=111111)]
    commit()
    if spell == 'Imperio' or spell == "Crucio":
        lobby = Lobby(
            name="mortifagos 4ever",
            max_players=7,
            owner_id=users[0].id)
    else:
        lobby = Lobby(
            name="mortifagos 4ever",
            max_players=5,
            owner_id=users[0].id)

    if spell == "Divination":
        create_players(users=users[:5], lobby=lobby, player_amount=5)
        game = Game(
            lobby=lobby,
            in_session=True,
            minister_proclaimed=True,
            director_proclaimed=True,
            last_proc_negative=True)

        create_cards(game=game)
    elif spell == "Avada Kedavra":
        create_players(users=users[:5], lobby=lobby, player_amount=5)
        game = Game(
            lobby=lobby,
            in_session=True,
            minister_proclaimed=True,
            director_proclaimed=True,
            last_proc_negative=True)

        create_cards_avada_kedavra(game=game)
    elif spell == "Imperio":
        create_players(users=users, lobby=lobby, player_amount=7)
        game = Game(
            lobby=lobby,
            in_session=True,
            minister_proclaimed=True,
            director_proclaimed=True,
            last_proc_negative=True)

        create_cards_imperio(game=game)
    elif spell == "Crucio":
        create_players(users=users, lobby=lobby, player_amount=7)
        game = Game(
            lobby=lobby,
            in_session=True,
            minister_proclaimed=True,
            director_proclaimed=True,
            last_proc_negative=True)

        create_cards_crucio(game=game)
    commit()
