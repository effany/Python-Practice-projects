import plotly.express as px
from datetime import datetime, date
import time
import os
import pandas as pd
import requests
import json

class DataGraber:
    def __init__(self, base_url, apikey):
        self.base_url = base_url
        self.apikey = apikey

    def write_to_csv(self, data, filename):
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)

    def needs_refresh(self, filepath):
        needs_refresh = (
            not os.path.exists(filepath) or 
            datetime.fromtimestamp(os.path.getmtime(filepath)).date() != date.today()
        )

        return True if needs_refresh else False

    def load_top_gainers_losers(self, DataType, color_continuous_scale='Plasma'):
        filepath = f'./data/top-{DataType}.csv'
        
        needs_refresh = self.needs_refresh(filepath)

        if needs_refresh:
            try:
                url = self.base_url + '/query'
                params = {
                    'function': 'TOP_GAINERS_LOSERS',
                    'apikey': self.apikey
                }
                response = requests.get(url, params=params)
                data = response.json()
                self.write_to_csv(data[f'top_{DataType}'], filepath)
            except Exception as e:
                print(e)
                return {}

        df = pd.read_csv(f'./data/top-{DataType}.csv')
        df['change_percentage'] = df['change_percentage'].str.rstrip('%').astype(float)
        
        fig = px.bar(df, x='ticker', 
        y='change_percentage', 
        hover_data=['price', 'volume'],
        color='price',
        color_continuous_scale=color_continuous_scale,
        labels={'change_percentage': 'Change(%)','ticker':'Stock Symbol' },
        title=f"Top {DataType} at {date.today()}"
        )

        self.chart_html = fig.to_html(full_html=False)
        return self.chart_html

    def get_100_days_stock_price(self, stock_symbol):
        filepath = f"./data/100-days-stock-price-{stock_symbol}.csv"

        needs_refresh = self.needs_refresh(filepath)

        if needs_refresh:
            try:
                url = self.base_url + '/query'
                params = {
                    'function': 'TIME_SERIES_DAILY',
                    'symbol': stock_symbol,
                    'apikey': self.apikey 
                }
                response = requests.get(url, params=params)
                data = response.json()
                self.write_to_csv(data["Time Series (Daily)"], filepath)
            except Exception as e:
                print(e)
                return {}
        else:
            df = pd.read_csv(filepath)
            df = df.T
            df.columns = ['open', 'high', 'low', 'close', 'volume']
            df = df.reset_index()
            df.rename(columns={'index': 'date'})
            fig = px.line(df, 
                          x='index', 
                          y=['open','close'], 
                          title=f"Open/Close Price pass 100 days {stock_symbol}",
                          template='seaborn')
            fig.update_layout(
                xaxis_title="Date", 
                yaxis_title="Open/Close Value", 
                hovermode='x unified'
            )    
            self.chart_html = fig.to_html(full_html=False)
        return self.chart_html   

    def get_news_sentiments(self, stock):
        filepath = f'./data/news/{stock}.json' 
        needs_refresh = self.needs_refresh(filepath)
        stock = stock.upper()

        if needs_refresh:
            try:
                url = self.base_url + '/query'
                params = {
                    "function": "NEWS_SENTIMENT", 
                    "tickers": stock,
                    "apikey": self.apikey
                }       

                response = requests.get(url, params=params)
                data = response.json()
                with open(f'./data/news/{stock}.json', 'w') as file:
                    json.dump(data, file, indent=2)
                
            except Exception as e:
                print(e)
                return {}
        else:
            with open(f'./data/news/{stock}.json', 'r') as file:
                data = json.load(file)
                return data
