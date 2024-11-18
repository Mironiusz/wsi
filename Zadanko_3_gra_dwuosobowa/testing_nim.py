import matplotlib.pyplot as plt
from play_nim import play_nim_bot_vs_bot

def compare_bot_depths_and_plot(heaps: list[int], depths: list[int], games_per_pair: int = 10):
    """
    Przeprowadza testy między botami z różnymi głębokościami przeszukiwania
    i zapisuje wyniki na wykresie.

    Parameters:
        heaps (list[int]): Lista rozmiarów stosów w grze Nim.
        depths (list[int]): Lista głębokości przeszukiwania do porównania.
        games_per_pair (int): Liczba gier do rozegrania dla każdej pary głębokości.

    Returns:
        None
    """
    results = {}

    for depth1 in depths:
        for depth2 in depths:
            wins1, wins2, draws = 0, 0, 0
            for _ in range(games_per_pair):
                winner = play_nim_bot_vs_bot(depth1, depth2, heaps)
                if winner == '1':
                    wins1 += 1
                elif winner == '2':
                    wins2 += 1
                else:
                    draws += 1
            results[(depth1, depth2)] = (wins1, wins2, draws)

    heatmap_data = [[results[(d1, d2)][0] for d2 in depths] for d1 in depths]

    plt.figure(figsize=(10, 8))
    plt.imshow(heatmap_data, cmap="coolwarm", origin="lower")
    plt.colorbar(label="Liczba wygranych bota 1")
    plt.xticks(range(len(depths)), depths)
    plt.yticks(range(len(depths)), depths)
    plt.xlabel("Głębokość bota 2")
    plt.ylabel("Głębokość bota 1")
    plt.title("Porównanie wygranych bota 1 dla różnych głębokości")
    plt.show()
