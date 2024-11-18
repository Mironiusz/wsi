from checkers_gui import CheckersGUI

if __name__ == "__main__":
    checkers_gui = CheckersGUI()

    # Niestandardowa konfiguracja planszy
    custom_board = [
        ['b', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', 'w', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', 'w', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ]

    # Ustawienie niestandardowej planszy
    checkers_gui.set_custom_board(custom_board, white_to_move=False)

    # Uruchomienie gry
    checkers_gui.run()
