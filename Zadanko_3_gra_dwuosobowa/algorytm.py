import random
from typing import Optional
from two_player_games_lib.state import State
from two_player_games_lib.move import Move
from two_player_games_lib.player import Player

def minimax(state: State, depth: int, alpha: float, beta: float, maximizing_player: bool, maximizing_player_obj: Player) -> float:
    """
    Algorytm minimax z obcinaniem alfa-beta.

    Parametry:
        state (State): Aktualny stan gry.
        depth (int): Pozostała głębokość przeszukiwania.
        alpha (float): Najlepsza już zbadana opcja na ścieżce do korzenia dla maksymalizującego.
        beta (float): Najlepsza już zbadana opcja na ścieżce do korzenia dla minimalizującego.
        maximizing_player (bool): Czy obecny gracz maksymalizuje wynik.
        maximizing_player_obj (Player): Obiekt gracza maksymalizującego.

    Zwraca:
        float: Heurystyczna wartość stanu.
    """
    evaluate = evaluate_nim

    if depth == 0 or state.is_finished():
        return evaluate(state, maximizing_player_obj)

    if maximizing_player:
        value = -float('inf')
        for move in state.get_moves():
            new_state = state.make_move(move)
            value = max(value, minimax(new_state, depth - 1, alpha, beta, False, maximizing_player_obj))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        for move in state.get_moves():
            new_state = state.make_move(move)
            value = min(value, minimax(new_state, depth - 1, alpha, beta, True, maximizing_player_obj))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value

def find_best_move(state: State, depth: int) -> Optional[Move]:
    """
    Znajduje najlepszy ruch dla obecnego gracza, korzystając z algorytmu minimax.

    Parametry:
        state (State): Aktualny stan gry.
        depth (int): Głębokość przeszukiwania.

    Zwraca:
        Move: Najlepszy znaleziony ruch.
    """
    maximizing_player_obj = state.get_current_player()
    best_value = -float('inf')
    best_moves = []

    for move in state.get_moves():
        new_state = state.make_move(move)
        move_value = minimax(new_state, depth - 1, -float('inf'), float('inf'), False, maximizing_player_obj)

        if move_value > best_value:
            best_value = move_value
            best_moves = [move]
        elif move_value == best_value:
            best_moves.append(move)

    chosen_move = random.choice(best_moves) if best_moves else None
    return chosen_move

def evaluate_nim(state: State, maximizing_player_obj: Player) -> float:
    """
    Funkcja oceniająca stan gry Nim.

    Parametry:
        state (State): Aktualny stan gry.
        maximizing_player_obj (Player): Obiekt gracza maksymalizującego.

    Zwraca:
        float: Wartość heurystyczna stanu.
    """
    if state.is_finished():
        winner = state.get_winner()
        if winner == maximizing_player_obj:
            return float('inf')
        else:
            return -float('inf')

    # Obliczenie nim-sumy
    heaps = getattr(state, 'heaps', [])
    nim_sum = 0
    for heap in heaps:
        nim_sum ^= heap # XOR

    # Jeśli nim-suma jest równa 0, stan jest słaby, w przeciwnym razie jest silny
    return 100 if nim_sum != 0 else -100

def evaluate_checkers(state: State, maximizing_player_obj: Player) -> float:
    """
    Ocenia stan gry w warcaby.

    Parametry:
        state (State): Stan gry do oceny.
        maximizing_player_obj (Player): Gracz, dla którego maksymalizujemy wynik.

    Zwraca:
        float: Wynik oceny stanu.
    """
    board = state.board
    score = 0
    for row in board:
        for piece in row:
            if piece.strip():
                piece_value = get_piece_value(piece)
                if piece.lower().startswith(maximizing_player_obj.char.lower()):
                    score += piece_value
                else:
                    score -= piece_value

    if state.is_finished():
        winner = state.get_winner()
        if winner == maximizing_player_obj:
            return float('inf')
        elif winner is None:
            return 0  # Draw
        else:
            return -float('inf')

    return score

def get_piece_value(piece: str) -> int:
    """
    Przypisuje wartość do pionka.

    Parametry:
        piece (str): Znak reprezentujący pionek ('w', 'b', 'W', 'B').

    Zwraca:
        int: Wartość pionka.
    """
    if piece.isupper():  # King
        return 3
    else:
        return 2

