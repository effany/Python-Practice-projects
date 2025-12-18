from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import os
from dotenv import load_dotenv

load_dotenv()

tinder_url = "https://tinder.com/"
fb_email = os.environ.get("FB_EMAIL")
fb_password = os.environ.get("FB_PASSWORD")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(2)

driver.get(tinder_url)
accept_btn = driver.find_element(By.XPATH, value='//*[@id="u-1445010807"]/div/div[2]/div/div/div[1]/div[1]/button/div[2]/div[2]/div')
accept_btn.click()
driver.implicitly_wait(2)

login_btn = driver.find_element(By.LINK_TEXT, value="Log in")
login_btn.click()

base_window = driver.window_handles[0]
print(base_window.title)

try:
    language_selection = driver.find_element(By.CSS_SELECTOR, value='a[aria-label="English"]')
    language_selection.click()
except NoSuchElementException:
    pass

driver.implicitly_wait(1)

login_with_facebook_btn = driver.find_element(By.CSS_SELECTOR, value='button[aria-label="Login with Facebook"]')
login_with_facebook_btn.click()

fb_login_window = driver.window_handles[1]
driver.switch_to.window(fb_login_window)
try:
    allow_all_cookies_fb = driver.find_element(By.XPATH, value='/html/body/div[2]/div[2]/div/div/div/div/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div')
    allow_all_cookies_fb.click()
except NoSuchElementException:
    pass

driver.implicitly_wait(1)
fb_email_el = driver.find_element(By.NAME, value="email")
fb_password_el = driver.find_element(By.NAME, value="pass")
fb_login_el = driver.find_element(By.NAME, value="login")
fb_email_el.send_keys(fb_email)
fb_password_el.send_keys(fb_password)
fb_login_el.click()

driver.implicitly_wait(1)

try:
    second_allow_all_cookies = driver.find_element(By.XPATH, value="/html/body/div[4]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[1]/div/div[1]/div/span/span")
    second_allow_all_cookies.click()
except NoSuchElementException:
    pass


log_in_as_btn_el = driver.find_element(By.XPATH, value="/html/body/div[1]/div/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div[3]/div/div/div/div/div[2]/div[1]/div/div/div/div")
log_in_as_btn_el.click()

## Not able to continue because Tinder require verification 