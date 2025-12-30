import os
from dotenv import load_dotenv
import requests

load_dotenv()

api_key = os.environ.get("API_ACCESS_TOKEN")

headers = {
            "accept": "application/json", 
            "Authorization": f"Bearer {api_key}"
        }

response = requests.get("https://image.tmdb.org/t/p/w500/AuqQnz7NcBJrYqIEYTRLFTEdg79.jpg", headers=headers)

print(response.status_code)