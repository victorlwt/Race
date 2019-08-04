from statistics import mean
from matplotlib import pyplot as plt


def range_visualize(odds, results, size=100):
    no_interval = len(odds) // size
    odd_means = []
    win_prob = []
    for i in range(no_interval):
        odd_sample = odds[i * size:(i + 1) * size]
        results_sample = results[i * size:(i + 1) * size]
        odd_means.append(mean(odd_sample))
        total_wins = 0
        for win in results_sample:
            if win:
                total_wins += 1
        win_prob.append(total_wins / size)
    inverse_odds = [1 / o for o in odd_means]
    plt.scatter(inverse_odds, win_prob)
    plt.show()
    return win_prob, inverse_odds
