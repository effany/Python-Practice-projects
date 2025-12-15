from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
from datetime import timedelta

url = "https://ozh.github.io/cookieclicker/"

chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_option)
driver.get(url)
time.sleep(2)

language_el = driver.find_element(By.ID, value="langSelect-EN")
language_el.click()

time.sleep(2)
cookies_el = driver.find_element(By.ID, value="bigCookie")

end_time = datetime.datetime.now() + timedelta(minutes=5)
last_purchase_time = datetime.datetime.now()

while datetime.datetime.now() < end_time:
    # Keep clicking cookies
    cookies_el.click()
    
    # Every 5 seconds, try to purchase the most expensive affordable upgrade
    if (datetime.datetime.now() - last_purchase_time).total_seconds() >= 5:
        avaliable_items = driver.find_elements(By.CSS_SELECTOR, ".product.unlocked.enabled")
        
        if avaliable_items:
            try:
                # Find max price
                prices = [int(item.find_element(By.CLASS_NAME, "price").text.replace(",", "")) 
                         for item in avaliable_items]
                max_price = max(prices)
                
                # Purchase the item with max price
                for item in avaliable_items:
                    price_text = item.find_element(By.CLASS_NAME, "price").text.replace(",", "")
                    if int(price_text) == max_price:
                        product_name = item.find_element(By.CLASS_NAME, "productName").text
                        print(f"Purchasing: {product_name} for {max_price} cookies")
                        item.click()
                        break
            except (ValueError, Exception) as e:
                print(f"Error during purchase: {e}")
        
        last_purchase_time = datetime.datetime.now()

driver.quit()