import realtime
date = input("Please input the date.")
no_of_races = input("Please input the number of races.")

for i in range(no_of_races):
	getBasePage("https://bet.hkjc.com/racing/pages/odds_wpq.aspx?lang=EN&date=" + date + "&venue=ST&raceno=" + str(i+1))
	n1 = "../Data/" + date + "-win.df"
	n2 = "../Data/" + date + "-QIN.df"
	n3 = "../Data/" + date + "-QPL.df"
	getData(n1, n2, n3)