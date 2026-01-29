import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from data_graber import DataGraber
import os
from dotenv import load_dotenv
load_dotenv()

base_url = 'https://www.alphavantage.co'
stock_api_key = os.environ.get('STOCK_API_KEY')

data_graber = DataGraber(base_url, stock_api_key)

# response = data_graber.get_100_days_stock_price('UUUU')

# print(response)

data_graber.get_news_sentiments('tsm')