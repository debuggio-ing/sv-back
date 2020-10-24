from pony.orm import *
from app.database.models import *
from app.api.schemas import *
from app.api.hasher import *




db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)


# Insert user into the database.
@db_session
def register_user(user: UserReg) -> int:

    guser = User.get(email=user.email)
    if guser is not None:
        return -1

    u = User(email=user.email, username=user.username, password=encrypt_password(user.password))
    commit()
    return u.id

@db_session
def get_password_hash(uemail:str) -> str:
    phash = list(select(u.password for u in User if u.email == uemail))
    return phash[0]

# Get all users from the database.
@db_session
def get_users_for_login():
    users = dict(select((u.email, u.password) for u in User))
    return users

# Get all emails from the database.
@db_session
def get_emails():
    emails = list(select(u.email for u in User))
    return emails

@db_session
def get_player_id(user_email: str, game_id: int):
    

    user = User.get(email=user_email)
    lobby = Lobby.get(id=game_id)

    player = Player.get(user=user, lobby=lobby)

    pid = -1
    if  player is not None:
        pid = player.id

    return pid

@db_session
def currently_voting(game_id: int):

    lobby = Lobby.get(id=game_id)
    return lobby.game.voting

@db_session
def is_last_vote(player_id: int, game_id: int):

    lobby = Lobby.get(id=game_id)
    game = lobby.game
    player = Player.get(id=player_id)
    max_players = lobby.max_players

    current_votes = lobby.game.numv
    already_vote = CurrentVote.get(voter_id=player_id)

    if already_vote is None:
        current_votes += 1

    return current_votes == max_players

@db_session
def set_last_player_vote(player_id: int, game_id: int, vote: bool):

    set_player_vote(player_id, game_id, vote)
    update_public_vote(game_id)
    clean_current_vote(game_id)
 
    commit()


@db_session
def set_player_vote(player_id: int, game_id: int, vote: bool):
    

    player = Player.get(id=player_id, lobby=game_id)
    lobby = Lobby.get(id=game_id)
    game = lobby.game

    if player.curr_vote is None:
        player.curr_vote = CurrentVote(game=game, player=player, vote=vote, voter_id=player_id)
        lobby.game.numv += 1
    else:
        player.curr_vote.vote = vote
        
    commit()

@db_session
def update_public_vote(game_id: int):

    lobby = Lobby.get(id=game_id)
    game = lobby.game

    delete(v for v in PublicVote)
    votes = (select((v.vote, v.voter_id) for v in CurrentVote))[:]
    for v in votes:
        pv = PublicVote(game=game, vote=v[0], voter_id=v[1])

    lobby.game.voting = False
    commit()

@db_session
def clean_current_vote(game_id: int):
    
    lob = Lobby.get(id=game_id)

    delete(v for v in CurrentVote)

    lob.game.numv = 0
    #delete(lobby.game.curr_vote.id for lobby in Lobby if lobby.id == game_id)
    commit()


@db_session
def populate_test_db():
    user1 = User(email="maw1@gmail.com", username="maw", password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.")
    user2 = User(email="law@gmail.com", username="law", password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.")
    user3 = User(email="lau@gmail.com", username="lau", password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.")
    user4 = User(email="ulince@gmail.com", username="ulince", password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.")
    user5 = User(email="nico@gmail.com", username="nico", password="$5$rounds=535000$hN.xjQV17DkWk3zX$cDFQJeakbvfB6Fn.5mB/XnSS/xjrplJ./7rh.I33Ss.")
    lobby1 = Lobby(name="mortifagos 4ever", max_players=5)
    lobby2 = Lobby(name="larga vida harry", max_players=5)
    lobby3 = Lobby(name="tom laura riddle", max_players=5)
   
    game1 = Game(lobby=lobby1, voting=True, semaphore=0, numv=3)
    role_vol = GRole(voldemort=True, phoenix=False)
    role_dea = GRole(voldemort=False, phoenix=False)
    role_ord = GRole(voldemort=False, phoenix=True)

    p1 = Player(position=1,user=user1, lobby=lobby1, role=role_vol, minister=False, director=False)
    p2 = Player(position=2,user=user2, lobby=lobby1, role=role_dea, minister=False, director=False)
    p3 = Player(position=3,user=user3, lobby=lobby1, role=role_ord, minister=False, director=False)
    p4 = Player(position=4,user=user4, lobby=lobby1, role=role_ord, minister=False, director=False)
    p5 = Player(position=5,user=user5, lobby=lobby1, role=role_ord, minister=False, director=False)

    curr_vote1 = CurrentVote(game=game1, player=p1, vote=True, voter_id=1)
    curr_vote3 = CurrentVote(game=game1, player=p3, vote=True, voter_id=3)
    curr_vote4 = CurrentVote(game=game1, player=p4, vote=True, voter_id=4)

    #last_vote1 = 
    last_vote1 = PublicVote(game=game1, player=p1, vote=True, voter_id=1)
    last_vote2 = PublicVote(game=game1, player=p2, vote=True, voter_id=2)
    last_vote3 = PublicVote(game=game1, player=p3, vote=True, voter_id=3)
    last_vote4 = PublicVote(game=game1, player=p4, vote=True, voter_id=4)
    last_vote4 = PublicVote(game=game1, player=p5, vote=True, voter_id=5)


@db_session
def delete_db():
    db.drop_all_tables(with_all_data=True)
    db.create_tables()