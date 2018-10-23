import os
import sys
import random

from collections import defaultdict

from errors_rules import GameRulesException
from errors_backend import GameAbortedAtStart, GuessNotAllowed, PlayerAlreadyGuessedCharacter, PlayerGuessWasWrong, \
                            PlayerLost, PlayerWon


class HangmanGame:

    def __init__(self, game_rules, high_score_table, frontend):
        
        self.game_rules = game_rules
        self.high_score_table = high_score_table
        self.frontend = frontend
        
        self.game_word, self.game_word_lookup = self._set_game_word_from_pool()
        
        self.word_was_guessed = False

        self.no_of_mistakes_made = 0
        self.letters_already_guessed = {letter: False
                                        for letter in self.game_word_lookup.keys()}
                                        
        self.display_string = [self.frontend.character_wildcard]*len(self.game_word)
        
    def _set_game_word_from_pool(self):
        
        chosen_word_index = random.randint(0, len(self.game_rules.word_pool)-1)
        
        game_word_string = self.game_rules.word_pool[chosen_word_index]
        
        game_word_lookup = defaultdict(list)
        
        for letter in game_word_string:
            game_word_lookup[letter] = self._get_letter_positions_in_word(letter, game_word_string)
        
        return game_word_string, game_word_lookup
        
    @staticmethod
    def _get_letter_positions_in_word(letter, word):
        
        letter_positions = []
        
        for i, letter_of_word in enumerate(word):
            if letter == letter_of_word:
                letter_positions.append(i)
            
        return letter_positions
        
    def play(self):
        
        try:
            self._welcome_player()
        
        except GameAbortedAtStart as abort:
            print(abort)
            sys.exit()
            
        # DEFINE FIRST GAME MESSAGE
        game_message = None

        while not self.word_was_guessed:
            
            self._draw_game_state(game_message=game_message)
            
            try:
                players_guess = self._guess_a_letter()
                self._check_guess(players_guess)
                game_message = "%s was correct!" % (players_guess, )
                
            except PlayerAlreadyGuessedCharacter as already_guessed:
                game_message = already_guessed
                continue

            except GuessNotAllowed as not_allowed:
                game_message = not_allowed
                continue
            
            except PlayerGuessWasWrong as wrong_guess:
                game_message = wrong_guess
                self.no_of_mistakes_made += 1

                try:
                    self._check_how_many_mistakes()
                    
                except PlayerLost as game_loss:
                    self._draw_game_state(game_message=game_loss)
                    sys.exit()
                
            except PlayerWon as victory :
                self._draw_game_state(game_message=victory)
                self.word_was_guessed = True
                self._write_and_display_high_score()
                sys.exit()
            
    def _welcome_player(self):
        
        print("""Hey! Welcome to Hangman!
        Rules are as follows:
            1) You win if you guess all the characters in a secret word
            2) The characters in the secret word all come from the set %s
            3) You can make up to %d wrong guesses
            
            Enjoy!
            """ % (self.game_rules.game_alphabet,
                   self.game_rules.no_of_mistakes_allowed))
        try:
            player_name_prompt = "Please enter your name:"+os.linesep
            self.player_name = input(player_name_prompt).strip()
            
        except KeyboardInterrupt:
            game_abort_msg = os.linesep+"Keyboard interrupt received. Aborting game."
            raise GameAbortedAtStart(game_abort_msg)
            
    def _draw_game_state(self, game_message=None):
        
        os.system("clear")
        if game_message is not None:
            print("GAME SAYS: "+str(game_message))
        print(os.linesep)
        self.frontend.draw_game_state(game_state_index=self.no_of_mistakes_made)
        print(os.linesep)
        print("%s, you've made %d mistakes! You are allowed at most %d." % (self.player_name,
                                                                            self.no_of_mistakes_made,
                                                                            self.game_rules.no_of_mistakes_allowed))
        print(os.linesep)
        self._display_word()
        print(os.linesep)
    
    def _guess_a_letter(self):
        
        try:
            guess = input("Make a guess: ").strip()
            self.game_rules.is_guess_allowed(guess)
            return guess

        except KeyboardInterrupt:
            print(os.linesep+"Received keyboard interrupt. Game will close. Bye!")
            sys.exit()
            
        except GameRulesException as rule_broken:
            raise GuessNotAllowed(rule_broken)

    def _check_guess(self, players_guess):
        
        try:
            if not self.letters_already_guessed[players_guess]:
                self.letters_already_guessed[players_guess] = True
                self._reveal_correctly_guessed_letters()
            else:
                raise PlayerAlreadyGuessedCharacter("You already guessed %s!" % (players_guess,))
                
        except KeyError:
            raise PlayerGuessWasWrong("%s was a wrong guess!" % (players_guess, ))
            
    def _reveal_correctly_guessed_letters(self):
    
        for letter in self.game_word_lookup.keys():
            if self.letters_already_guessed[letter]:
                for letter_position in self.game_word_lookup[letter]:
                    self.display_string[letter_position] = letter
                    
        if self.frontend.character_wildcard not in self.display_string:
            congrats_msg = "Congrats, %s! You have correctly guessed the word %s!" % (self.player_name, self.game_word)
                
            raise PlayerWon(congrats_msg)
    
    def _check_how_many_mistakes(self):
        
        if self.game_rules.too_many_mistakes(self.no_of_mistakes_made):
            raise PlayerLost("You have made too many mistakes, %s! You lose." %
                             (self.player_name, ))
        else:
            pass
                             
    def _write_and_display_high_score(self):
        
        score_won = self.high_score_table.score_and_store(self.player_name,
                                                          self.game_word,
                                                          self.no_of_mistakes_made)
                                              
        print("You have won %d points!" % (score_won, ))
        print(os.linesep)

        self.high_score_table.print_high_scores()

    def _display_word(self):
        print(" ".join(self.display_string))
