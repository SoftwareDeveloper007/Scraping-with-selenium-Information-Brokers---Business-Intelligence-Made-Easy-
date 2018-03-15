from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import xlrd, openpyxl, csv
# import datetime
from datetime import datetime

from datetime import datetime, tzinfo, timedelta

class UTC(tzinfo):
    def utcoffset(self, dt):
         return timedelta(0)
    def tzname(self, dt):
        return "UTC"
    def dst(self, dt):
        return timedelta(0)

class mainScraper():
    def __init__(self):
        csv_file_name = "Data/director search sample 100k.csv"
        input_file = open(csv_file_name, "r", encoding="utf-8").read()
        self.input_dt = []
        for i, row in enumerate(input_file.split("\n")):
            if i==0:
                continue
            if row:
                self.input_dt.append(row.split("\t"))
        print(self.input_dt)
        print(len(self.input_dt))

    def scrapeUnit(self):

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')  # Last I checked this was necessary.
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='WebDriver/chromedriver.exe')
        driver.maximize_window()

if __name__ == '__main__':
    app = mainScraper()


