from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

url = "https://en.wikipedia.org/wiki/Main_Page"
chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_option)
driver.get(url)

article_nums = driver.find_element(By.XPATH, value='//*[@id="articlecount"]/ul/li[2]/a[1]')
# article_nums.click()

# find element by link text

all_portals = driver.find_element(By.LINK_TEXT, value = "Content portals")
#all_portals.click()

# type the text 

search = driver.find_element(By.NAME, value="search")

search.send_keys("Python")

# import key class to send keys
search.send_keys(Keys.ENTER)




