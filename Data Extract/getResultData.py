from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import pickle as pk
from datetime import datetime

options = webdriver.ChromeOptions()
options.add_argument("--disable-extensions")
options.add_argument("--headless")
dr = webdriver.Chrome(chrome_options=options)


def getBasePage(date, race_no):
    url = "https://racing.hkjc.com/racing/information/English/Racing/LocalResults.aspx?RaceDate=" + date + "&Racecourse=ST&RaceNo=" + str(race_no)
    dr.get(url)
    time.sleep(0.5)
    bsObj = BeautifulSoup(dr.page_source, 'lxml')
    return bsObj


def scrapeTable(bp):
    table = bp.find('div', class_='performance')
    race = bp.find('div', class_='race_tab')
    meeting = bp.find('div', class_='raceMeeting_select')
    venue = meeting.find('span', class_='f_fl f_fs13').text
    venue = venue[25:].strip()
    mode = race.find('td', style='width: 385px;').text
    going = race.find('td', colspan='14').text
    table = table.find('table', class_='f_tac table_bd draggable')
    df = pd.read_html(str(table))[0]
    for i in range(len(df)):
        if df.loc[i, 'Win Odds'] == '---':
            df = df.drop(i, axis=0)
    df['Mode'] = [mode for _ in range(len(df))]
    df['Going'] = [going for _ in range(len(df))]
    df['Venue'] = [venue for _ in range(len(df))]
    return df


num_lines = sum(1 for line in open('valid_dates.txt'))
with open("valid_dates.txt", "r") as f:
    print("There are " + str(num_lines) + " dates in total.")
    count = 1
    success = 0
    i = 1
    for d in f:
        day = []
        d = d.strip()
        dstr = datetime.strptime(d, '%d/%m/%Y').strftime('%Y%m%d')
        i = 0
        while True:
            try:
                i += 1
                bp = getBasePage(d, i)
                df = scrapeTable(bp)
                day.append(df)
            except AttributeError:
                break
        if len(day) != 0:
            print(len(day), 'races in', d, 'scrapped.')
            f = open('../Data/Results/' + dstr + '_result.dfl', 'wb')
            pk.dump(day, f)
            f.close()

dr.close()
