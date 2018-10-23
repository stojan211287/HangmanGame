
class GuessNotAllowed(Exception):
    pass


class PlayerGuessWasWrong(Exception):
    pass


class PlayerAlreadyGuessedCharacter(Exception):
    pass


class PlayerWon(Exception):
    pass


class PlayerLost(Exception):
    pass


class GameAbortedAtStart(Exception):
    pass
