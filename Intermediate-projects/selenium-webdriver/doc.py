from selenium import webdriver
from selenium.webdriver.common.by import By

url="https://www.amazon.de/-/en/Containers-Programmes-Smoothie-Milkshakes-NC300EUCP/dp/B0CXXX6Z2H?pd_rd_w=6etPq&content-id=amzn1.sym.1f4ab70d-e4c2-4163-adb8-f439441a894e&pf_rd_p=1f4ab70d-e4c2-4163-adb8-f439441a894e&pf_rd_r=GR5PH87110TKR9S1EAYN&pd_rd_wg=hkqoa&pd_rd_r=f42d1149-4b95-4b24-9cf6-296780e090b9&pd_rd_i=B0CXXX6Z2H&ref_=oct_dx_dotd_B0CXXX6Z2H"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

price_dollar = driver.find_element(By.CLASS_NAME, value="a-price-whole")
print(price_dollar.text)

driver.quit()



# search_bar = driver.find_element(By.NAME, value="q")
#print(search_bar.tag_name)
#print(search_bar.get_attribute("placeholder"))
#button = driver.find_element(By.ID, value="submit")
#button.size
# doc_link = driver.find_element(By.CSS_SELECTOR, value = ".documentation-widget a")
# print(doc_link.text)
# right click and copy xpath in browser to find the element 
#x_path = driver.find_element(By.XPATH, value='//*[@id="selenium-with-python"]/h1/text()')
# print(x_path.text)
# find all the elements
#driver.find_elements(By.CLASS_NAME)

#close one tab
#driver.close()



#quit the entire browser