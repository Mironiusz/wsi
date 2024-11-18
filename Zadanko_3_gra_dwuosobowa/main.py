from play_nim import play_nim
from play_nim import play_nim_bot_vs_bot
from testing_nim import compare_bot_depths_and_plot
from checkers_gui import CheckersGUI

if __name__ == "__main__":
    # play_nim()
    checkers_gui = CheckersGUI()
    checkers_gui.run()

    # heaps = [3, 4, 5]
    # depths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # compare_bot_depths_and_plot(heaps, depths, games_per_pair=10)