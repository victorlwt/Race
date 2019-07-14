from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os
from io import StringIO
import pandas as pd


def getBasePage(date):
	url = "https://racing.hkjc.com/racing/information/English/Racing/LocalResults.aspx?RaceDate=" + date + "&Racecourse=ST&RaceNo=1"
	dr = webdriver.PhantomJS(executable_path='Data Extract/phantomjs.exe')
	dr.get(url)
	time.sleep(2)
	try:
		bsObj = BeautifulSoup(dr.page_source)
		dr.close()
		return bsObj
	except:
		dr.close()
		return None


def scrapeAllData(bp, date):
	t = bp.find_all("table", "js_racecard")
	if len(t) == 0 or len(t[0].find("tbody").find_all("tr")) == 0:
		return False
	b = t[0].find("tbody").find_all("tr")[0].find_all("a")
	no_of_races = len(b)
	file = open("Data/" + date.replace("/", "-") + ".csv", "w")
	for i in range(no_of_races):
		table_string = ''
		table_string += (str(i + 1) + "\n")
		if bp.find("div", "performance") is None:
			file.close()
			os.remove(date + ".csv")
			return False
		table = bp.find("div", "performance").find("table")
		# Remove all br tags
		for e in table.find_all("br"):
			e.extract()
		headings = table.find("thead").find_all("td")
		horses = table.find("tbody").find_all("tr")
		for heading in headings:
			table_string += (heading.get_text() + ",")
		table_string += "\n"
		for horse in horses:
			atts = horse.find_all("td")
			for att in atts:
				# Check if this is a name
				t = att.find_all("div")
				t2 = att.find_all("a")
				if len(t) != 0:
					s = ""
					for x in t[1:]:
						s += x.get_text().strip() + " "
					table_string += (s.rstrip() + ",")
				elif len(t2) != 0:
					table_string += (t2[0].get_text().strip() + ",")
				else:
					table_string += (att.get_text().strip() + ",")
			table_string += "\n"
		csv = StringIO(table_string)
		df = pd.read_csv(csv)
		print(df)
		print(date)
	file.close()
	return True


os.chdir(os.pardir)
num_lines = sum(1 for line in open('Data Extract/valid_dates.txt'))
with open("Data Extract/valid_dates.txt", "r") as f:
	print("There are " + str(num_lines) + " dates in total.")
	count = 1
	success = 0
	for d in f:
		date = d.strip()
		basePage = getBasePage(date)
		scrapeAllData(basePage, date)
		
