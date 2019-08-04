import pandas as pd
import os
import pickle as pk
from math import log2
import matplotlib.pyplot as plt


class GoldenStrategy:

    def __init__(self):
        self.current_race = 0
        self.total_race = 0
        self.value = 0
        self.bet_list = [0, 10]
        self.stop = False

    def handle(self, df, n=1):
        if self.stop:
            return self.value
        df['Win Odds'] = pd.to_numeric(df['Win Odds'])
        df = df.sort_values('Win Odds')
        df = df.reset_index()
        odd = float(df.loc[n, 'Win Odds'])
        self.current_race += 1
        bet = self.bet_list[-1] + self.bet_list[-2]
        self.bet_list.append(bet)
        if bet > self.value:
            self.stop = True
            return self.value
        try:
            if int(df.loc[n, 'Plc.']) == 1:
                self.value += odd * bet
                self.bet_list = [0, 10]
                if self.current_race * 3 > self.total_race:
                    self.stop = True
            self.value -= bet
        except ValueError:
            pass
        return self.value

    def reset(self, value=200, total=10, multiplier=1):
        self.value = value
        self.total_race = total
        self.current_race = 0
        self.bet_list = [0, 10 * multiplier]
        self.stop = False


pool = 800
invested = 800
strategy = GoldenStrategy()
d = 0
m = 2
pool_list = []
for f in os.listdir('./Data/Results/'):
    with open('./Data/Results/' + f, 'rb') as file:
        result_list = pk.load(file)
        pool += 200
        invested += 200
        no_race = len(result_list)
        strategy.reset(pool, no_race, 1)
        for r in result_list:
            pool = strategy.handle(r)
            print(pool)
        d += 1
        print(d, 'Day Balance:', pool)
        pool_list.append(pool)
print(invested)

plt.plot(pool_list)
plt.show()



