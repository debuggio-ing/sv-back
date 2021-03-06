from app.database.binder import *

import random


@db_session
def populate_test_db():
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
    lobby2 = Lobby(name="larga vida harry", max_players=5, owner_id=user_id)
    lobby3 = Lobby(name="tom laura riddle", max_players=5, owner_id=user_id)

    game1 = Game(lobby=lobby1, voting=True,
                 semaphore=0, num_votes=3, list_head=2)
    game2 = Game(lobby=lobby2, voting=False, in_session=False,
                 semaphore=0, num_votes=3, list_head=2)

    positions = list(range(17))
    random.shuffle(positions)
    card_pool = []
    for i in range(17):
        c = ProcCard(game=game1, discarded=False,
                     position=positions[i], phoenix=(i < 6))
        c = ProcCard(game=game2, discarded=False,
                     position=positions[i], phoenix=(i < 6))
        card_pool.append(c)

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

    p6 = Player(
        position=1,
        user=user1,
        lobby=lobby2,
        role=role_vol,
        minister=True,
        director=False)
    p7 = Player(
        position=2,
        user=user2,
        lobby=lobby2,
        role=role_dea,
        minister=False,
        director=False)
    p8 = Player(
        position=3,
        user=user3,
        lobby=lobby2,
        role=role_ord,
        prev_minister=True,
        director=False)
    p9 = Player(
        position=4,
        user=user4,
        lobby=lobby2,
        role=role_ord,
        minister=False,
        prev_director=True)
    p10 = Player(
        position=5,
        user=user5,
        lobby=lobby2,
        role=role_ord,
        minister=False,
        director=False)
    commit()

    curr_vote1 = CurrentVote(
        game=game1.id, player=p1.id, vote=True, voter_id=1)
    curr_vote3 = CurrentVote(
        game=game1.id, player=p3.id, vote=True, voter_id=3)
    curr_vote4 = CurrentVote(
        game=game1.id, player=p4.id, vote=True, voter_id=4)

    curr_vote6 = CurrentVote(
        game=game2.id, player=p6.id, vote=True, voter_id=6)
    curr_vote8 = CurrentVote(
        game=game2.id, player=p8.id, vote=True, voter_id=8)
    curr_vote9 = CurrentVote(
        game=game2.id, player=p9.id, vote=True, voter_id=9)

    last_vote1 = PublicVote(game=game1.id, player=p1.id, vote=True, voter_id=1)
    last_vote2 = PublicVote(game=game1.id, player=p2.id, vote=True, voter_id=2)
    last_vote3 = PublicVote(game=game1.id, player=p3.id, vote=True, voter_id=3)
    last_vote4 = PublicVote(game=game1.id, player=p4.id, vote=True, voter_id=4)
    last_vote4 = PublicVote(game=game1.id, player=p5.id, vote=True, voter_id=5)

    last_vote10 = PublicVote(
        game=game2.id, player=p6.id, vote=True, voter_id=6)
    last_vote20 = PublicVote(
        game=game2.id, player=p7.id, vote=True, voter_id=7)
    last_vote30 = PublicVote(
        game=game2.id, player=p8.id, vote=True, voter_id=8)
    last_vote40 = PublicVote(
        game=game2.id, player=p9.id, vote=True, voter_id=9)
    last_vote40 = PublicVote(
        game=game2.id, player=p10.id, vote=True, voter_id=10)
