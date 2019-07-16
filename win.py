import pickle as pk
import os
import pandas as pd


no_race = 0
hot_win = 0
hot_sum = 0
for f in os.listdir('./Data/Results'):
    with open('./Data/Results/' + f, 'rb') as file:
        result_list = pk.load(file)
        for df in result_list:
            df['Win Odds'].apply(pd.to_numeric)
            df = df.sort_values('Win Odds')
            no_race += 1
            hot_sum += float(df.loc[0, 'Win Odds'])
            if int(df.loc[0, 'Plc.']) == 1:
                hot_win += 1
print(hot_win/no_race, hot_sum/no_race)

