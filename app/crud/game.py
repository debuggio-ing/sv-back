from app.crud.card import *
from app.crud.lobby import *
from app.crud.player import *
from app.crud.chat import *
from app.validators.constants import *


# Create game in the database.
@db_session
def insert_game(lobby_id: int) -> int:
    lobby = Lobby.get(id=lobby_id)

    max_players = select(p for p in Player if p.lobby.id == lobby_id).count()
    ultra_random_number = random.randint(0, 4)

    player_order = [i for i in range(max_players)]
    random.shuffle(player_order)

    cards = list(i < NUM_PHOENIX_CARDS for i in range(PROC_CARD_NUMBER))
    random.shuffle(cards)

    game_id = -1
    if lobby is not None:
        game = Game(lobby=lobby)

        player_ids = get_lobby_players_id(lobby.id)

        # Set player order
        for i, pid in enumerate(player_ids):
            player = Player.get(id=pid)
            player.position = player_order[i]

        # Set first player of the list
        game.list_head = ultra_random_number

        # create proclamation cards.
        for i in range(PROC_CARD_NUMBER):
            ProcCard(position=i, phoenix=cards[i], game=game)

        # choose who will be and death eaters.
        death_eaters = random.sample(
            range(
                len(player_ids)),
            NUM_DEATH_EATERS[max_players])

        # set roles.
        set_phoenixes([player_ids[i]
                       for i in range(len(player_ids)) if i not in death_eaters])
        set_death_eaters(list(player_ids[i] for i in death_eaters[1:]))
        set_voldemort(player_ids[death_eaters[0]])

        # set first minister of magic.
        set_minister_of_magic(player_ids[ultra_random_number])
        game.list_head = ((game.list_head + 1) % max_players)

        commit()
        game_id = game.id

    return game_id


# Return the required game status.
@db_session
def get_game_public_info(game_id: int, player_id: int):
    if get_game_ended(game_id=game_id):

        # end: Optional[bool]
        # winners: Optional[bool]
        # # players' role reaveal party at the end of the game
        # roleReveal: Optional[List[Role]]
        return GamePublic(
            id=game_id,
            player_list=get_game_player_public_list(
                game_id=game_id,
                c_player_id=player_id),
            minister=get_game_minister_id(game_id=game_id),
            prev_minister=get_game_prev_minister_id(game_id=game_id),
            director=get_game_director_id(game_id=game_id),
            prev_director=get_game_prev_director_id(game_id=game_id),
            semaphore=get_game_semaphore(game_id=game_id),
            discarded=get_discarded_cards(game_id=game_id),
            score=get_game_score(game_id=game_id),
            voting=get_game_voting(game_id=game_id),
            in_crucio=get_in_crucio(game_id=game_id),
            expelliarmus=get_expelliarmus(game_id=game_id),
            in_session=get_game_in_session(game_id=game_id),
            minister_proclaimed=get_game_minister_proclaimed(game_id=game_id),
            director_proclaimed=get_director_proclaimed(game_id=game_id),
            last_proc_negative=get_last_proc_negative(game_id=game_id),
            client_minister=get_is_player_minister(player_id=player_id),
            client_director=is_player_director(player_id=player_id),
            messages=get_messages(id=game_id),
            end=True,
            phoenix_win=get_game_phoenix_win(game_id=game_id))
    else:
        return GamePublic(
            id=game_id,
            player_list=get_game_player_public_list(
                game_id=game_id,
                c_player_id=player_id),
            minister=get_game_minister_id(game_id=game_id),
            prev_minister=get_game_prev_minister_id(game_id=game_id),
            director=get_game_director_id(game_id=game_id),
            prev_director=get_game_prev_director_id(game_id=game_id),
            semaphore=get_game_semaphore(game_id=game_id),
            discarded=get_discarded_cards(game_id=game_id),
            score=get_game_score(game_id=game_id),
            voting=get_game_voting(game_id=game_id),
            in_crucio=get_in_crucio(game_id=game_id),
            expelliarmus=get_expelliarmus(game_id=game_id),
            in_session=get_game_in_session(game_id=game_id),
            minister_proclaimed=get_game_minister_proclaimed(game_id=game_id),
            director_proclaimed=get_director_proclaimed(game_id=game_id),
            last_proc_negative=get_last_proc_negative(game_id=game_id),
            client_minister=get_is_player_minister(player_id=player_id),
            client_director=is_player_director(player_id=player_id),
            messages=get_messages(id=game_id))


# Returns true if pid is minister.
@db_session
def get_is_player_minister(player_id: int) -> bool:
    player = Player.get(id=player_id)
    if player:
        return player.minister
    else:
        return False


# Returns true if pid is director.
@db_session
def is_player_director(player_id: int) -> bool:
    player = Player.get(id=player_id)
    if player:
        return player.director
    else:
        return False

# Returns all game's ids
@db_session
def get_all_games_ids(game_from: int, game_to: int) -> List[int]:
    return list(select(g.id for g in Game if not g.ended))


# Return a list of all players in gid game with the information of concern
# to c_pid (callers_player_id).
@db_session
def get_game_player_public_list(
        game_id: int,
        c_player_id: int) -> List[PlayerPublic]:
    player_list = list(
        select(
            p for p in Player if game_id == p.lobby.id).order_by(
            lambda p: p.position))
    pid_list = map(lambda p: p.id, player_list)

    players = [get_player_public(player_id, c_player_id)
               for player_id in pid_list]

    return players


# Returns the nickname of the game's minister.
@db_session
def get_game_minister_nickname(game_id: int) -> int:
    minister = Player.get(lobby=game_id, minister=True)

    minister_nickname = -1
    if minister is not None:
        minister_nickname = minister.user.nickname

    return minister_nickname


# Returns the nickname of the game's director.
@db_session
def get_game_director_nickname(game_id: int) -> int:
    director = Player.get(lobby=game_id, director=True)

    director_nickname = -1
    if director is not None:
        director_nickname = director.user.nickname

    return director_nickname


# Returns the id of the game's minister.
@db_session
def get_game_minister_id(game_id: int) -> int:
    minister = Player.get(lobby=game_id, minister=True)

    minister_id = -1
    if minister is not None:
        minister_id = minister.id

    return minister_id


# Returns the id of the game's director.
@db_session
def get_game_director_id(game_id: int) -> int:
    director = Player.get(lobby=game_id, director=True)

    director_id = -1
    if director is not None:
        director_id = director.id

    return director_id


# Returns the id of the game's previous minister.
@db_session
def get_game_prev_minister_id(game_id: int) -> int:
    prev_minister = Player.get(lobby=game_id, prev_minister=True)

    prev_minister_id = -1
    if prev_minister is not None:
        prev_minister_id = prev_minister.id

    return prev_minister_id


# Get previous director's player_id
@db_session
def get_game_prev_director_id(game_id: int) -> int:
    prev_director = Player.get(lobby=game_id, prev_director=True)

    prev_director_id = -1
    if prev_director is not None:
        prev_director_id = prev_director.id

    return prev_director_id


# Get game's semaphore
@db_session
def get_game_semaphore(game_id: int) -> int:
    lobby = Lobby.get(id=game_id)

    sem = -1
    if lobby is not None and lobby.game is not None:
        sem = lobby.game.semaphore

    return sem


# Check if the game is in election
@db_session
def get_game_voting(game_id) -> bool:
    game = Lobby.get(id=game_id).game

    ans = False
    if game is not None:
        ans = game.voting

    return ans


# Check if game is in legislative session
@db_session
def get_game_in_session(game_id) -> bool:
    game = Lobby.get(id=game_id).game

    ans = False
    if game is not None:
        ans = game.in_session

    return ans


# Check if director asked for expelliarmus
@db_session
def get_expelliarmus(game_id: int) -> bool:
    lobby = Lobby.get(id=game_id)
    return lobby and lobby.game and lobby.game.expelliarmus


# Check if the game is in a crucio torture
@db_session
def get_in_crucio(game_id: int) -> bool:
    lobby = Lobby.get(id=game_id)
    return lobby and lobby.game and lobby.game.in_crucio


# Returns a list of the tortured players
@db_session
def get_crucied_players(game_id: int):
    return list(
        select(
            p for p in Player if p.lobby.id == game_id and p.crucied))


# Check if the minister has already proclaimed cards
@db_session
def get_game_minister_proclaimed(game_id) -> bool:
    game = Lobby.get(id=game_id).game

    ans = False
    if game is not None:
        ans = game.minister_proclaimed

    return ans


# Ends expelliarmus and legislative session with it
@db_session
def end_expelliarmus(game_id: int):
    discharge_director(game_id=game_id)
    finish_legislative_session(game_id=game_id, imperio=False)
    commit()


# Get game's total proclaimed cards (phoenix = good, death eaters = bad)
@db_session
def get_game_score(game_id: int) -> Score:
    lobby = Lobby.get(id=game_id)

    bad_score = 0
    good_score = 0
    if lobby is not None and lobby.game is not None:
        card_pool = select(c for c in lobby.game.cards)

        bad_score = len(
            select(
                c for c in card_pool if c.proclaimed and c.phoenix == False))
        good_score = len(
            select(
                c for c in card_pool if c.proclaimed and c.phoenix))

    return Score(good=good_score, bad=bad_score)


# Check if it's time for a government proposal
@db_session
def goverment_proposal_needed(game_id: int) -> bool:
    game = Lobby.get(id=game_id).game

    ans = False
    if game is not None:
        ans = not game.voting and not game.in_session

    return ans


# Purpose a director specified by the user id dir_id
@db_session
def propose_government(game_id: int, dir_id: int):
    lobby = Lobby.get(id=game_id)

    old_dir_id = get_game_director_id(game_id=game_id)
    old_dir = Player.get(id=old_dir_id)

    if old_dir is not None:
        old_dir.director = False

    player = Player.get(id=dir_id)
    if player:
        player.director = True
    if lobby:
        lobby.game.voting = True

    commit()


# Finish the current legislative session
@db_session
def finish_legislative_session(game_id: int, imperio: bool):
    game = Lobby.get(id=game_id).game
    if game:
        game.in_session = False
        game.minister_proclaimed = False
        game.director_proclaimed = False
        if not imperio:
            set_next_minister_candidate(game_id)
        game.expelliarmus = False
    commit()


# Updates the status of the game after the minister discards a card
@db_session
def finish_minister_proclamation(game_id: int):
    game = Lobby.get(id=game_id).game
    if game:
        game.minister_proclaimed = True
        commit()


# Director asks for Expelliarmus
@db_session
def director_ask_expelliarmus(game_id: int):
    game = Lobby.get(id=game_id).game
    if game: 
        game.minister_proclaimed = False
        game.expelliarmus = True
        commit()


# Proclaim and discard cards,
@db_session
def finish_director_proclamation(game_id: int):
    game = Lobby.get(id=game_id).game
    if game:
        game.director_proclaimed = True
        cards = list(select(c for c in ProcCard if c.game.lobby.id == game_id))
        neg_procs = get_number_neg_procs(game_id=game_id)
        players = get_lobby_max_players(lobby_id=game_id)
        if len(
            list(
                filter(
                lambda c: not (c.proclaimed or c.discarded),
                cards))) <= 2:
            shuffle_cards(game_id=game_id)
        if SPELLS_PLAYERS[players][neg_procs] == Spells.none or not game.last_proc_negative:
            discharge_director(game_id=game_id)
            finish_legislative_session(game_id=game_id, imperio=False)

        commit()


# Check if game in legislative session
@db_session
def in_legislative_session(game_id) -> bool:
    game = Lobby.get(id=game_id).game
    if game:
        return game.in_session
    else:
        return False


# Check if director proclaimed
@db_session
def get_director_proclaimed(game_id) -> bool:
    game = Lobby.get(id=game_id).game
    if game:
        return game.director_proclaimed
    else:
        return False


# Check if last proclamation is negative
@db_session
def get_last_proc_negative(game_id) -> bool:
    game = Lobby.get(id=game_id).game
    if game:
        return game.last_proc_negative
    else:
        return False

@db_session
def delete_player_from_game(game_id: int, player_id: int):
    lobby = Lobby.get(id=game_id)

    if lobby:
    # if owner set another person as lobby owner
        if get_lobby_is_id_owner(lobby_id=game_id, player_id=player_id):
            players = select(
                p for p in lobby.player if p.user.id != lobby.owner_id)
            if players.first() is not None:
                lobby.owner_id = players.first().user.id
            else:
                lobby.delete()

        player = Player.get(id=player_id)
        if player is not None:
            player.delete()
        commit()


@db_session
def get_game_ended(game_id: int):
    lobby = Lobby.get(id=game_id)

    if lobby and lobby.game:
        return Lobby.get(id=game_id).game.ended
    else:
        return False


@db_session
def get_game_phoenix_win(game_id: int):
    lobby = Lobby.get(id=game_id)
    if lobby and lobby.game :
        return Lobby.get(id=game_id).game.phoenix_win
    else:
        return False


