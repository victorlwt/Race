import pickle as pk
from getOddData import getBasePage, getData


date = input("Please input the date:")
no_of_races = int(input("Please input the number of races:"))

odds_list = []
for i in range(no_of_races):
	getBasePage("https://bet.hkjc.com/racing/pages/odds_wpq.aspx?lang=EN&date=" + date + "&venue=ST&raceno=" + str(i+1))
	race_odd = getData()
	odds_list.append(race_odd)
	print(i + 1, 'races scraped.')
with open('../Data/Odds/' + date + '_odd.dfdl', 'wb') as f:
	pk.dump(odds_list, f)
