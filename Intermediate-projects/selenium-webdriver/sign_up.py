from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

url="https://secure-retreat-92358.herokuapp.com/"
chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=chrome_option)

driver.get(url)

first_name_el = driver.find_element(By.NAME, value="fName")
last_name_el = driver.find_element(By.NAME, value="lName")
email_el = driver.find_element(By.NAME, value="email")
submit_el = driver.find_element(By.CLASS_NAME, value="btn-primary")

first_name_el.send_keys("test")
last_name_el.send_keys("effany")
email_el.send_keys("effany12334@gmail.com")
submit_el.send_keys(Keys.ENTER)

