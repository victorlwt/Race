import pickle as pk
import os
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import numpy as np

from utility import range_visualize


# return the average win probability and and average odd of the nth-heat
def average_win_odd(n, folder='./Data/Results/', gate=1.0):
    no_race = 0
    hot_win = 0
    hot_sum = 0
    for f in os.listdir(folder):
        with open(folder + f, 'rb') as file:
            result_list = pk.load(file)
            for df in result_list:
                df['Win Odds'] = pd.to_numeric(df['Win Odds'])
                df = df.sort_values('Win Odds')
                df = df.reset_index(drop=True)
                odd = float(df.loc[n, 'Win Odds'])
                if odd < gate:
                    continue
                no_race += 1
                hot_sum += odd
                plc = df.loc[n, 'Plc.']
                try:
                    plc = int(plc)
                    if plc <= 3:
                        hot_win += 1
                except ValueError:
                    pass
    return hot_win/no_race, hot_sum/no_race


# return two sorted list showing the win prob and mean odd for a horse group of the given size and visualize
def extract_win(size, folder='./Data/Results/', place=False):

    def test(plc, place):
        try:
            if place:
                return int(plc) < 4
            else:
                return int(plc) == 1
        except ValueError:
            return False

    race_list = []
    for f in os.listdir(folder):
        with open(folder + f, 'rb') as file:
            result_list = pk.load(file)
            for df in result_list:
                df['Win Odds'] = pd.to_numeric(df['Win Odds'])
                df = df[['Win Odds', 'Plc.']]
                race_list.append(df)
    df = pd.concat(race_list, axis=0)
    df = df.sort_values('Win Odds')
    odds = df['Win Odds'].tolist()
    results = df['Plc.'].tolist()
    results = [test(plc, place) for plc in results]
    return range_visualize(odds, results, size)


# a, b = average_win_odd(1, gate=3)
# print(a, b)

wp, imo = extract_win(80, place=False)

imo = np.array(imo).reshape([-1, 1])
wp = np.array(wp)
model = LinearRegression()
poly = PolynomialFeatures(1)
imo = poly.fit_transform(imo)
model.fit(imo, wp)
print(model.score(imo, wp))









