class GameRulesException(Exception):
    pass


class GuessTooLong(GameRulesException):
    pass


class GuessWasEmpty(GameRulesException):
    pass


class GuessedLetterNotInAlphabet(GameRulesException):
    pass
