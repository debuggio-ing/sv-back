from fastapi import APIRouter

from app.crud.chat import *
from app.validators.auth_validator import *
from app.validators.game_validator import *

r = games_router = APIRouter()


# List games in database
@r.get("/games/", response_model=List[LobbyPublic])
def get_game_list(
        game_from: Optional[int] = 0,
        game_to: Optional[int] = None,
        auth: AuthJWT = Depends()):
    user_email = validate_user(auth=auth)

    game_id_list = get_all_games_ids(game_from=game_from, game_to=game_to)
    # generate game list
    games = []
    for game_id in game_id_list:
        game = get_lobby_public_info(lobby_id=game_id, user_email=user_email)
        games.append(game)

    return games


# View public data about a specified game
@r.get("/games/{game_id}/", response_model=GamePublic)
def get_game(game_id: int, auth: AuthJWT = Depends()):
    user_email = validate_user(auth=auth)

    # get the id of the user in the game (player_id)
    player_id = get_player_id(user_email, game_id)

    return get_game_public_info(game_id=game_id, player_id=player_id)


# Player votes in the specified game
@r.post("/games/{game_id}/vote/")
def player_vote(game_id: int, vote: PlayerVote, auth: AuthJWT = Depends()):
    email = validate_user(auth=auth)
    player_id = get_player(email=email, game_id=game_id)

    # check if there's a vote occurring in the game
    in_voting_phase(game_id)

    # check if player is dead
    is_player_dead(player_id=player_id)

    # cast vote
    if is_last_vote(player_id, game_id):
        set_last_player_vote(player_id, game_id, vote.vote)
    else:
        set_player_vote(player_id, game_id, vote.vote)
    return 1


# Cast spell in specified game
@r.post("/games/{game_id}/spell/")
def post_cast_spell(game_id: int, spell: CastSpell, auth: AuthJWT = Depends()):
    email = validate_user(auth=auth)

    # check user in game
    player_id = get_player(email=email, game_id=game_id)

    # check if player is minister
    is_player_minister(player_id=player_id)

    # check if game state is correct
    in_casting_phase(game_id=game_id)

    # check if target is dead
    if spell.target != -1:
        is_player_in_game(player_id=player_id, game_id=game_id)
        is_player_dead(player_id=spell.target)

    # execute spell
    return cast_spell(game_id=game_id, target=spell.target)


# Get information to cast spell in specified game
@r.get("/games/{game_id}/spell/", response_model=Spell)
def get_cast_spell(game_id: int, auth: AuthJWT = Depends()):
    email = validate_user(auth=auth)

    # check gid correct
    # check user in game
    player_id = get_player(email=email, game_id=game_id)

    # check if player is minister
    is_player_minister(player_id=player_id)

    # check if game state is correct
    in_casting_phase(game_id=game_id)

    # cast spell(send spell)
    return get_spell(game_id=game_id)


# Return to the minister/director the selected cards according to the game
# status
@r.get("/games/{game_id}/proc/", response_model=List[CardToProclaim])
def get_proclamations(game_id: int, auth: AuthJWT = Depends()):
    user_email = validate_user(auth=auth)

    player_id = get_player(email=user_email, game_id=game_id)
    cards = []
    if is_min_proc_time(
            game_id=game_id,
            player_id=player_id) or is_dir_proc_time(
            game_id=game_id,
            player_id=player_id):
        selected_cards = get_selected_cards(game_id=game_id)
        for card in selected_cards:
            cards.append(CardToProclaim(
                card_pos=card.position, phoenix=card.phoenix))
    else:
        raise HTTPException(status_code=401, detail='User not allowed')
    return cards


@r.post("/games/{game_id}/proc/", response_model=bool)
def post_proclamations(
        game_id: int,
        legislation: Legislation,
        auth: AuthJWT = Depends()):
    email = validate_user(auth=auth)

    player_id = get_player(email=email, game_id=game_id)
    # if expelliarmus is asked
    if legislation.expelliarmus:
        # check if minister an cast expelliarmus spell
        if is_min_expelliarmus_time(game_id=game_id, player_id=player_id):
            # cast expelliarmus
            cast_expelliarmus(game_id=game_id)
        # check if director can ask for expelliarmus spell
        elif is_dir_expelliarmus_time(game_id=game_id, player_id=player_id):
            # ask minister for expelliarmus
            director_ask_expelliarmus(game_id=game_id)
    else:
        # check if minister didn't accept expelliarmus request
        if get_expelliarmus(game_id=game_id) and get_is_player_minister(
                player_id=player_id):
            reject_expelliarmus(game_id=game_id, player_id=player_id)

        # check if minister or director can proclaim/discard and the player's
        # role
        elif is_min_proc_time(game_id=game_id, player_id=player_id):
            # minister discard the selected card
            minister_discards(election=legislation.election, game_id=game_id)
            # update game status
            finish_minister_proclamation(game_id=game_id)

        # raise exceptions
        elif is_dir_proc_time(game_id=game_id, player_id=player_id):
            # director proclaims the selected cards
            director_proclaims(election=legislation.election, game_id=game_id)
            # update game status and card deck
            finish_director_proclamation(game_id=game_id)

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

    # is candidate in game
    is_player_in_game(player_id=candidate_id, game_id=game_id)

    # is candidate alive
    is_player_dead(player_id=candidate_id)

    is_player_electable(player_id=candidate_id, game_id=game_id)

    propose_government(game_id=game_id, dir_id=candidate_id)


# Nominate director in specified game
@r.post("/games/{game_id}/chat/send/")
def send_message(game_id: int, msg: MessageIn, auth: AuthJWT = Depends()):
    email = validate_user(auth=auth)

    player_id = get_player(email=email, game_id=game_id)

    # is player in game
    is_player_in_game(player_id=player_id, game_id=game_id)

    # is player alive
    is_player_dead(player_id=player_id)

    insert_message(player_id=player_id, message=msg.msg)
    return msg
