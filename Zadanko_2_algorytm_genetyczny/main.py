from classes import Solver
import numpy as np

def test_solver(amount_of_tests, population_size, mutation_probability, crossover_probability, max_iterations):
    results = []
    for i in range(amount_of_tests):
        start_population = np.random.randint(0, 2, (population_size, 200))
        solver = Solver(start_population, population_size, mutation_probability, crossover_probability, max_iterations)
        solver.solve()
        results.append(solver.best_result)
    return results

def plot_group_results(results):
    import matplotlib.pyplot as plt
    print(max(results))
    plt.figure(figsize=(10, 6))
    plt.scatter(range(len(results)), results, color="blue", alpha=0.6)
    plt.xlabel("Test number")
    plt.ylabel("Best Result")
    plt.title("Best Result Distribution over Tests")
    plt.grid(True)
    plt.savefig("results.png")
    plt.show()

if __name__ == '__main__':
    start_population = np.random.randint(0, 2, (25, 200))
    #start_population = np.ones((25, 200), dtype=int)
    # populacja startowa, ilość osobników, prawdopodobieństwo mutacji, prawdopodobieństwo krzyżowania, ilość iteracji
    solver = Solver(start_population, 25, 0.001, 0.9, 300)
    solver.solve()
    print(solver.best_individual)
    print(solver.best_result)
    solver.plot_results()

    #liczba testów, ilość osobników, prawdopodobieństwo mutacji, prawdopodobieństwo krzyżowania, ilość iteracji
    # results = test_solver(25, 25, 0.0015, 0.1, 1000)
    # plot_group_results(results)