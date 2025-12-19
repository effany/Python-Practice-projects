from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DATAFILLER:
    def __init__(self):
        load_dotenv()
        url = os.environ.get("GOOGLE_FORM")
        chrome_option = webdriver.ChromeOptions()
        chrome_option.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_option)
        self.driver.get(url)

    def fill_form(self, data_array):
        time.sleep(2)
        for data in data_array:
            WebDriverWait(self.driver, 60).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="text"]')))

            fields_to_input = self.driver.find_elements(By.CSS_SELECTOR, value='input[type="text"]')
            
            # Fill each field with corresponding datß
            fields_to_input[0].send_keys(data['address'])
            fields_to_input[1].send_keys(data['price'])
            fields_to_input[2].send_keys(data['link'])

            submit_btn = self.driver.find_element(By.CSS_SELECTOR, value='div[role="button"]')
            submit_btn.click()
            
            time.sleep(2)
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.LINK_TEXT, "Nog een antwoord verzenden"))
            )
            # Click "Submit another response" link to get back to the form
            another_response_link = self.driver.find_element(By.LINK_TEXT, value='Nog een antwoord verzenden')
            another_response_link.click()
            
        self.driver.quit()
            