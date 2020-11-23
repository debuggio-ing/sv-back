import enum


class Spells(enum.Enum):
    none = 0
    divination = 1
    avada_kedavra = 2
    crucio = 3
    imperio = 4


SPELLS_PLAYERS = {5: {0: Spells.none,
                      1: Spells.none,
                      2: Spells.none,
                      3: Spells.divination,
                      4: Spells.avada_kedavra,
                      5: Spells.avada_kedavra},
                  6: {0: Spells.none,
                      1: Spells.none,
                      2: Spells.none,
                      3: Spells.divination,
                      4: Spells.avada_kedavra,
                      5: Spells.avada_kedavra},
                  7: {0: Spells.none,
                      1: Spells.none,
                      2: Spells.crucio,
                      3: Spells.imperio,
                      4: Spells.avada_kedavra,
                      5: Spells.avada_kedavra},
                  8: {0: Spells.none,
                      1: Spells.none,
                      2: Spells.crucio,
                      3: Spells.imperio,
                      4: Spells.avada_kedavra,
                      5: Spells.avada_kedavra},
                  9: {0: Spells.none,
                      1: Spells.crucio,
                      2: Spells.crucio,
                      3: Spells.imperio,
                      4: Spells.avada_kedavra,
                      5: Spells.avada_kedavra},
                  10: {0: Spells.none,
                       1: Spells.crucio,
                       2: Spells.crucio,
                       3: Spells.imperio,
                       4: Spells.avada_kedavra,
                       5: Spells.avada_kedavra}}

NUM_DEATH_EATERS = {5: 2, 6: 2, 7: 3, 8: 3, 9: 4, 10: 4}
NUM_PHOENIX_CARDS = 6
PROC_CARD_NUMBER = 17
VOLDEMORT_PERMISSIONS = {
    5: True,
    6: True,
    7: False,
    8: False,
    9: False,
    10: False}
