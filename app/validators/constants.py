import enum
<<<<<<< HEAD


=======
from functools import lru_cache
from pydantic import BaseSettings


# Read environment variables
class Settings(BaseSettings):
    demo: bool = False


# Create settings according to the environment variables
settings = Settings()


# Spells supported by the game
>>>>>>> origin/develop
class Spells(enum.Enum):
    none = 0
    divination = 1
    avada_kedavra = 2
    crucio = 3
    imperio = 4


<<<<<<< HEAD
=======
# Order of spell according to the number of player and death eaters proclaimed
# The format is: {number_of_players: {death_eater_proclamations: spell}}
>>>>>>> origin/develop
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

<<<<<<< HEAD
NUM_DEATH_EATERS = {5: 2, 6: 2, 7: 3, 8: 3, 9: 4, 10: 4}
NUM_PHOENIX_CARDS = 6
PROC_CARD_NUMBER = 17
=======
# Number of death eaters for the match according to the number of players
# Format {number_of_player: number_of_death_eaters}
NUM_DEATH_EATERS = {5: 2, 6: 2, 7: 3, 8: 3, 9: 4, 10: 4}
# Number of cards and their types
NUM_PHOENIX_CARDS = 6
PROC_CARD_NUMBER = 17


# Can Voldemort see roles according to the number of players in the game?
# Format: {number_of_players: permission}
VOLDEMORT_PERMISSIONS = {
    5: True,
    6: True,
    7: False,
    8: False,
    9: False,
    10: False}
>>>>>>> origin/develop
