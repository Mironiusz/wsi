import matplotlib.pyplot as plt
import numpy as np

class Solver():
    def __init__(self, start_population, individual_amount, mutation_probability, crossover_probability, max_iterations):
        self.start_population = start_population
        self.individual_amount = individual_amount
        self.mutation_probability = mutation_probability
        self.crossover_probability = crossover_probability
        self.max_iterations = max_iterations
        self.best_individual = None
        self.best_result = None
        self.history = []

    def solve(self):
        current_iteration = 0
        current_population = self.start_population
        results = [self.evaluate(individual) for individual in current_population]
        self.best_individual, self.best_result = self.find_best_individual(current_population, results)

        while current_iteration < self.max_iterations:
            #print(f'Iteration {current_iteration}, best result: {self.best_result}')
            #results.sort()


            new_population = self.proportionate_selection(current_population, results, self.individual_amount)
            new_population = self.crossover_and_mutate(new_population)
            results = [self.evaluate(individual) for individual in new_population]
            best_new_individual, best_new_result = self.find_best_individual(new_population, results)

            self.history.append(best_new_result)

            if best_new_result > self.best_result:
                self.best_individual = best_new_individual
                self.best_result = best_new_result

            current_population = new_population
            current_iteration += 1

    def plot_results(self):
        plt.figure(figsize=(10, 6))
        plt.scatter(range(len(self.history)), self.history, color="blue", alpha=0.6)
        plt.xlabel("Iteration")
        plt.ylabel("Best Result")
        plt.title("Best Result Distribution over Iterations")
        plt.grid(True)
        plt.savefig("results.png")
        plt.show()

    def proportionate_selection(self, population, results, amount):
        min_result = np.min(results)
        offset = -min_result + 1e-6
        fitness = [result + offset for result in results]
        fitness_sum = sum(fitness)

        if fitness_sum == 0:
            probabilities = [1 / len(fitness) for _ in fitness]
        else:
            probabilities = [f / fitness_sum for f in fitness]

        cumulative_probabilities = np.cumsum(probabilities)

        new_population = []
        for _ in range(amount):
            random_value = np.random.rand()
            chosen_individual_index = np.where(cumulative_probabilities > random_value)[0][0]
            new_population.append(population[chosen_individual_index])
        return new_population



    def crossover_and_mutate(self, population):
        # crossover
        new_population = []
        i = 0

        while i < len(population) - 1:
            if np.random.rand() < self.crossover_probability:
                crossover_point = np.random.randint(0, len(population[i]))
                new_population.append(np.concatenate([population[i][:crossover_point], population[i + 1][crossover_point:]]))
                new_population.append(np.concatenate([population[i + 1][:crossover_point], population[i][crossover_point:]]))
            else:
                new_population.append(population[i])
                new_population.append(population[i + 1])
            i += 2

        if len(population) % 2 == 1:
            new_population.append(population[-1])

        # mutation
        for i in range(len(new_population)):
            for j in range(len(new_population[i])):
                if np.random.rand() < self.mutation_probability:
                    if new_population[i][j] == 0:
                        new_population[i][j] = 1
                    else:
                        new_population[i][j] = 0

        return new_population


    def find_best_individual(self, population, results):
        best_index = np.argmax(results)
        return population[best_index], results[best_index]


    def generate_start_population(self):
        return np.random.randint(0, 2, (self.individual_amount, len(self.start_population[0])))


    def evaluate(self, individual):
        # all temperatures are represented as relative to the background

        temperature = np.zeros_like(individual[..., 0]) + 1500
        obj_temperature = np.zeros_like(individual[..., 0])

        temperatures = [temperature]
        for t, v in enumerate(np.transpose(individual)):
            delta_t = temperature
            delta_e = temperature - obj_temperature

            if 30 <= t <= 50:
                # door opened
                temperature = temperature - delta_t * 0.03

            else:
                # door closed
                temperature = temperature - delta_t * 0.01

            if t >= 40:
                # object in oven
                temperature = temperature - delta_e * 0.025
                obj_temperature = obj_temperature + delta_e * 0.0125

            temperature = temperature + 50 * v
            temperatures.append(temperature)

        temperatures = np.array(temperatures).T
        cost = np.sum(individual, axis=-1)
        diffs = np.sum(((temperatures[..., 40:] - 1500) / 500) ** 2, axis=-1)

        return -cost -diffs