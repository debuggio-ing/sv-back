from app.database.crud import *
from fastapi_jwt_auth import AuthJWT
from fastapi import HTTPException, Depends


# Checks if the user is properly validated and returns its email or raises an exception
def validate_user(auth: AuthJWT = Depends()):
    # check if token is valid
    auth.jwt_required()

    # get user's email
    user_email = auth.get_jwt_identity()
    if user_email is None:
        raise HTTPException(status_code=409, detail='Corrupted JWT')
    return user_email


# Gets player from game and returns its id or raises and exception
def get_player(email: str, game_id: int):
    player_id = get_player_id(email, game_id)
    if player_id == -1:
        raise HTTPException(status_code=401, detail='User not in game')
    return player_id


# Check if game is over
def is_game_over(game_id):
    score = get_game_score(game_id)
    return score.good == 5 or score.bad == 6


# Checks if director or user can proclaim a card. It raises an exception on failure
def is_dir_proc_time(game_id: int, player_id: int):
    # check if it's time for a director to choose
    if not director_chooses_proc(game_id):
        raise HTTPException(status_code=401, detail='It\'s not time to choose')

    # check if the player is the director
    if not is_director(player_id):
        raise HTTPException(status_code=401, detail='Player isn\'nt director')


# Checks if the player can propose and if it's time to select a government
# Raises exception on failure
def can_propose_gvt(game_id: int, player_id: int):
    # check if the player is the minister
    if not get_game_minister_id(game_id) == player_id:
        raise HTTPException(
            status_code=409, detail='You are not the minister!')

    # check if it's time to propose a government
    if not goverment_proposal_needed(game_id):
        raise HTTPException(
            status_code=409, detail='It\'s not time to select a government')
