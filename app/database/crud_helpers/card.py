from app.database.models import *
from app.api.schemas import *


# Return selected cards in a game
@db_session
def get_selected_cards(game_id):
    return list(ProcCard.select(lambda c: c.game.id == game_id and c.selected == True))


# Proclaim card, return false if it couldn't be proclaimed
@db_session
def proclaim_card(proclamation: [(int, bool)], game_id: int):
    # check cards are valid before modifying the database
    for (card_position, _) in proclamation:
        card = ProcCard.get(position == card_position)
        if card is None or not card.selected:
            return False

    # update cards' status in database
    for (card_pos, proclaim) in proclamation:
        card = ProcCard.get(position = card_pos)
        card.selected = False
        if proclaim:
            card.proclaimed = True
        else:
            card.discarded = True
    commit()
    return True
