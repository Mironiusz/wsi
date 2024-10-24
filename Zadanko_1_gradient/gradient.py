import numpy as np
from functions import f, g, grad_f, grad_g, Solver
from plotting import plot_g_function, plot_f_function, plot_g_function_3d
from tests import run_tests, save_results_to_table

if __name__ == "__main__":
    # losowe testy f(x)
    steps_f = [0.01, 0.05, 0.0833, 0.1, 0.1667, 0.2, 0.25, 0.26, 0.27, 0.28]
    test_results_f = run_tests(f, grad_f, num_points=50, steps=steps_f, dimensions=1, low=-2, high=1.8)
    save_results_to_table(test_results_f, filename="results_f.csv")

    # losowe testy g(x)
    steps_g = [0.01, 0.05, 0.0833, 0.1, 0.1667, 0.2, 0.25, 0.5, 0.75, 0.8, 0.85, 0.9, 0.95, 1, 1.5, 1.6, 1.62, 1.65, 1.7, 1.8, 2, 2.5, 3]
    test_results_g = run_tests(g, grad_g, num_points=5, steps=steps_g, dimensions=2, low=[-2, -3], high=[3, 1])
    save_results_to_table(test_results_g, filename="results_g.csv")

    # generowanie trajektorii funkcji g(x) przy różnych krokach
    x0_g = np.array([0, 1])
    paths_g = []
    for beta in steps_g:
        solver = Solver(beta=beta)
        _, path_g, iters = solver.solve(grad_g, x0_g)
        print(f"beta: {beta}, iters: {iters}")
        paths_g.append(path_g)
    plot_g_function(paths_g, steps_g, output_file="wykres_g_z_trajektoriami.png")

    # generowanie trajektorii funkcji f(x) przy różnych krokach
    x0_f = np.array([-2])
    paths_f = []
    for beta in steps_f:
        solver = Solver(beta=beta, epsilon=0.01)
        _, path_f, iters = solver.solve(grad_f, x0_f)
        paths_f.append(path_f)
    plot_f_function(paths_f, steps_f, output_file="wykres_f_z_trajektoriami.png")

    # render 3d funkcji g(x)
    plot_g_function_3d(output_file="wykres_3d_g.png")
