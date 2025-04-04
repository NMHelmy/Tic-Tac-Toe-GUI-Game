import pygame as pg
import time
import sys
from pygame.locals import *


class TicTacToe():
    """
    Main Tic-Tac-Toe game class that handles all game logic, display, and user interaction.
    """
    
    def __init__(self):
        """
        Initialize the game with default values, load resources, and set up the display.
        """
        # Game state variables
        self.xo = 'x'  # Current player ('x' or 'o')
        self.winner = None  # Tracks the winner of the current game
        self.draw = False  # Flag for game being a draw
        self.game_started = False  # Flag for whether the game has started
        
        # Display settings
        self.width = 400  # Width of game board
        self.height = 400  # Height of game board
        self.fps = 30  # Frames per second for game loop
        
        # Game board (3x3 grid)
        self.board = [[None]*3, [None]*3, [None]*3]
        
        # Load and scale player images
        self.x_image = pg.image.load("x.png")
        self.o_image = pg.image.load("o.png")
        
        # Initialize pygame
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((self.width, self.height + 100), 0, 32)
        
        # Game statistics
        self.scores = {'x': 0, 'o': 0}  # Track scores for both players
        self.last_winner = None  # Track who won the last game
        
        # Font settings
        self.font_bold = pg.font.SysFont('Arial', 72, bold=True)
        
        # Tiebreaker mode
        self.tiebreaker_round = False  # Flag for tiebreaker mode
        
        # Player information
        self.player_names = {'x': "Player 1", 'o': "Player 2"}  # Default player names
        self.name_input_active = False  # Flag for name input screen
        self.current_input = ""  # Current text input for player names
        self.current_player_input = 'x'  # Track which player we're entering name for

    def draw_name_input_screen(self):
        """
        Draw the player name input screen with text boxes for both players.
        Returns the rectangles for the start button and player input boxes.
        """
        # Fill screen with dark purple background
        self.screen.fill((48, 25, 72))
        
        # Draw title
        title_font = pg.font.Font(None, 50)
        title = title_font.render("Enter Player Names", True, pg.Color('white'))
        self.screen.blit(title, (self.width/2 - title.get_width()/2, 50))
        
        # Player X input section
        x_font = pg.font.Font(None, 36)
        x_label = x_font.render("Player X:", True, pg.Color('white'))
        self.screen.blit(x_label, (self.width/4 - 100, 150))
        
        # Draw input box for Player X
        x_box = pg.Rect(self.width/4 + 20, 145, 200, 40)
        pg.draw.rect(self.screen, pg.Color('white'), x_box, 2)
        
        # Highlight if currently editing Player X name
        if self.current_player_input == 'x':
            pg.draw.rect(self.screen, pg.Color('yellow'), x_box, 2)
        
        # Show current name or placeholder
        x_name = x_font.render(self.player_names['x'] if self.player_names['x'] else "Player 1", 
                            True, pg.Color('white'))
        self.screen.blit(x_name, (x_box.x + 10, x_box.y + 10))
        
        # Player O input section
        o_label = x_font.render("Player O:", True, pg.Color('white'))
        self.screen.blit(o_label, (self.width/4 - 100, 220))
        
        # Draw input box for Player O
        o_box = pg.Rect(self.width/4 + 20, 215, 200, 40)
        pg.draw.rect(self.screen, pg.Color('white'), o_box, 2)
        
        # Highlight if currently editing Player O name
        if self.current_player_input == 'o':
            pg.draw.rect(self.screen, pg.Color('yellow'), o_box, 2)
        
        # Show current name or placeholder
        o_name = x_font.render(self.player_names['o'] if self.player_names['o'] else "Player 2", 
                            True, pg.Color('white'))
        self.screen.blit(o_name, (o_box.x + 10, o_box.y + 10))
        
        # Draw start button
        button_font = pg.font.Font(None, 40)
        start_button_text = button_font.render("START", True, pg.Color('white'))
        start_button_rect = pg.Rect(self.width/2 - 100, 300, 200, 50)
        pg.draw.rect(self.screen, pg.Color('black'), start_button_rect, border_radius=10)
        self.screen.blit(start_button_text, (start_button_rect.centerx - start_button_text.get_width()/2, 
                                        start_button_rect.centery - start_button_text.get_height()/2))
        
        # Draw instructions
        instr_font = pg.font.Font(None, 24)
        instruction = instr_font.render("Click on a name to edit, then press START", True, pg.Color('white'))
        self.screen.blit(instruction, (self.width/2 - instruction.get_width()/2, 360))
        
        pg.display.update()
        return start_button_rect, x_box, o_box

    def draw_start_screen(self):
        """
        Draw the initial start screen with game title and start button.
        Returns the rectangle for the start button.
        """
        # Fill screen with dark purple background
        self.screen.fill((48, 25, 72))
        
        # Draw multi-line title "TIC TAC TOE"
        title_lines = ["TIC", "TAC", "TOE"]
        title_y = self.height/4 - 30
        
        for line in title_lines:
            # Create text with shadow effect
            title_text = self.font_bold.render(line, True, pg.Color('white'))
            title_rect = title_text.get_rect(center=(self.width/2, title_y))
            shadow = self.font_bold.render(line, True, pg.Color('black'))
            self.screen.blit(shadow, (title_rect.x+2, title_rect.y+2))
            self.screen.blit(title_text, title_rect)
            title_y += title_text.get_height() + 5
        
        # Draw start button
        button_font = pg.font.Font(None, 50)
        start_button_text = button_font.render("START", 1, pg.Color('white'))
        start_button_rect = pg.Rect(self.width/4, self.height - 80, self.width/2, 60)
        pg.draw.rect(self.screen, pg.Color('black'), start_button_rect, border_radius=10)
        self.screen.blit(start_button_text, (start_button_rect.centerx - start_button_text.get_width()/2, 
                                          start_button_rect.centery - start_button_text.get_height()/2))
        
        pg.display.update()
        return start_button_rect

    def show_tie_breaker_prompt(self):
        """
        Display a prompt asking if players want to play a tiebreaker round.
        Returns True if players choose to play, False otherwise.
        """
        # Create semi-transparent overlay
        overlay = pg.Surface((self.width, self.height + 100), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Use slightly smaller font for tie message
        font = pg.font.Font(None, 36)
        
        # Show current scores
        score_text = font.render(f"Scores tied at {self.scores['x']}-{self.scores['o']}", 
                            True, pg.Color('white'))
        score_rect = score_text.get_rect(center=(self.width/2, self.height/2 - 50))
        self.screen.blit(score_text, score_rect)
        
        # Ask about tiebreaker
        question_text = font.render("Play one tiebreaker round?", True, pg.Color('white'))
        question_rect = question_text.get_rect(center=(self.width/2, self.height/2))
        self.screen.blit(question_text, question_rect)
        
        # Create yes/no buttons
        button_font = pg.font.Font(None, 30)
        yes_text = button_font.render("YES", True, pg.Color('white'))
        no_text = button_font.render("NO", True, pg.Color('white'))
        
        yes_rect = pg.Rect(self.width/2 - 90, self.height/2 + 50, 70, 35)
        no_rect = pg.Rect(self.width/2 + 20, self.height/2 + 50, 70, 35)
        
        # Draw buttons with different colors
        pg.draw.rect(self.screen, (34, 139, 34), yes_rect, border_radius=5)
        pg.draw.rect(self.screen, (178, 34, 34), no_rect, border_radius=5)
        
        # Position button text
        self.screen.blit(yes_text, (yes_rect.centerx - yes_text.get_width()/2, 
                                yes_rect.centery - yes_text.get_height()/2))
        self.screen.blit(no_text, (no_rect.centerx - no_text.get_width()/2, 
                                no_rect.centery - no_text.get_height()/2))
        
        pg.display.update()
        
        # Wait for player input
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()
                    if yes_rect.collidepoint(mouse_pos):
                        return True  # Play tiebreaker
                    elif no_rect.collidepoint(mouse_pos):
                        return False  # Don't play tiebreaker
            self.clock.tick(self.fps)

    def check_tie_and_prompt(self):
        """
        Check if scores are tied and prompt for tiebreaker if needed.
        Returns True if tiebreaker should be played, False otherwise.
        """
        if self.scores['x'] == self.scores['o'] and self.scores['x'] > 0:
            return self.show_tie_breaker_prompt()
        return False

    def handle_exit(self):
        """
        Handle game exit, showing appropriate messages for tiebreakers or normal game end.
        """
        # Special handling for tiebreaker rounds
        if self.tiebreaker_round:
            if self.last_winner:
                winner_name = self.player_names[self.last_winner]
                self.show_final_message(f"{winner_name} wins the tiebreaker!")
            else:
                self.show_final_message("Tiebreaker was a draw!")
            pg.quit()
            sys.exit()
        
        # Check for tied scores and prompt for tiebreaker
        if self.scores['x'] == self.scores['o'] and (self.scores['x'] > 0 or self.winner is not None):
            if self.show_tie_breaker_prompt():
                self.tiebreaker_round = True
                self.scores = {'x': 0, 'o': 0}  # Reset scores for tiebreaker
                self.reset_game()
                return
            
            # If no tiebreaker, show tie message
            self.show_final_message("Game ended in a tie!")
        else:
            # Show winner message if there is one
            if self.last_winner:
                winner_name = self.player_names[self.last_winner]
                self.show_final_message(f"{winner_name} wins the game!")
            else:
                self.show_final_message("Thanks for playing!")
        
        # Quit the game
        pg.quit()
        sys.exit()

    def show_final_message(self, message):
        """
        Display a final message overlay before exiting the game.
        """
        # If message contains a winner, use player name
        if "wins" in message.lower() and self.last_winner:
            player_name = self.player_names[self.last_winner]
            message = f"{player_name} wins!"
        
        # Create semi-transparent overlay
        overlay = pg.Surface((self.width, self.height+100), pg.SRCALPHA)
        overlay.fill((0,0,0,180))
        self.screen.blit(overlay, (0,0))
        
        # Display the message
        font = pg.font.Font(None, 40)
        text = font.render(message, True, pg.Color('white'))
        text_rect = text.get_rect(center=(self.width/2, self.height/2))
        self.screen.blit(text, text_rect)
        pg.display.update()
        time.sleep(2)  # Show message for 2 seconds

    def show_exit_message(self):
        """
        Display an exit message overlay before quitting.
        """
        # Create semi-transparent overlay
        overlay = pg.Surface((self.width, self.height + 100), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Determine appropriate exit message
        font = pg.font.Font(None, 40)
        if self.scores['x'] == self.scores['o']:
            message = "Game ended in a tie!"
        elif self.last_winner:
            message = f"{self.last_winner.upper()} won the game!"
        elif self.draw:
            message = "Game was a draw!"
        else:
            message = "Thanks for playing!"
        
        # Display the message
        text = font.render(message, True, pg.Color('white'))
        text_rect = text.get_rect(center=(self.width/2, self.height/2))
        self.screen.blit(text, text_rect)
        
        pg.display.update()
        time.sleep(2)  # Show message for 2 seconds

    def start_screen(self):
        """
        Display and handle the initial start screen.
        """
        start_button_rect = self.draw_start_screen()
        waiting = True
        
        while waiting:
            for event in pg.event.get():
                if event.type == QUIT:
                    self.show_exit_message()
                    pg.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()
                    if start_button_rect.collidepoint(mouse_pos):
                        waiting = False
                        # Show name input screen
                        if not self.handle_name_input():
                            return  # User exited from name input
                        self.game_started = True
                        self.init_game_board()
            self.clock.tick(self.fps)

    def init_game_board(self):
        """
        Initialize the game board with scaled images and grid lines.
        """
        # Scale player images
        self.x_image = pg.transform.scale(self.x_image, (80, 80))
        self.o_image = pg.transform.scale(self.o_image, (80, 80))
        
        # Fill screen with white for board and dark purple for status area
        self.screen.fill(pg.Color('white'))
        self.screen.fill((48, 25, 52), (0, 400, 400, 100))

        # Draw grid lines
        pg.draw.line(self.screen, (48, 25, 52), (self.width/3, 0), (self.width/3, self.height), 7)
        pg.draw.line(self.screen, (48, 25, 52), (self.width/3 * 2, 0), (self.width/3 * 2, self.height), 7)
        pg.draw.line(self.screen, (48, 25, 52), (0, self.height/3), (self.width, self.height/3), 7)
        pg.draw.line(self.screen, (48, 25, 52), (0, self.height/3 * 2), (self.width, self.height/3 * 2), 7)
        
        pg.display.update()
        self.status()  # Update status display

    def handle_name_input(self):
        """
        Handle player name input screen and user interactions.
        Returns True when names are submitted, False if exited.
        """
        start_button_rect, x_box, o_box = self.draw_name_input_screen()
        input_active = False
        
        while True:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()
                    if start_button_rect.collidepoint(mouse_pos):
                        return True  # Start game
                    elif x_box.collidepoint(mouse_pos):
                        self.current_player_input = 'x'
                        # Clear if default text
                        if self.player_names['x'] == "Player 1":
                            self.current_input = ""
                            self.player_names['x'] = ""
                        else:
                            self.current_input = self.player_names['x']
                        input_active = True
                    elif o_box.collidepoint(mouse_pos):
                        self.current_player_input = 'o'
                        # Clear if default text
                        if self.player_names['o'] == "Player 2":
                            self.current_input = ""
                            self.player_names['o'] = ""
                        else:
                            self.current_input = self.player_names['o']
                        input_active = True
                    else:
                        input_active = False
                elif event.type == KEYDOWN and input_active:
                    if event.key == K_RETURN:
                        # If empty after editing, restore default
                        if not self.current_input.strip():
                            if self.current_player_input == 'x':
                                self.player_names['x'] = "Player 1"
                            else:
                                self.player_names['o'] = "Player 2"
                        input_active = False
                    elif event.key == K_BACKSPACE:
                        self.current_input = self.current_input[:-1]
                        self.player_names[self.current_player_input] = self.current_input
                    else:
                        self.current_input += event.unicode
                        self.player_names[self.current_player_input] = self.current_input
            
            # Redraw the input screen with updated names
            start_button_rect, x_box, o_box = self.draw_name_input_screen()
            self.clock.tick(self.fps)

    def status(self):
        """
        Update and display the game status bar (current player, scores, exit button).
        Returns the exit button rectangle for click detection.
        """
        # Clear status area
        pg.draw.rect(self.screen, (48, 25, 52), (0, 400, self.width, 100))
        
        # Use different font sizes for normal and tiebreaker modes
        if self.tiebreaker_round:
            main_font_size = 30  # Smaller font for tiebreaker
            status_y_pos = 450   # Position further down
        else:
            main_font_size = 40  # Normal size
            status_y_pos = 440   # Normal position
        
        # Build status message based on game state
        if self.winner is None:
            player_name = self.player_names[self.xo]
            status_message = f"{player_name}'s Turn"
        else:
            player_name = self.player_names[self.winner]
            status_message = f"{player_name} WON!!"
            self.last_winner = self.winner
        if self.draw:
            status_message = "Game Draw!"
            self.last_winner = None

        # Render main status text
        font = pg.font.Font(None, main_font_size)
        text = font.render(status_message, 2, pg.Color('white'))
        text_rect = text.get_rect(center=(self.width/2, status_y_pos))
        self.screen.blit(text, text_rect)
        
        # Display scores (smaller font)
        score_font = pg.font.Font(None, 25)
        score_text = score_font.render(f"X: {self.scores['x']}  O: {self.scores['o']}", 1, pg.Color('white'))
        self.screen.blit(score_text, (20, 415))  # Position in top-left
        
        # Draw exit button
        exit_font = pg.font.Font(None, 25)
        exit_text = exit_font.render("EXIT", 1, pg.Color('white'))
        exit_rect = pg.Rect(self.width - 70, 415, 50, 25)
        pg.draw.rect(self.screen, (0, 0, 0), exit_rect, border_radius=5)
        self.screen.blit(exit_text, (exit_rect.centerx - exit_text.get_width()/2, 
                                    exit_rect.centery - exit_text.get_height()/2))
        
        pg.display.update()
        return exit_rect  # Return for click detection

    def check_win(self):
        """
        Check if the current board state has a winner or is a draw.
        Updates game state and draws winning lines if needed.
        Returns the exit button rectangle.
        """
        # Check rows for winner
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0] is not None:
                self.winner = self.board[i][0]
                # Draw horizontal winning line
                pg.draw.line(self.screen, pg.Color('black'), 
                            (0, (i+1)*self.height/3 - self.height / 6), 
                            (self.width, (i+1)*self.height/3 - self.height / 6), 5)
                break
            # Check columns for winner
            elif self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] is not None:
                self.winner = self.board[0][i]
                # Draw vertical winning line
                pg.draw.line(self.screen, pg.Color('black'), 
                            ((i+1)*self.height/3 - self.height / 6, 0), 
                            ((i+1)*self.height/3 - self.height / 6, self.width), 5)
                break

        # Check diagonal (top-left to bottom-right)
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            self.winner = self.board[0][0]
            pg.draw.line(self.screen, pg.Color('black'), (0, 0), (self.width, self.height), 5)

        # Check diagonal (top-right to bottom-left)
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            self.winner = self.board[0][2]
            pg.draw.line(self.screen, pg.Color('black'), (self.width, 0), (0, self.height), 5)

        # Check for draw (all spaces filled)
        if self.winner is None and all([all(row) for row in self.board]):
            self.draw = True
        elif self.winner:
            self.scores[self.winner] += 1  # Update scores

        # Update status display
        exit_rect = self.status()
        return exit_rect

    def draw_xo(self, row, col):
        """
        Draw an X or O in the specified row and column.
        Alternates players after each move.
        """
        # Calculate position based on row and column
        if row == 1:
            posx = 30
        if row == 2:
            posx = self.width/3 + 30
        if row == 3:
            posx = self.width/3*2 + 30

        if col == 1:
            posy = 30
        if col == 2:
            posy = self.height/3 + 30
        if col == 3:
            posy = self.height/3*2 + 30

        # Update board state
        self.board[row-1][col-1] = self.xo

        # Draw appropriate symbol and switch player
        if (self.xo == 'x'):
            self.screen.blit(self.x_image, (posy, posx))
            self.xo = 'o' 
        else:
            self.screen.blit(self.o_image, (posy, posx))
            self.xo = 'x' 

        pg.display.update()

    def user_click(self):
        """
        Handle user mouse clicks on the game board or exit button.
        """
        x,y = pg.mouse.get_pos()
    
        # Check if exit button was clicked
        if self.width-80 <= x <= self.width-20 and 410 <= y <= 440:
            self.handle_exit()
            return

        # Determine which column was clicked
        if (x < self.width/3):
            col = 1
        elif (x < self.width/3 * 2):
            col = 2
        elif (x < self.width):
            col = 3
        else:
            col = None

        # Determine which row was clicked
        if (y < self.height/3):
            row = 1
        elif (y < self.height/3 * 2):
            row = 2
        elif (y < self.height):
            row = 3
        else:
            row = None

        # If valid empty cell was clicked, make the move
        if (row and col and self.board[row-1][col-1] is None):
            self.draw_xo(row, col)
            self.check_win()  # Check for win/draw after move

    def reset_game(self):
        """
        Reset the game state for a new round while maintaining scores.
        """
        time.sleep(1.5)  # Pause to show final state
        
        # Special handling for tiebreaker rounds
        if self.tiebreaker_round and (self.winner or self.draw):
            if self.winner:
                self.show_final_message(f"{self.winner.upper()} wins the tiebreaker!")
            else:
                self.show_final_message("Tiebreaker was a draw!")
            pg.quit()
            sys.exit()
        
        # Reset game state
        self.xo = 'x'
        self.draw = False
        self.winner = None
        self.board = [[None]*3, [None]*3, [None]*3]
        self.init_game_board()  # Redraw empty board


# Main game initialization and loop
t = TicTacToe()
t.start_screen()  # Show start screen first

while True:
    for event in pg.event.get():
        if event.type == QUIT:
            t.handle_exit()  # Handle window close
        elif event.type == MOUSEBUTTONDOWN:
            if t.game_started:
                t.user_click()  # Handle game moves
                if (t.winner or t.draw):
                    t.reset_game()  # Start new round if game ended
            else:
                t.start_screen()  # Return to start screen if not started
    pg.display.update()
    t.clock.tick(30)  # Maintain 30 FPS