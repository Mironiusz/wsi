import pygame
import sys
from two_player_games_lib.player import Player
from two_player_games_lib.games.checkers import Checkers, CheckersMove
from algorytm import find_best_move

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (205, 92, 92)
BEIGE = (245, 245, 220)
GOLD = (255, 215, 0)
GREEN = (0, 255, 0)
BLUE = (30, 144, 255)

class CheckersGUI:
    def __init__(self):
        pygame.init()
        self.board_size = 8
        self.square_size = 80
        self.width = self.height = self.board_size * self.square_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Checkers')

        # Create players
        self.player1 = Player('W')  # White (Bot)
        self.player2 = Player('B')  # Black (Human)

        # Initialize game
        self.game = Checkers(self.player1, self.player2)
        self.state = self.game.state

        self.selected_piece = None
        self.move_sequence = []

        self.running = True

        # Load images or create simple representations
        self.create_piece_surfaces()

    def create_piece_surfaces(self):
        # Create surfaces for pieces
        self.white_piece = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
        pygame.draw.circle(self.white_piece, WHITE, (self.square_size // 2, self.square_size // 2), self.square_size // 2 - 10)

        self.black_piece = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
        pygame.draw.circle(self.black_piece, BLACK, (self.square_size // 2, self.square_size // 2), self.square_size // 2 - 10)

        self.white_king = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
        pygame.draw.circle(self.white_king, WHITE, (self.square_size // 2, self.square_size // 2), self.square_size // 2 - 10)
        pygame.draw.circle(self.white_king, GOLD, (self.square_size // 2, self.square_size // 2), self.square_size // 2 - 20)

        self.black_king = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
        pygame.draw.circle(self.black_king, BLACK, (self.square_size // 2, self.square_size // 2), self.square_size // 2 - 10)
        pygame.draw.circle(self.black_king, GOLD, (self.square_size // 2, self.square_size // 2), self.square_size // 2 - 20)

    def draw_board(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                rect = pygame.Rect(col * self.square_size, row * self.square_size, self.square_size, self.square_size)
                if (row + col) % 2 == 0:
                    pygame.draw.rect(self.screen, BEIGE, rect)
                else:
                    pygame.draw.rect(self.screen, RED, rect)

    def draw_pieces(self):
        board = self.state.board
        for row in range(self.board_size):
            for col in range(self.board_size):
                piece = board[row][col]
                if piece != ' ':
                    x = col * self.square_size
                    y = row * self.square_size
                    if piece == 'w':
                        self.screen.blit(self.white_piece, (x, y))
                    elif piece == 'b':
                        self.screen.blit(self.black_piece, (x, y))
                    elif piece == 'W':
                        self.screen.blit(self.white_king, (x, y))
                    elif piece == 'B':
                        self.screen.blit(self.black_king, (x, y))

    def get_square_under_mouse(self, pos):
        x, y = pos
        col = x // self.square_size
        row = y // self.square_size
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            return (row, col)
        else:
            return None

    def draw_valid_moves(self):
        if self.selected_piece:
            possible_destinations = []
            current_moves = self.state.get_moves()
            for move in current_moves:
                if move.sequence[:len(self.move_sequence)] == self.move_sequence:
                    next_pos = move.sequence[len(self.move_sequence)]
                    possible_destinations.append(next_pos)

            for pos in possible_destinations:
                row, col = pos
                x = col * self.square_size
                y = row * self.square_size
                pygame.draw.rect(self.screen, BLUE, (x, y, self.square_size, self.square_size), 3)

    def human_turn(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                square = self.get_square_under_mouse(pos)
                if square:
                    row, col = square
                    piece = self.state.board[row][col]
                    if self.selected_piece:
                        # Continue move sequence
                        self.move_sequence.append(square)
                        move = CheckersMove(self.move_sequence)
                        possible_moves = self.state.get_moves()
                        valid_move = None
                        for m in possible_moves:
                            if m.sequence[:len(self.move_sequence)] == self.move_sequence:
                                valid_move = m
                                break
                        if valid_move:
                            if len(self.move_sequence) == len(valid_move.sequence):
                                # Complete move
                                self.state = self.state.make_move(valid_move)
                                if self.state.must_jump:
                                    # Must continue jumping
                                    self.selected_piece = self.move_sequence[-1]
                                    self.move_sequence = [self.selected_piece]
                                else:
                                    self.selected_piece = None
                                    self.move_sequence = []
                                return
                            else:
                                # Partial move, wait for next input
                                pass
                        else:
                            # Invalid move, reset selection
                            self.selected_piece = None
                            self.move_sequence = []
                    else:
                        # Select a piece
                        if (self.state.white_to_move and piece.lower() == 'b') or (not self.state.white_to_move and piece.lower() == 'w'):
                            # Not the player's piece
                            continue
                        if piece != ' ':
                            self.selected_piece = square
                            self.move_sequence = [square]
        self.draw_valid_moves()

    def bot_turn(self):
        move = find_best_move(self.state, depth=6)
        if move:
            self.state = self.state.make_move(move)
        else:
            print("Bot has no valid moves.")
        self.selected_piece = None
        self.move_sequence = []

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.draw_board()
            self.draw_pieces()
            if self.selected_piece:
                # Highlight selected piece
                row, col = self.selected_piece
                x = col * self.square_size
                y = row * self.square_size
                pygame.draw.rect(self.screen, GREEN, (x, y, self.square_size, self.square_size), 3)
            pygame.display.flip()

            if self.state.is_finished():
                print("Game over!")
                winner = self.state.get_winner()
                if winner:
                    print(f"Winner: Player {winner.char}")
                else:
                    print("Draw!")
                self.running = False
                pygame.time.wait(3000)
                pygame.quit()
                sys.exit()

            if self.state.get_current_player().char == 'W':  # Bot
                self.bot_turn()
            else:
                self.human_turn()

            clock.tick(30)

if __name__ == "__main__":
    checkers_gui = CheckersGUI()
    checkers_gui.run()
