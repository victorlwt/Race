from .realtime import getBasePage, getData
date = input("Please input the date.")
no_of_races = int(input("Please input the number of races."))

for i in range(no_of_races):
	getBasePage("https://bet.hkjc.com/racing/pages/odds_wpq.aspx?lang=EN&date=" + date + "&venue=ST&raceno=" + str(i+1))
	n1 = "../Data/" + date + str(i+1) + "-win.df"
	n2 = "../Data/" + date + str(i+1) + "-QIN.df"
	n3 = "../Data/" + date + str(i+1) + "-QPL.df"
	getData(n1, n2, n3)