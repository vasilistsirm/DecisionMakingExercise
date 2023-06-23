import numpy as np

# Parameters
num_fish = 100
num_iterations = 100
# if it doesn't work for that many iterations/fish u can change the number to a lower one, but the results
# will not be as optimal
visual_range = 0.1
step_size = 0.1

# Generate user_money_rates and album_price (unchanged)
users_money = 200 + np.ceil(100 * np.random.rand(100))
user_money_rates = np.empty_like(np.append(users_money[0], np.random.randint(5, size=50) + 1))
for i in users_money:
    user_money_rates = np.vstack([user_money_rates, np.append(i, np.random.randint(5, size=50) + 1)])
user_money_rates = np.delete(user_money_rates, (0), axis=0)

album_price = np.random.randint(50, size=100) + 1


# Define fitness function (unchanged)
def calculate_individual_fitness(fish, i):
    fish = fish.reshape(user_money_rates.shape[0], 3)
    total_score = np.sum(fish[:, 1] * fish[:, 2])
    total_price = np.sum(fish[:, 1] * fish[:, 0])
    if total_price > users_money[i]:
        total_score -= total_score * (total_price - users_money[i]) / total_price
    return total_score


# Create initial fish population (unchanged)
def initialize_fish_population():
    initial_fish_population = []
    for _ in range(num_fish):
        fish = np.zeros(user_money_rates.shape[0] * 3)
        fish[:user_money_rates.shape[0]] = user_money_rates[:, 0]
        fish[user_money_rates.shape[0]:2 * user_money_rates.shape[0]] = np.random.choice(album_price,
                                                                                         size=user_money_rates.shape[0])
        fish[2 * user_money_rates.shape[0]:] = user_money_rates[:, 1]
        initial_fish_population.append(fish)
    return initial_fish_population


# Update fish position and behavior (unchanged)
def update_fish(fish):
    new_fish_population = []
    for i in range(num_fish):
        current_fish = fish[i]
        for _ in range(num_iterations):
            neighbors = get_neighbors(current_fish, fish)
            if len(neighbors) > 0:
                move_towards_neighbors(current_fish, neighbors)
            move_to_new_position(current_fish)
        new_fish_population.append(current_fish)
    return new_fish_population


# Get neighboring fish within the visual range (unchanged)
def get_neighbors(fish, population):
    neighbors = []
    for other_fish in population:
        if np.linalg.norm(fish - other_fish) <= visual_range:
            neighbors.append(other_fish)
    return neighbors


# Move the fish towards its neighbors (unchanged)
def move_towards_neighbors(fish, neighbors):
    for neighbor in neighbors:
        if calculate_individual_fitness(neighbor, 0) > calculate_individual_fitness(fish, 0):
            fish += step_size * (neighbor - fish)


# Move the fish to a new position (unchanged)
def move_to_new_position(fish):
    for i in range(user_money_rates.shape[0]):
        price_range = album_price[(album_price <= users_money[i]) & (album_price >= fish[(i * 3) + 1])]
        if len(price_range) > 0:
            fish[(i * 3) + 1] = np.random.choice(price_range)
        else:
            fish[(i * 3) + 1] = np.random.choice(album_price)
        fish[(i * 3) + 2] = np.random.choice(user_money_rates[:, 1])


# Main loop
fish_population = initialize_fish_population()
for _ in range(num_iterations):
    fish_population = update_fish(fish_population)

best_fish = max(fish_population, key=lambda x: calculate_individual_fitness(x, 0))

# Print the selected discs for each user
for i in range(user_money_rates.shape[0]):
    user = user_money_rates[i, 0]
    selected_discs = best_fish[(i * 3) + 1:(i * 3) + 4]
    print(f"User {user}: Selected Discs with prices: {selected_discs}")

# Random selection of discs
random_selection = []
for i in range(user_money_rates.shape[0]):
    user = user_money_rates[i, 0]
    random_disc = np.random.choice(album_price)
    random_selection.append(random_disc)
    print(f"User {user}: Randomly Selected Disc with price: {random_disc}")

# Compare scores
best_score = calculate_individual_fitness(best_fish, 0)
random_score = np.sum(np.array(random_selection) * user_money_rates[:, 2])
print(f"\nBest Fish Score: {best_score}")
print(f"Random Selection Score: {random_score}")
