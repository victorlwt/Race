from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os


def getHorseData():
    url = "https://racing.hkjc.com/racing/information/chinese/Racing/LocalResults.aspx?RaceDate=2019/07/14&Racecourse=ST&RaceNo=1"
    dr = webdriver.Chrome()
    dr.get(url)
    time.sleep(2)
    elem = dr.find_element_by_class_name('performance')
    elems = elem.find_elements_by_tag_name('a')
    i = 0
    for e in elems:
        print(e.text)

getHorseData()


