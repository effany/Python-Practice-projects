import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import lxml
import requests

class Scrapper:
    def __init__(self):
        load_dotenv()
        self.web_url = os.environ.get("PROPERTY_WEB_URL")
        
        self.header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
        }
        response = requests.get(self.web_url, headers=self.header).text
        self.soup = BeautifulSoup(response, "html.parser")
    
    def get_property_listings(self):
        listings = self.soup.find_all("article")
        properties = []
        for list in listings:
            link = list.find('a').get('href')
            address = list.find("address").getText().strip()
            price = list.find('span', {'data-test': 'property-card-price'}).text
            sanitized_price = price.split()[0].replace("$", '').replace("/mo", "").replace(",","").replace("+", "")
            properties.append({"address": address, "price": sanitized_price, "link": link}) 
        return properties
        