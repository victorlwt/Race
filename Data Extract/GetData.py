from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os
def getBasePage(date):
	url = "https://racing.hkjc.com/racing/information/English/Racing/LocalResults.aspx?RaceDate=" + date + "&Racecourse=ST&RaceNo=1"
	dr = webdriver.PhantomJS(executable_path=r'phantomjs.exe')
	dr.get(url)
	time.sleep(3)
	try:
		bsObj = BeautifulSoup(dr.page_source)
		dr.close()
		return bsObj
	except:
		dr.close()
		return None
def scrapeAllData(bp, date):
	t = bp.find_all("table", "js_racecard")
	if(len(t) == 0 or len(t[0].find("tbody").find_all("tr")) == 0):
		return False
	b = t[0].find("tbody").find_all("tr")[0].find_all("a")
	no_of_races = len(b)
	file = open(date.replace("/", "-") + ".txt", "w")
	for i in range(no_of_races):
	 	file.write(str(i+1) + "\n")
	 	if bp.find("div", "performance") == None:
	 		file.close()
	 		os.remove(date + ".txt")
	 		return False
	 	table = bp.find("div", "performance").find("table")
	 	# Remove all br tags
	 	for e in table.find_all("br"):
	 		e.extract()
	 	headings = table.find("thead").find_all("td")
	 	horses = table.find("tbody").find_all("tr")
	 	for heading in headings:
	 		file.write(heading.get_text() + "\t")
 		file.write("\n")
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
 					file.write(s.rstrip() + "\t")
 				elif len(t2) != 0:
 					file.write(t2[0].get_text().strip() + "\t")
 				else:
 					file.write(att.get_text().strip() + "\t")
 			file.write("\n")
	file.close()
	return True


num_lines = sum(1 for line in open('valid_dates.txt'))
with open("valid_dates.txt","r") as f:
	print("There are " + str(num_lines) + " dates in total.")
	count = 1
	success = 0
	for d in f:
		date = d.strip()
		basePage = getBasePage(date)
		if basePage == None:
			print("Error of accessing the page")
		else:
			is_success = scrapeAllData(basePage, date)
			# Try one more time
			if not is_success:
				basePage = getBasePage(date)
				if basePage == None:
					print("Error of accessing the page")
				else:
					is_sucess = scrapeAllData(basePage, date)
			if is_success:
				success = success + 1
				print(str(success) + " file(s) has been successfully created...(" + str(count) + "/" + str(num_lines) + ")")
		count = count + 1
