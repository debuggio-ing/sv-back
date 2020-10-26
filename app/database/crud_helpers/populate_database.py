from app.database.models import *
from app.api.schemas import *


@db_session
def populate_test_db():
    user1 = User(
        email="maw1@gmail.com",
        username="maw",
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

    lobby1 = Lobby(name="mortifagos 4ever", max_players=5)
    lobby2 = Lobby(name="larga vida harry", max_players=5)
    lobby3 = Lobby(name="tom laura riddle", max_players=5)

    game1 = Game(lobby=lobby1, voting=True, semaphore=0, numv=3)

    role_vol = GRole(voldemort=True, phoenix=False)
    role_dea = GRole(voldemort=False, phoenix=False)
    role_ord = GRole(voldemort=False, phoenix=True)

    p1 = Player(
        position=1,
        user=user1,
        lobby=lobby1,
        role=role_vol,
        minister=False,
        director=False)
    p2 = Player(
        position=2,
        user=user2,
        lobby=lobby1,
        role=role_dea,
        minister=False,
        director=False)
    p3 = Player(
        position=3,
        user=user3,
        lobby=lobby1,
        role=role_ord,
        minister=False,
        director=False)
    p4 = Player(
        position=4,
        user=user4,
        lobby=lobby1,
        role=role_ord,
        minister=False,
        director=False)
    p5 = Player(
        position=5,
        user=user5,
        lobby=lobby1,
        role=role_ord,
        minister=False,
        director=False)

    curr_vote1 = CurrentVote(game=game1, player=p1, vote=True, voter_id=1)
    curr_vote3 = CurrentVote(game=game1, player=p3, vote=True, voter_id=3)
    curr_vote4 = CurrentVote(game=game1, player=p4, vote=True, voter_id=4)

    last_vote1 = PublicVote(game=game1, player=p1, vote=True, voter_id=1)
    last_vote2 = PublicVote(game=game1, player=p2, vote=True, voter_id=2)
    last_vote3 = PublicVote(game=game1, player=p3, vote=True, voter_id=3)
    last_vote4 = PublicVote(game=game1, player=p4, vote=True, voter_id=4)
    last_vote4 = PublicVote(game=game1, player=p5, vote=True, voter_id=5)


@db_session
def delete_db():
    delete(r for r in GRole)
    delete(g for g in Game)
    delete(l for l in Lobby)
    delete(u for u in User)
    delete(p for p in Player)
    delete(v for v in PublicVote)
    delete(v for v in CurrentVote)
