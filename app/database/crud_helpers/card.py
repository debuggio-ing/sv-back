from app.database.models import *
from app.api.schemas import *


# Return selected cards in a game
@db_session
def get_selected_cards(game_id):
    return list(ProcCard.select(lambda c: c.game.lobby.id == game_id and c.selected == True))


# Proclaim card, return false if it couldn't be proclaimed
@db_session
def proclaim_card(proclamation: [(int, bool)], game_id: int):
    # check cards are valid before modifying the database
    for sel_card in proclamation:
        card = list(ProcCard.select(lambda c: c.position == sel_card.card_pos and c.game.id == game_id))
        if len(card) is None or not card[0].selected:
            return False

    # update cards' status in database
    for sel_card in proclamation:
        card = list(ProcCard.select(lambda c: c.position == sel_card.card_pos and c.game.id == game_id))[0]
        card.selected = False
        if sel_card.to_proclaim:
            card.proclaimed = True
        else:
            card.discarded = True
    commit()
    return True
