from app.database.models import *
from app.api.schemas import *
from app.database.crud_helpers.user import *

import random

@db_session
def populate_test_db():
    user1 = User(
        email="maw@gmail.com",
        username="maw",
        #password = password
        password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.")
    user2 = User(
        email="law@gmail.com",
        username="law",
        password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.")
    user3 = User(
        email="lau@gmail.com",
        username="lau",
        password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.")
    user4 = User(
        email="ulince@gmail.com",
        username="ulince",
        password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.")
    user5 = User(
        email="nico@gmail.com",
        username="nico",
        password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.")

    user_id = 1 # cant use get_user_id(user1.email) because is not stored on the db.

    lobby1 = Lobby(name="mortifagos 4ever", max_players=5, owner_id=user_id)
    lobby2 = Lobby(name="larga vida harry", max_players=5, owner_id=user_id)
    lobby3 = Lobby(name="tom laura riddle", max_players=5, owner_id=user_id)

    game1 = Game(lobby=lobby1, voting=True, semaphore=0, num_votes=3, list_head=2)
    game2 = Game(lobby=lobby2, voting=False, in_session=False, semaphore=0, num_votes=3, list_head=2)

    positions = list(range(17))
    random.shuffle(positions)
    card_pool = []
    for i in range(17):
        c = ProcCard(game=game1, discarded=False, position=positions[i], phoenix=(i < 6))
        c = ProcCard(game=game2, discarded=False, position=positions[i], phoenix=(i < 6))
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

    curr_vote1 = CurrentVote(game=game1, player=p1, vote=True, voter_id=1)
    curr_vote3 = CurrentVote(game=game1, player=p3, vote=True, voter_id=3)
    curr_vote4 = CurrentVote(game=game1, player=p4, vote=True, voter_id=4)

    curr_vote2 = CurrentVote(game=game2, player=p6, vote=True, voter_id=6)
    curr_vote6 = CurrentVote(game=game2, player=p8, vote=True, voter_id=8)
    curr_vote8 = CurrentVote(game=game2, player=p9, vote=True, voter_id=9)

    last_vote1 = PublicVote(game=game1, player=p1, vote=True, voter_id=1)
    last_vote2 = PublicVote(game=game1, player=p2, vote=True, voter_id=2)
    last_vote3 = PublicVote(game=game1, player=p3, vote=True, voter_id=3)
    last_vote4 = PublicVote(game=game1, player=p4, vote=True, voter_id=4)
    last_vote4 = PublicVote(game=game1, player=p5, vote=True, voter_id=5)

    last_vote10 = PublicVote(game=game2, player=p6, vote=True, voter_id=6)
    last_vote20 = PublicVote(game=game2, player=p7, vote=True, voter_id=7)
    last_vote30 = PublicVote(game=game2, player=p8, vote=True, voter_id=8)
    last_vote40 = PublicVote(game=game2, player=p9, vote=True, voter_id=9)
    last_vote40 = PublicVote(game=game2, player=p10, vote=True, voter_id=10)
