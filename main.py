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
import time

from datetime import datetime, tzinfo, timedelta


class UTC(tzinfo):
    def utcoffset(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return timedelta(0)

month_list = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}

class mainScraper():
    def __init__(self):
        csv_file_name = "Data/director search sample 100k.csv"
        input_file = open(csv_file_name, "r", encoding="utf-8").read()
        self.input_dt = []
        for i, row in enumerate(input_file.split("\n")):
            if i == 0:
                continue
            if row:
                self.input_dt.append(row.split("\t"))

        self.input_dt.reverse()
        # print(self.input_dt)

    def totalScraping(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument('--disable-gpu')  # Last I checked this was necessary.
        chrome_options.add_argument("download.default_directory=C:/Downloads")
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='WebDriver/chromedriver.exe')
        driver.maximize_window()
        self.url = "https://www.ib.com.au/buy/295/asic-personal-name-extract"
        driver.get(self.url)

        while self.input_dt:
            driver.delete_all_cookies()
            driver = self.scrapeUnit(driver)

    def scrapeUnit(self, driver):
        [firstname, lastname, birthday] = self.input_dt.pop()
        # [firstname, lastname, birthday] = ["James", "L'Almont", "1986-06-06"]

        birthday = birthday.split("-")
        birthday = "{:04d}-{:02d}-{:02d}".format(int(birthday[2]), month_list[birthday[1]], int(birthday[0]))

        surname_form = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input#surname"))
        )

        action_chain = ActionChains(driver)
        action_chain.move_to_element(surname_form).click(surname_form).key_down(Keys.CONTROL).send_keys('a').\
            key_up(Keys.CONTROL).send_keys(Keys.DELETE).send_keys(lastname).send_keys(
            Keys.ENTER).perform()

        firstname_form = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input#firstName"))
        )

        action_chain = ActionChains(driver)
        action_chain.move_to_element(firstname_form).click(firstname_form).key_down(Keys.CONTROL).send_keys('a').\
            key_up(Keys.CONTROL).send_keys(Keys.DELETE).send_keys(firstname).send_keys(
            Keys.ENTER).perform()

        start_form = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input#start"))
        )
        action_chain = ActionChains(driver)
        action_chain.move_to_element(start_form).click(start_form).key_down(Keys.CONTROL).send_keys('a').\
            key_up(Keys.CONTROL).send_keys(Keys.DELETE).send_keys(birthday).send_keys(Keys.ENTER).perform()

        end_form = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input#end"))
        )
        action_chain = ActionChains(driver)
        action_chain.move_to_element(end_form).click(end_form).key_down(Keys.CONTROL).send_keys('a').\
            key_up(Keys.CONTROL).send_keys(Keys.DELETE).send_keys(birthday).send_keys(Keys.ENTER).perform()

        search_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button#do_search"))
        )

        search_btn.click()

        time.sleep(5)

        try:

            captcha_audio_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.rc-button.goog-inline-block.rc-button-audio"))
            )

            captcha_audio_btn.click()
            print("captcha audio button is clicked!")
            audio_download_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.rc-audiochallenge-tdownload-link"))
            )

            audio_url = audio_download_btn.get_attribute('href')
            print(audio_url)

        except:
            pass


        try:
            # rows = WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.XPATH, "//table[@id='content-table']/tbody/tr"))
            # )
            #
            # for row in rows:
            #     record_id = row.find_element_by_xpath("td[2]").text
            #     name = row.find_element_by_xpath("td[3]").text
            #     birth_place = row.find_element_by_xpath("td[5]").text
            #     former_name = row.find_element_by_xpath("td[6]").text


            record_id = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//table[@id='content-table']/tbody/tr/td[2]"))
            )
            record_id = record_id.text
            birth_place = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//table[@id='content-table']/tbody/tr/td[5]"))
            )
            birth_place = birth_place.text

            search_again_btn = driver.find_element_by_css_selector("span#search_again")
            search_again_btn.click()
            action_chain = ActionChains(driver)
            action_chain.move_to_element(search_again_btn).click(search_again_btn).perform()
            # driver.get(self.url)

        except:
            record_id = ""
            birth_place = ""

        try:
            alert = driver.switch_to.alert
            alert.accept()

        except:
            pass


        logTxt = "+-+-+-+-+-+- First Name: {}, Last Name: {} +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-".format(firstname, lastname)
        print(logTxt)
        logTxt = "Record ID:\t{}\nBirth Place:\t{}".format(record_id, birth_place)
        print(logTxt)
        # driver.quit()
        return driver

if __name__ == '__main__':
    app = mainScraper()
    app.totalScraping()
