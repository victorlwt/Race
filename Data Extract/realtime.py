from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import pickle as pk
import time
import os

global T1, T2, T3


def getBasePage(url):
	global T1, T2, T3
	dr = webdriver.PhantomJS(executable_path='phantomjs.exe')
	dr.get(url)
	time.sleep(2)
	T1 = BeautifulSoup(dr.find_element_by_id("wpTable1").get_attribute("innerHTML"))
	T2 = BeautifulSoup(dr.find_element_by_id("combOddsTableQIN").get_attribute("innerHTML"))
	T3 = BeautifulSoup(dr.find_element_by_id("combOddsTableQPL").get_attribute("innerHTML"))
	dr.close()



def getData(name1, name2, name3):
	global T1, T2, T3
	table = T1.find_all("table")[1]
	df = pd.read_html(table.prettify())[0]
	df = df.drop(1, axis=1).drop(2, axis=1).drop(len(df)-1, axis=0)
	with open(name1, "wb") as f:
		pk.dump(df, f)

	table = T2.find("table")
	df = pd.read_html(table.prettify())[0]
	with open(name2, "wb") as f:
		pk.dump(df, f)

	table = T3.find("table")
	df = pd.read_html(table.prettify())[0]
	with open(name3, "wb") as f:
		pk.dump(df, f)


# getBasePage("https://bet.hkjc.com/racing/pages/odds_wpq.aspx?lang=en&dv=local")
# getData("realtimewin.df", "realtimeQIN.df", "realtimeQPL.df")
