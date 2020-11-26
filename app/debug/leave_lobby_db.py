from app.database.binder import *

import random


@db_session
def caos_db():
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

    # cant use get_user_id(user1.email) because is not stored on the db.
    user_id = 1

    lobby1 = Lobby(name="mortifagos 4ever", max_players=5, owner_id=user_id)

    role_vol = GRole(voldemort=True, phoenix=False)
    role_dea = GRole(voldemort=False, phoenix=False)
    role_ord = GRole(voldemort=False, phoenix=True)

    p1 = Player(
        position=1,
        user=user1,
        lobby=lobby1,
        role=role_vol,
        minister=True,
        director=False)
    p2 = Player(
        position=2,
        user=user2,
        lobby=lobby1,
        role=role_dea,
        minister=False,
        director=True)
    p3 = Player(
        position=3,
        user=user3,
        lobby=lobby1,
        role=role_ord,
        prev_minister=True,
        director=False)
    p4 = Player(
        position=4,
        user=user4,
        lobby=lobby1,
        role=role_ord,
        minister=False,
        prev_director=True)
    p5 = Player(
        position=5,
        user=user5,
        lobby=lobby1,
        role=role_ord,
        minister=False,
        director=False)
    commit()
