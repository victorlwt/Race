import pickle as pk
import os
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import numpy as np
from itertools import combinations

from utility import range_visualize


# return two sorted list showing the quinella prob and mean odd for a horse group of the given size and visualize
def extract_quinella(size, folder='./Data/Results/', place=False):
    if place:
        test = lambda x: x < 4
    else:
        test = lambda x: x < 3
    odds = []
    results = []
    for f in os.listdir(folder):
        with open(folder + f, 'rb') as file:
            result_list = pk.load(file)
            for df in result_list:
                try:
                    df['Plc.'] = pd.to_numeric(df['Plc.'])
                    df['Win Odds'] = pd.to_numeric(df['Win Odds'])
                    df = df.reset_index(drop=True)
                except ValueError:
                    continue
                horse_no = [i for i in range(len(df))]
                for m, n in combinations(horse_no, 2):
                    odd1 = float(df.loc[m, 'Win Odds'])
                    odd2 = float(df.loc[n, 'Win Odds'])
                    plc1 = int(df.loc[m, 'Plc.'])
                    plc2 = int(df.loc[n, 'Plc.'])
                    odd = odd1 * odd2 / 2
                    r = test(plc1) and test(plc2)
                    odds.append(odd)
                    results.append(r)
    tmp = sorted(zip(odds, results), key=lambda pair: pair[0])
    odds = [i[0] for i in tmp]
    results = [i[1] for i in tmp]
    return range_visualize(odds, results, size)


wp, imo = extract_quinella(160, place=False)

imo = np.array(imo).reshape([-1, 1])
wp = np.array(wp)
model = LinearRegression()
poly = PolynomialFeatures(1)
imo = poly.fit_transform(imo)
model.fit(imo, wp)
print(model.score(imo, wp))