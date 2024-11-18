from two_player_games_lib.player import Player
from two_player_games_lib.games.nim import Nim, NimMove
from algorytm import find_best_move

def get_player_move(state: Nim, player_char: str) -> NimMove:
    """
    Funkcja do pobierania ruchu gracza.
    """
    while True:
        try:
            heap = int(input(f"Gracz {player_char}, wybierz stos (numer od 1 do {len(state.heaps)}): ")) - 1
            n = int(input("Podaj liczbę elementów do usunięcia: "))

            if heap < 0 or heap >= len(state.heaps) or n <= 0 or n > state.heaps[heap]:
                raise ValueError("Nieprawidłowy ruch. Spróbuj ponownie.")

            return NimMove(heap, n)
        except ValueError as e:
            print(e)

def play_nim():
    """
    Funkcja uruchamiająca grę Nim między dwoma graczami.
    """
    # Tworzenie graczy
    player1 = Player('1')
    player2 = Player('2')
    heaps = [3, 4, 5]

    game = Nim(heaps, player1, player2)

    state = game.state

    while not state.is_finished():
        print(state)
        if state.get_current_player().char == '1':
            move = find_best_move(state, depth=10)
            print(f"Bot wybiera ruch...")
        else:
            move = get_player_move(state, '2')
        state = state.make_move(move)

    print("\nKoniec gry!")
    winner = state.get_winner()
    print(f"Zwycięzca: Gracz {winner.char}")

def play_nim_bot_vs_bot(depth1: int, depth2: int, heaps: list[int]) -> str:
    """
    Gra między dwoma botami o różnych głębokościach przeszukiwania.

    Parameters:
        depth1 (int): Głębokość przeszukiwania dla bota 1.
        depth2 (int): Głębokość przeszukiwania dla bota 2.
        heaps (list[int]): Lista rozmiarów stosów w grze.

    Returns:
        str: Zwycięzca gry ('1', '2' lub 'Draw').
    """
    player1 = Player('1')
    player2 = Player('2')
    game = Nim(heaps, player1, player2)

    state = game.state

    while not state.is_finished():
        if state.get_current_player().char == '1':
            move = find_best_move(state, depth=depth1)
        else:
            move = find_best_move(state, depth=depth2)
        state = state.make_move(move)

    winner = state.get_winner()
    if winner:
        return winner.char
    else:
        return "Draw"


if __name__ == "__main__":
    play_nim()
