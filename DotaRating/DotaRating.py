from cProfile import label
import math
import random
import matplotlib.pyplot as plt

# Model constants
rating_change_default = 25

# Simulation props
rating_formal_initial = 6000
rating_actual_initial = 2000
games_played_total = 1000

# Analysis prefs
winrate_interval_param = 50


def learning_curve(rating_actual, rating_formal, game_result):
    # In general, you don't learn much when you play with weak players
    # But you learn quickly if you play with strong opponents

    # At maximum you can improve your skill by learning_maximum points. Change this value to whatever you want
    learning_maximum = 2

    # At minimum you can improve your skill by learning_minimum points. Change this value to whatever you want
    learning_minimum = 0

    rating_diff = rating_actual - rating_formal
    factored = -rating_diff * 0.001
    lerp_alpha = (1 + math.tanh(factored)) * 0.5
    lerp = (learning_maximum - learning_minimum) * lerp_alpha + learning_minimum
    return lerp

def victory_chance(rating_diff):
    factored = rating_diff * 0.0005
    return (1 + math.tanh(factored)) * 0.5

def generate_game_result(chance_to_win):
    # Simple probabilistic generator
    # Returns 1 if result is victory
    # Return -1 if result is defeat
    rand = random.random()
    if rand < chance_to_win:
        return 1
    else:
        return -1

def calculate_winrate(history, from_index, to_index):
    wins = 0
    defeats = 0

    if to_index > from_index:
        step = 1
    else:
        step = -1

    for i in range(from_index, to_index, step):
        if i < 0 or i >= len(history):
            break

        record = history[i]
        if record.rating_change < 0:
            defeats += 1
        else:
            wins += 1

    if wins + defeats == 0:
        return None

    rate = wins / (wins + defeats)
    return rate

class HistoryRecord:
    def __init__(self, game_number, rating_change, rating_actual, rating_formal, winrate_interval, winrate_total):
        self.game_number = game_number
        self.rating_change = rating_change
        self.rating_actual = rating_actual
        self.rating_formal = rating_formal
        self.winrate_interval = winrate_interval
        self.winrate_total = winrate_total


current_formal_rating = rating_formal_initial
current_actual_rating = rating_actual_initial
history = []
total_wins = 0
total_defeats = 0
for i in range(games_played_total):
    # Difference between player's skill and formal rating
    # Positive number means player plays better than the game thinks
    skill_difference = current_actual_rating - current_formal_rating 

    # Chance to win depends on skill difference. The more this value differs
    # from 0, the more chance differs from 0.5
    # See victory_chance(x) for actual relation
    chance_to_win = victory_chance(skill_difference)
    game_result = generate_game_result(chance_to_win)
    if game_result > 0:
        total_wins += 1
    else:
        total_defeats += 1

    rating_change = rating_change_default * game_result
    current_formal_rating += rating_change
    current_actual_rating += learning_curve(current_actual_rating, current_formal_rating, game_result)    

    if i > 1:
        winrate_interval = calculate_winrate(history, i - 1, i - winrate_interval_param)
        winrate_total = total_wins/(total_wins + total_defeats)
    else:
        winrate_interval = None
        winrate_total = None

    record = HistoryRecord(i, rating_change, current_actual_rating, current_formal_rating, winrate_interval, winrate_total)
    history.append(record)

print(f"Overall winrate: {total_wins/(total_wins + total_defeats)}")

# Plotting
x_values = []
actual_rating_values = []
formal_rating_values = []
winrate_interval_values = []
winrate_total_values = []
for record in history:
    x_values.append(record.game_number)
    actual_rating_values.append(record.rating_actual)
    formal_rating_values.append(record.rating_formal)
    winrate_interval_values.append(record.winrate_interval)
    winrate_total_values.append(record.winrate_total)

plt.figure()

plt.subplot(211)
plt.ylabel('Rating')
plt.plot(x_values, actual_rating_values, '-b', label="Actual rating")
plt.plot(x_values, formal_rating_values, '-r', label="Formal rating")
plt.legend(loc="upper left")

plt.subplot(212)
plt.ylabel(f"Winrate")
plt.axhline(y=0.5, color='g', linestyle='-')
plt.plot(x_values, winrate_interval_values, '-b', label=f"Last {winrate_interval_param}")
plt.plot(x_values, winrate_total_values, '-r', label=f"Overall")
plt.legend(loc="upper left")

plt.show()


