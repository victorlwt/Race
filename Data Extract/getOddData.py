from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time

global T1, T2, T3


def getBasePage(url):
	global T1, T2, T3
	options = webdriver.ChromeOptions()
	options.add_argument("--disable-extensions")
	options.add_argument("--headless")
	dr = webdriver.Chrome(chrome_options=options)
	dr.get(url)
	time.sleep(2)
	T1 = BeautifulSoup(dr.find_element_by_id("wpTable1").get_attribute("innerHTML"))
	T2 = BeautifulSoup(dr.find_element_by_id("combOddsTableQIN").get_attribute("innerHTML"))
	T3 = BeautifulSoup(dr.find_element_by_id("combOddsTableQPL").get_attribute("innerHTML"))
	dr.close()


def getData():

	global T1, T2, T3
	odd_dict = {}

	table = T1.find_all("table")[1]
	df = pd.read_html(table.prettify())[0]
	df = df.drop(1, axis=1).drop(2, axis=1).drop(len(df)-1, axis=0)
	odd_dict['wp'] = df

	table = T2.find("table")
	df = pd.read_html(table.prettify())[0]
	odd_dict['q'] = df

	table = T3.find("table")
	df = pd.read_html(table.prettify())[0]
	odd_dict['qp'] = df
