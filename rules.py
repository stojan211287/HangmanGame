from errors_rules import GuessedLetterNotInAlphabet, GuessTooLong, GuessWasEmpty


class GameRules:
    
    def __init__(self, game_alphabet, word_pool):
        
        self.game_alphabet = game_alphabet
        self.word_pool = word_pool
        
        # TRADITIONAL HANGMAN GAMES USUALLY ALLOW FOR 5 MISTAKES, BUT THIS CUSTOMIZABLE
        # ALTHOUGH, THE FRONTEND NEEDS TO CHANGE AS WELL
        self.no_of_mistakes_allowed = 5

    def too_many_mistakes(self, no_of_mistakes_made):
        return no_of_mistakes_made > self.no_of_mistakes_allowed
                    
    def is_guess_allowed(self, guessed_letter):
        
        if len(guessed_letter) > 1:
            raise GuessTooLong("Please only make single-letter guesses!")
        elif guessed_letter not in self.game_alphabet:
            raise GuessedLetterNotInAlphabet("Character is not in the game alphabet!")
        elif guessed_letter == "":
            raise GuessWasEmpty("You input was empty. Try again.")
        else:
            pass
