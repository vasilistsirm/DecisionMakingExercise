import numpy as np

# Parameters
population_size = 100
num_generations = 100
mutation_rate = 0.1

# Generate user_money_rates and album_price (unchanged)
users_money = 200 + np.ceil(100 * np.random.rand(100))
user_money_rates = np.empty_like(np.append(users_money[0], np.random.randint(5, size=50) + 1))
for i in users_money:
    user_money_rates = np.vstack([user_money_rates, np.append(i, np.random.randint(5, size=50) + 1)])
user_money_rates = np.delete(user_money_rates, (0), axis=0)

album_price = np.random.randint(50, size=100) + 1

# Define fitness function (modified variable name)
def calculate_individual_fitness(individual):
    individual = individual.reshape(user_money_rates.shape[0], 3)
    total_score = np.sum(individual[:, 1] * individual[:, 2])
    total_price = np.sum(individual[:, 1] * album_price)
    if total_price > individual[0, 0]:
        total_score = 0
    return total_score

# Create initial population (modified variable name)
initial_population = []
for _ in range(population_size):
    individual = np.zeros(user_money_rates.shape[0] * 3)
    individual[:user_money_rates.shape[0]] = user_money_rates[:, 0]
    individual[user_money_rates.shape[0]:2 * user_money_rates.shape[0]] = np.random.choice(album_price,
                                                                                          size=user_money_rates.shape[0])
    individual[2 * user_money_rates.shape[0]:] = user_money_rates[:, 1]
    initial_population.append(individual)

# Main loop (modified variable names)
for generation in range(num_generations):
    fitness_scores = [calculate_individual_fitness(individual) for individual in initial_population]
    sum_fitness_scores = np.sum(fitness_scores)
    if sum_fitness_scores == 0:
        probabilities = np.ones(population_size) / population_size  # Equal probabilities
    else:
        probabilities = fitness_scores / sum_fitness_scores
    selected_indices = np.random.choice(range(population_size), size=population_size, p=probabilities)
    selected_population = np.array([initial_population[index] for index in selected_indices])  # Convert to numpy array
    new_population = []
    for _ in range(population_size):
        parent_indices = np.random.choice(range(len(selected_population)), size=2, replace=False)
        parent1, parent2 = selected_population[parent_indices]
        parent1 = parent1.reshape(user_money_rates.shape[0], 3)
        parent2 = parent2.reshape(user_money_rates.shape[0], 3)
        crossover_point = np.random.randint(1, parent1.shape[0])
        child = np.concatenate((parent1[:crossover_point].flatten(), parent2[crossover_point:].flatten()))
        for i in range(child.shape[0]):
            if np.random.rand() < mutation_rate:
                child[i] = np.random.choice(album_price)
        new_population.append(child)
    initial_population = new_population

best_individual = max(initial_population, key=calculate_individual_fitness)

# Print the selected discs for each user (modified variable name)
for i in range(user_money_rates.shape[0]):
    user = user_money_rates[i, 0]
    selected_discs = best_individual[(i * 3) + 1]
    print(f"User {user}: Selected Disc with price: {selected_discs}")
