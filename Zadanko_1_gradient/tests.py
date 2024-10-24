import numpy as np
import pandas as pd
from functions import Solver

def generate_random_points(num_points, dimensions, low, high):
    return np.random.uniform(low, high, (num_points, dimensions))

def run_tests(f, grad_f, num_points, steps, dimensions, low, high):
    start_points = generate_random_points(num_points, dimensions, low, high)
    aggregated_results = []

    for beta in steps:
        iter_counts = []
        minima = []
        solver = Solver(beta=beta)

        for x0 in start_points:
            minimum, _, num_iterations = solver.solve(grad_f, x0)
            iter_counts.append(num_iterations)
            minima.append(f(minimum))

        mean_iterations = np.mean(iter_counts)
        std_iterations = np.std(iter_counts)
        mean_minimum = np.mean(minima)
        std_minimum = np.std(minima)

        aggregated_results.append({
            'step': beta,
            'mean_iterations': mean_iterations,
            'std_iterations': std_iterations,
            'mean_minimum': mean_minimum,
            'std_minimum': std_minimum
        })

    return aggregated_results

def save_results_to_table(aggregated_results, filename="aggregated_results.csv"):
    df = pd.DataFrame(aggregated_results)
    df.to_csv(filename, index=False)
    print(f"Aggregated results saved to {filename}")
