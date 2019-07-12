import os
import base64

from rules import GameRules
from scoring import HighScoreTable

from backend import HangmanGame
from frontend import HangmanASCIIArt

# FOR DEFINING THE GAME ALPHABET
from string import ascii_letters, digits

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
WORD_POOL_FILE = os.path.join(ROOT_DIR, "words", "solutions")

with open(WORD_POOL_FILE, "r") as solution_file:
    scrambled_solutions = solution_file.read().split(",")

WORD_POOL = [
    base64.b64decode(scrambled_solution.encode("utf-8")).decode("utf-8")
    for scrambled_solution in scrambled_solutions
]

GAME_ALPHABET = ascii_letters + digits
NO_OF_HIGH_SCORES = 10
CHARACTER_WILDCARD = "*"


def game_scoring_function(game_word, no_of_mistakes_made):
    return 100 * (len(game_word) - no_of_mistakes_made)


def main():

    game_rules = GameRules(game_alphabet=GAME_ALPHABET, word_pool=WORD_POOL)

    high_score_table = HighScoreTable(
        no_of_high_scores=NO_OF_HIGH_SCORES, game_scoring_function=game_scoring_function
    )

    frontend_drawer = HangmanASCIIArt(character_wildcard=CHARACTER_WILDCARD)

    my_game_instance = HangmanGame(
        game_rules=game_rules,
        high_score_table=high_score_table,
        frontend=frontend_drawer,
    )

    my_game_instance.play()


if __name__ == "__main__":
    main()
