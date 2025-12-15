from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import datetime
from datetime import timedelta

url="https://ozh.github.io/cookieclicker/"

chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option("detach", True)
driver = webdriver.Chrome(options = chrome_option)
driver.get(url)
time.sleep(2)  # Give the page time to load

language_el = driver.find_element(By.ID, value="langSelect-EN")
language_el.click()

time.sleep(2)
cookies_el = driver.find_element(By.ID, value="bigCookie")

mins = 5
current_time = datetime.datetime.now()
end_time = current_time + timedelta(minutes=5)
last_purchase_time = datetime.datetime.now()

while current_time < end_time:
    current_time = datetime.datetime.now()
    
    # Keep clicking cookies
    for _ in range(500):
        cookies_el.click()
    
    # Every 5 seconds, try to purchase the most expensive affordable upgrade
    if (datetime.datetime.now() - last_purchase_time).total_seconds() >= 5:
        avaliable_items_to_purchase = driver.find_elements(By.CSS_SELECTOR, value=".product.unlocked.enabled")
        
        if len(avaliable_items_to_purchase) > 0:
            prices_el = [i.find_element(By.CLASS_NAME, value="price").text for i in avaliable_items_to_purchase]
            max_price = max([int(price.replace(",", "")) for price in prices_el])
            
            for i in avaliable_items_to_purchase:
                price = i.find_element(By.CLASS_NAME, value="price")
                price_int = int(price.text.replace(",", ""))
                if price_int == max_price:
                    product_name_el = i.find_element(By.CLASS_NAME, value="productName")
                    print(f"Purchasing: {product_name_el.text} for {max_price} cookies")
                    i.click()
                    break
        
        last_purchase_time = datetime.datetime.now()
    
driver.quit()