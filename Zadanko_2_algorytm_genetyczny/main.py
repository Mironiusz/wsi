from classes import Solver
import numpy as np

if __name__ == '__main__':
    start_population = np.random.randint(0, 2, (25, 200))
    # populacja startowa, ilość osobników, prawdopodobieństwo mutacji, prawdopodobieństwo krzyżowania, ilość iteracji
    solver = Solver(start_population, 25, 0.01, 0.6, 1000)
    solver.solve()
    print(solver.best_individual)
    print(solver.best_result)
    solver.plot_results()