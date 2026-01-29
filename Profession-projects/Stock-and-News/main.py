from flask import Flask, render_template, jsonify, request, redirect, flash, abort, session, url_for
import os
from dotenv import load_dotenv
import requests

import csv
import plotly.express as px
from datetime import datetime, date
import time
from pathlib import Path
from data_graber import DataGraber

load_dotenv()

app = Flask(__name__)

base_url = 'https://www.alphavantage.co'
stock_api_key = os.environ.get('STOCK_API_KEY')

data_graber = DataGraber(base_url, stock_api_key)

@app.route('/', methods=['GET', 'POST'])
def home():
    # Handle stock search if form is submitted
    if request.method == "POST":
        stock = request.form.get('stock')
        if stock:
            stock = stock.upper()
            return redirect(url_for('show_stock_trend', stock=stock))
    
    if request.method == "POST":
        search_news = request.form.get('news')
        if search_news:
            search_news.upper()
            return redirect(url_for('show_news_setiments', stock=search_news))

    
    # Always load the default charts for GET requests
    top_gainers_chart = data_graber.load_top_gainers_losers('gainers')
    top_losers_chart = data_graber.load_top_gainers_losers('losers', color_continuous_scale='Viridis')
    
    return render_template('index.html', 
                         top_gainers_chart=top_gainers_chart, 
                         top_losers_chart=top_losers_chart)


@app.route('/100-days-price/<stock>', methods=["GET", "POST"])
def show_stock_trend(stock):
    stock_chart = data_graber.get_100_days_stock_price(stock)
    return render_template('chart.html', stock_chart=stock_chart, stock=stock)


@app.route('/news-sentiments/<stock>', methods=["GET", "POST"])

def show_news_setiments(stock):
    news = data_graber.get_news_sentiments(stock)
    return render_template('news-sentiments.html', stock=stock,  news=news)

