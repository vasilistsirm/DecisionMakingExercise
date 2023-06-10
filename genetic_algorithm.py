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

# Define fitness function
def calculate_individual_fitness(individual, i):
    individual = individual.reshape(user_money_rates.shape[0], 3)
    total_score = np.sum(individual[:, 1] * individual[:, 2])
    total_price = np.sum(individual[:, 1] * individual[:, 0])
    if total_price > users_money[i]:
        total_score -= total_score * (total_price - users_money[i]) / total_price
    return total_score

# Create initial population
def initialize_population():
    initial_population = []
    for _ in range(population_size):
        individual = np.zeros(user_money_rates.shape[0] * 3)
        individual[:user_money_rates.shape[0]] = user_money_rates[:, 0]
        individual[user_money_rates.shape[0]:2 * user_money_rates.shape[0]] = np.random.choice(album_price,
                                                                                              size=user_money_rates.shape[0])
        individual[2 * user_money_rates.shape[0]:] = user_money_rates[:, 1]
        initial_population.append(individual)
    return initial_population

# Selection operator
def selection(fitness_scores):
    sum_fitness_scores = np.sum(fitness_scores)
    if sum_fitness_scores == 0:
        probabilities = np.ones(population_size) / population_size  # Equal probabilities
    else:
        probabilities = fitness_scores / sum_fitness_scores
    selected_indices = np.random.choice(range(population_size), size=population_size, p=probabilities)
    selected_population = np.array([initial_population[index] for index in selected_indices])
    return selected_population

# Crossover operator
def crossover(selected_population):
    new_population = []
    for _ in range(population_size):
        parent_indices = np.random.choice(range(len(selected_population)), size=2, replace=False)
        parent1, parent2 = selected_population[parent_indices]
        parent1 = parent1.reshape(user_money_rates.shape[0], 3)
        parent2 = parent2.reshape(user_money_rates.shape[0], 3)

        # Generate child
        child = np.zeros(user_money_rates.shape[0] * 3)
        for i in range(user_money_rates.shape[0]):
            price_range = album_price[album_price <= users_money[i]]
            if len(price_range) > 0:
                child[(i * 3) + 1] = np.random.choice(price_range)
            else:
                child[(i * 3) + 1] = album_price[0]
            child[(i * 3) + 2] = np.random.choice(user_money_rates[:, 1])

        new_population.append(child)
    return new_population


# Main loop
initial_population = initialize_population()
for generation in range(num_generations):
    fitness_scores = [calculate_individual_fitness(individual, i) for i, individual in enumerate(initial_population)]
    selected_population = selection(fitness_scores)
    initial_population = crossover(selected_population)

best_individual = max(initial_population, key=lambda x: calculate_individual_fitness(x, 0))

# Print the selected discs for each user
for i in range(user_money_rates.shape[0]):
    user = user_money_rates[i, 0]
    selected_discs = best_individual[(i * 3) + 1:(i * 3) + 4]
    print(f"User {user}: Selected Discs with prices: {selected_discs}")

# Random selection of discs
random_selection = []
for i in range(user_money_rates.shape[0]):
    user = user_money_rates[i, 0]
    random_disc = np.random.choice(album_price)
    random_selection.append(random_disc)
    print(f"User {user}: Randomly Selected Disc with price: {random_disc}")

# Compare scores
best_score = calculate_individual_fitness(best_individual, 0)
random_score = np.sum(np.array(random_selection) * user_money_rates[:, 2])
print(f"\nBest Individual Score: {best_score}")
print(f"Random Selection Score: {random_score}")
