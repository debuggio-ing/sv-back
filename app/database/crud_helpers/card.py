from app.database.models import *
import random


# Return all selected cards in a game identified by game_id
@db_session
def get_selected_cards_pos(game_id: int):
    return list(
        select(
            card.position for card in ProcCard if card.selected and card.game.lobby.id == game_id))


@db_session
def get_selected_cards(game_id: int):
    return list(
        select(
            card for card in ProcCard if card.selected and card.game.lobby.id == game_id))

# Discard the card identified by card_pos and game_id


@db_session
def discard_card(card_pos: int, game_id: int):
    card = ProcCard.get(position=card_pos, game=game_id)
    card.selected = False
    card.discarded = True
    commit()


# Proclaim the card identified by card_pos and game_id.
# Discard the other selected card in the same game
@db_session
def proclaim_card(card_pos: int, game_id: int):
    cards = select(c for c in ProcCard if c.game.lobby.id == game_id)
    game = Lobby.get(id=game_id).game
    for card in cards:
        card.selected = False
        if card.position == card_pos:
            card.proclaimed = True
            game.last_proc_negative = (not card.phoenix)
        else:
            card.discarded = False
    commit()


# Shuffle the cards in the deck of the game specified by game_id
@db_session
def shuffle_cards(game_id: int):
    cards = select(c for c in ProcCard if c.game.lobby.id ==
                   game_id and not c.proclaimed)
    positions = list(range(0, len(cards)))
    random.shuffle(positions)
    for i in range(0, len(cards)):
        cards[i].position = positions[i]
        cards[i].selected = cards[i].discarded = False

def get_number_neg_procs(game_id: int):
    cards = select(c for c in ProcCard if c.game.lobby.id ==
                   game_id and (c.proclaimed and not c.phoenix))
    return len(cards)