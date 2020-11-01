from app.database.models import *
from app.api.schemas import *


@db_session
def set_db_for_procl():
    user1 = User(email="maw@gmail.com", username="maw",
                 # password = password
                 password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.")
    user2 = User(email="law@gmail.com", username="law",
                 password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.")
    user3 = User(email="lau@gmail.com", username="lau",
                 password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.")
    user4 = User(email="ulince@gmail.com", username="ulince",
                 password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.")
    user5 = User(email="nico@gmail.com", username="nico",
                 password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.")

    lobby1 = Lobby(name="mortifagos 4ever", max_players=5)
    # Set the game so that the director can get and post the cards to proclaim
    game1 = Game(lobby=lobby1, voting=False, semaphore=0,
                 in_session=True, minister_proclaimed=True)

    for i in range(17):
        if i in [1, 2]:
            c = ProcCard(game=game1, discarded=False, selected=True,
                         position=i, phoenix=(i == 1))
        else:
            c = ProcCard(game=game1, discarded=False,
                         position=i, phoenix=(i < 7))

    role_vol = GRole(voldemort=True, phoenix=False)
    role_dea = GRole(voldemort=False, phoenix=False)
    role_ord = GRole(voldemort=False, phoenix=True)

    p1 = Player(position=1, user=user1, lobby=lobby1,
                role=role_vol, minister=True, director=False)
    p2 = Player(position=2, user=user2, lobby=lobby1,
                role=role_dea, minister=False, director=True)
    p3 = Player(position=3, user=user3, lobby=lobby1,
                role=role_ord, prev_minister=True, director=False)
    p4 = Player(position=4, user=user4, lobby=lobby1,
                role=role_ord, minister=False, prev_director=True)
    p5 = Player(position=5, user=user5, lobby=lobby1,
                role=role_ord, minister=False, director=False)
    commit()
