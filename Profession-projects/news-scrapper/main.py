from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime as dt
import csv
import os


url = "https://news.google.com/home?hl=en-US&gl=US&ceid=US:en"
chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=chrome_option)

driver.get(url)

WebDriverWait(driver, 60).until(
    EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Accept all')]"))
)

accept_btn = driver.find_element(By.XPATH, "//span[contains(text(), 'Accept all')]")
accept_btn.click()

current_url = driver.current_url

business_btn = driver.find_element(By.LINK_TEXT, "Business")
business_btn.click()

# Wait for URL to change
WebDriverWait(driver, 10).until(
    EC.url_changes(current_url)
)

time.sleep(3)

# Now get the articles from the new Business page
# Article link with text
titles = driver.find_elements(By.XPATH, "//a[contains(@href, './read/') and normalize-space(text())]")

file_exists = os.path.isfile('collection.csv')
with open('collection.csv', 'a') as file:
    csvwriter = csv.writer(file)
    if not file_exists:
        csvwriter.writerow(['date', 'title', 'link'])
    for title in titles:
        if title.text != "":
            row = [dt.datetime.now().date(), title.text, title.get_attribute('href')]
            csvwriter.writerow(row)