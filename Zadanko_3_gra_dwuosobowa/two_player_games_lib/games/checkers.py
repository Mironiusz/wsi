from typing import Iterable, Optional, List, Tuple
from two_player_games_lib.game import Game
from two_player_games_lib.move import Move
from two_player_games_lib.player import Player
from two_player_games_lib.state import State
import copy

class Checkers(Game):
    """Class that represents the Checkers game."""
    FIRST_PLAYER_DEFAULT_CHAR = 'W'  # White
    SECOND_PLAYER_DEFAULT_CHAR = 'B'  # Black

    def __init__(self, first_player: Player = None, second_player: Player = None):
        """
        Initializes the Checkers game.

        Parameters:
            first_player: the player that will go first (White)
            second_player: the player that will go second (Black)
        """
        self.first_player = first_player or Player(self.FIRST_PLAYER_DEFAULT_CHAR)
        self.second_player = second_player or Player(self.SECOND_PLAYER_DEFAULT_CHAR)

        state = CheckersState(self.first_player, self.second_player)

        super().__init__(state)

class CheckersMove(Move):
    """
    Class that represents a move in Checkers.

    Variables:
        sequence: List[Tuple[int, int]], a sequence of positions the piece moves through
    """
    def __init__(self, sequence: List[Tuple[int, int]]):
        self.sequence = sequence  # List of positions (row, col)

    def __eq__(self, other):
        if not isinstance(other, CheckersMove):
            return False
        return self.sequence == other.sequence

    def __str__(self):
        cols = 'abcdefgh'
        move_str = ' -> '.join(f"{cols[col]}{row + 1}" for row, col in self.sequence)
        return move_str

class CheckersState(State):
    """Class that represents a state in the Checkers game."""
    def __init__(self, current_player: Player, other_player: Player, board: List[List[str]] = None,
                 white_to_move: bool = True, must_jump: bool = False):
        self.board = board or self.initial_board()
        self.white_to_move = white_to_move
        self.must_jump = must_jump  # Flag indicating if the player must perform a jump
        super().__init__(current_player, other_player)

    def initial_board(self) -> List[List[str]]:
        """
        Sets up the initial Checkers board.

        Returns:
            A 2D list representing the board.
        """
        board = [[' ' for _ in range(8)] for _ in range(8)]
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 'b'  # Black pieces
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 'w'  # White pieces
        return board

    def get_moves(self) -> Iterable[CheckersMove]:
        """
        Generates all possible moves for the current player.
        """
        moves = []
        player_char = 'w' if self.white_to_move else 'b'

        # First, find all jumps (captures)
        jumps = self.find_all_jumps(player_char)
        if jumps:
            self.must_jump = True
            return jumps  # Must perform a jump if available
        else:
            self.must_jump = False

        # If no jumps, find regular moves
        for row in range(8):
            for col in range(8):
                if self.board[row][col].lower() == player_char:
                    moves.extend(self.get_piece_moves(row, col))

        return moves

    def find_all_jumps(self, player_char: str) -> List[CheckersMove]:
        """
        Finds all possible jumps for the current player.

        Parameters:
            player_char: 'w' or 'b' representing the player.

        Returns:
            A list of possible jump moves.
        """
        jumps = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col].lower() == player_char:
                    piece_jumps = self.get_piece_jumps(row, col, first_move=True)
                    jumps.extend(piece_jumps)
        return jumps

    def get_piece_moves(self, row: int, col: int) -> List[CheckersMove]:
        """
        Generates possible moves (non-capturing) for a piece at the given position.

        Parameters:
            row: Row index of the piece.
            col: Column index of the piece.

        Returns:
            A list of possible moves.
        """
        moves = []
        piece = self.board[row][col]
        directions = self.get_directions(piece, first_move=True, capturing=False)
        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc
            if self.is_valid_position(new_row, new_col) and self.board[new_row][new_col] == ' ':
                moves.append(CheckersMove([(row, col), (new_row, new_col)]))
        return moves

    def get_piece_jumps(self, row: int, col: int, path=None, visited=None, first_move=True) -> List[CheckersMove]:
        """
        Recursively finds all possible jumps for a piece at the given position.

        Parameters:
            row: Row index of the piece.
            col: Column index of the piece.
            path: Current path of the jump sequence.
            visited: Set of visited positions to prevent cycles.
            first_move: Whether this is the first move in the jump sequence.

        Returns:
            A list of possible jump moves.
        """
        if path is None:
            path = [(row, col)]
        if visited is None:
            visited = set()

        jumps = []
        piece = self.board[row][col]
        player_char = piece.lower()
        opponent_char = 'b' if player_char == 'w' else 'w'
        directions = self.get_directions(piece, first_move=first_move, capturing=True)

        can_jump_further = False

        for dr, dc in directions:
            middle_row = row + dr
            middle_col = col + dc
            new_row = row + 2 * dr
            new_col = col + 2 * dc
            if self.is_valid_position(new_row, new_col):
                if self.board[middle_row][middle_col].lower() == opponent_char and self.board[new_row][new_col] == ' ':
                    if ((middle_row, middle_col), (new_row, new_col)) not in visited:
                        visited.add(((middle_row, middle_col), (new_row, new_col)))
                        new_path = path + [(new_row, new_col)]
                        further_jumps = self.get_piece_jumps(new_row, new_col, new_path, visited, first_move=False)
                        if further_jumps:
                            jumps.extend(further_jumps)
                        else:
                            jumps.append(CheckersMove(new_path))
                        can_jump_further = True

        if not can_jump_further and len(path) > 1:
            return [CheckersMove(path)]
        else:
            return jumps

    def get_directions(self, piece: str, first_move: bool, capturing: bool) -> List[Tuple[int, int]]:
        """
        Returns the movement directions for a piece.

        Parameters:
            piece: The piece character ('w', 'b', 'W', 'B').
            first_move: Whether this is the first move in the jump sequence.
            capturing: Whether we're looking for capturing moves.

        Returns:
            A list of direction tuples.
        """
        if piece.isupper():  # King
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        elif piece == 'w':
            if capturing and not first_move:
                return [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Any direction after first capture
            else:
                return [(-1, -1), (-1, 1)]  # White moves up the board
        else:
            if capturing and not first_move:
                return [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Any direction after first capture
            else:
                return [(1, -1), (1, 1)]  # Black moves down the board

    def is_valid_position(self, row: int, col: int) -> bool:
        """
        Checks if the given position is valid on the board.

        Parameters:
            row: Row index.
            col: Column index.

        Returns:
            True if valid, False otherwise.
        """
        return 0 <= row < 8 and 0 <= col < 8

    def make_move(self, move: CheckersMove) -> 'CheckersState':
        new_board = copy.deepcopy(self.board)
        sequence = move.sequence
        piece = new_board[sequence[0][0]][sequence[0][1]]
        new_board[sequence[0][0]][sequence[0][1]] = ' '
        for idx in range(1, len(sequence)):
            row, col = sequence[idx]
            prev_row, prev_col = sequence[idx - 1]
            if abs(row - prev_row) == 2:
                # Remove the jumped piece
                middle_row = (row + prev_row) // 2
                middle_col = (col + prev_col) // 2
                new_board[middle_row][middle_col] = ' '
        new_board[sequence[-1][0]][sequence[-1][1]] = piece

        # Promote to king if reached the opposite end
        if piece == 'w' and sequence[-1][0] == 0:
            new_board[sequence[-1][0]][sequence[-1][1]] = 'W'
        elif piece == 'b' and sequence[-1][0] == 7:
            new_board[sequence[-1][0]][sequence[-1][1]] = 'B'

        # Check if another jump is possible (multi-capture)
        last_row, last_col = sequence[-1]
        new_state = CheckersState(self._other_player, self._current_player, new_board, not self.white_to_move)
        jumps = new_state.get_piece_jumps(last_row, last_col, first_move=False)
        if jumps and abs(sequence[-1][0] - sequence[-2][0]) == 2:
            # Must continue jumping with the same piece
            new_state.white_to_move = self.white_to_move  # Keep the same player's turn
            new_state._current_player = self._current_player
            new_state._other_player = self._other_player
            new_state.must_jump = True
        else:
            new_state.must_jump = False

        return new_state

    def is_finished(self) -> bool:
        # Game is finished if a player has no pieces or no possible moves
        player_char = 'w' if self.white_to_move else 'b'
        opponent_char = 'b' if self.white_to_move else 'w'

        player_pieces = any(piece.lower() == player_char for row in self.board for piece in row)
        opponent_pieces = any(piece.lower() == opponent_char for row in self.board for piece in row)

        if not player_pieces or not opponent_pieces:
            return True

        if not any(self.get_moves()):
            return True

        return False

    def get_winner(self) -> Optional[Player]:
        if not self.is_finished():
            return None
        player_char = 'w' if self.white_to_move else 'b'
        opponent_char = 'b' if self.white_to_move else 'w'

        player_pieces = any(piece.lower() == player_char for row in self.board for piece in row)
        opponent_pieces = any(piece.lower() == opponent_char for row in self.board for piece in row)

        if player_pieces and not opponent_pieces:
            return self._current_player
        elif opponent_pieces and not player_pieces:
            return self._other_player
        else:
            # No pieces or no moves for both players - draw
            return None

    def __str__(self) -> str:
        board_str = '  a b c d e f g h\n'
        for row in range(7, -1, -1):
            board_str += f"{row + 1} "
            for col in range(8):
                piece = self.board[row][col]
                if (row + col) % 2 == 0:
                    board_str += '. '
                else:
                    board_str += f"{piece} "
            board_str += f"{row + 1}\n"
        board_str += '  a b c d e f g h'
        return board_str
