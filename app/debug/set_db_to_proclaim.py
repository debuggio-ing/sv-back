from app.database.binder import *


@db_session
def db_to_proclaim():
    user1 = User(
        email="maw@gmail.com",
        nickname="maw",
        password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.",
        verification_code=111111)
    user2 = User(
        email="law@gmail.com",
        nickname="law",
        password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.",
        verification_code=111111)
    user3 = User(
        email="lau@gmail.com",
        nickname="lau",
        password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.",
        verification_code=111111)
    user4 = User(
        email="ulince@gmail.com",
        nickname="ulince",
        password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.",
        verification_code=111111)
    user5 = User(
        email="nico@gmail.com",
        nickname="nico",
        password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.",
        verification_code=111111)
    commit()
    lobby1 = Lobby(name="mortifagos 4ever", max_players=5, owner_id=user1.id)

    # set game so that the minister can discard a card
    game1 = Game(lobby=lobby1, in_session=True)

    # create and select the first three cards
    for i in range(17):
        if i in [0, 1, 2]:
            c = ProcCard(game=game1, discarded=False, selected=True,
                         position=i, phoenix=(i <= 1))
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
                role=role_ord, minister=False, prev_director=False)
    p5 = Player(position=5, user=user5, lobby=lobby1,
                role=role_ord, minister=False, director=False)
    commit()
