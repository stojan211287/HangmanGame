
class HangmanASCIIArt:
    
    def __init__(self, character_wildcard):
        
        self.character_wildcard = character_wildcard
        
        self.game_state_art = []
        
        self.gallows = []
        self.gallows.append(' +---+')
        self.gallows.append(' |   |')
        self.gallows.append('     |')
        self.gallows.append('     |')
        self.gallows.append('     |')
        self.gallows.append('     |')
        self.gallows.append('=======')
        
        self.hangman = {}
        self.hangman[0] = [' 0   |']
        self.hangman[1] = [' 0   |', ' |   |']
        self.hangman[2] = [' 0   |', '/|   |']
        self.hangman[3] = [' 0   |', '/|\\  |']
        self.hangman[4] = [' 0   |', '/|\\  |', '/    |']
        self.hangman[5] = [' 0   |', '/|\\  |', '/ \\  |']
        
        # THE "HEAD" OF THE HANGMAN IS TO BE DRAWN IN THE 3rd ROW, IE AT INDEX 2
        hangman_starting_row, hangman_body_index = 2, 0
        
        # FIRST GAME STATE IMAGE IS AN EMPTY GALLOWS
        self.game_state_art.append(self.gallows)
        
        for hangman_drawing in self.hangman.values():
            game_state_drawing, hangman_body_index = self.gallows.copy(), 0
            
            for hangman_drawing_row in hangman_drawing:
                game_state_drawing[hangman_starting_row + hangman_body_index] = hangman_drawing_row
                
                hangman_body_index += 1
                
            self.game_state_art.append(game_state_drawing)
            
    def draw_game_state(self, game_state_index):
        for element in self.game_state_art[game_state_index]:
            print(element)