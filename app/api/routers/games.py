from app.api.routers_helpers.game_helper import *

r = games_router = APIRouter()


# List games in database
@r.get("/games/")
def get_game_list(game_from: Optional[int] = 0, game_to: Optional[int] = None, auth: AuthJWT = Depends()):
    user_email = validate_user(auth=auth)

    game_id_list = get_all_games_ids(game_from, game_to)
    # generate game list
    games = []
    for gid in game_id_list:
        pid = get_player_id(user_email, gid)
        game = get_game_public_info(gid, pid)
        games.append(game)

    return games


# View public data about a specified game
@r.get("/games/{game_id}/", response_model=GamePublic)
def get_game(game_id: int, auth: AuthJWT = Depends()):
    user_email = validate_user(auth=auth)

    # get the id of the user in the game (player_id)
    player_id = get_player_id(user_email, game_id)

    return get_game_public_info(gid=game_id, pid=player_id)


# Player votes in the specified game
@r.post("/games/{game_id}/vote/")
def player_vote(game_id: int, vote: PlayerVote, auth: AuthJWT = Depends()):
    email = validate_user(auth=auth)
    player_id = get_player(email=email, game_id=game_id)

    # check if there's a vote occurring in the game
    if not currently_voting(game_id):
        raise HTTPException(
            status_code=403, detail='There isn\'t a vote ocurring')

    # cast vote
    if is_last_vote(player_id, game_id):
        set_last_player_vote(player_id, game_id, vote.vote)
    else:
        set_player_vote(player_id, game_id, vote.vote)
    return 1


# Return player's role in the specified game
@r.get("/games/{game_id}/role/", response_model=PlayerRole)
def get_player_role(game_id: int, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return


# Cast spell in specified game
@r.post("/games/{game_id}/spell/")
def cast_spell(game_id: int, spell: CastSpell, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return


# Return to the director the cards selected by the minister
@r.get("/games/{game_id}/dir/proc/")
def get_director_proc(game_id: int, auth: AuthJWT = Depends()):
    user_email = validate_user(auth=auth)

    player_id = get_player(email=user_email, game_id=game_id)

    is_dir_proc_time(game_id=game_id, player_id=player_id)

    # get the cards selected by the minister
    selected_cards = get_selected_cards(game_id)
    cards = []
    for card in selected_cards:
        cards.append(CardToProclaim(
            card_pos=card.position, phoenix=card.phoenix))

    return cards


# Director chooses the cards to proclaim
# At this point expelliarmus is not implemented
# Returns True if game continues or False if game is over
@r.post("/games/{game_id}/dir/proc/", response_model=bool)
def proc_election(
        game_id: int,
        election: LegislativeSession,
        auth: AuthJWT = Depends()):
    email = validate_user(auth=auth)

    player_id = get_player(email=email, game_id=game_id)

    # check if it's time for a director to choose
    is_dir_proc_time(game_id=game_id, player_id=player_id)

    # check if the received proclamation is valid
    proclamation_count = sum(
        map(lambda c: c.to_proclaim, election.proclamation))
    if proclamation_count != 1 or len(election.proclamation) != 2:
        raise HTTPException(
            status_code=401, detail='Invalid selection of cards')

    # proclaim card if it's not proclaimed
    if not proclaim_card(election.proclamation, game_id):
        raise HTTPException(
            status_code=401, detail='Invalid selection of cards')

    # finish legislative session and release the director
    finish_legislative_session(game_id)
    discharge_director(player_id)

    return is_game_over(game_id)


# Nominate director in specified game
@r.post("/games/{game_id}/director/{candidate_id}/")
def director_candidate(
        game_id: int,
        candidate_id: int,
        auth: AuthJWT = Depends()):
    email = validate_user(auth=auth)

    player_id = get_player(email=email, game_id=game_id)

    can_propose_gvt(game_id=game_id, player_id=player_id)

    propose_government(game_id=game_id, dir_id=candidate_id)
