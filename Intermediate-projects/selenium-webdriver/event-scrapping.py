from selenium import webdriver
from selenium.webdriver.common.by import By

url = "https://www.python.org/"
chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_option)
driver.get(url)
event_times = driver.find_elements(By.CSS_SELECTOR, value=".event-widget ul time")
event_names = driver.find_elements(By.CSS_SELECTOR, value=".event-widget ul a")

events = {}

for n in range(len(event_times)):
    events[n] = {
        "time": event_times[n].text,
        "name": event_names[n].text
    }

print(events)

driver.quit()
