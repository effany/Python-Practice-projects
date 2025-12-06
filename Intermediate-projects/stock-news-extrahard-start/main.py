import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
load_dotenv()
from twilio.rest import Client

# STOCK = "TSLA"
STOCK = "CRM"
# COMPANY_NAME = "Tesla"
COMPANY_NAME = "Salesforce"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

today = datetime.today()
yesterday = str((today - timedelta(days=1)).date())
day_before_yesterday = str((today - timedelta(days=2)).date())
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

stock_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY"
stock_parameters = {
    "apikey": os.environ.get("STOCK_API_KEY"),
    "symbol": STOCK
}

news_url = "https://newsapi.org/v2/everything"
news_parameters = {
    'q': COMPANY_NAME.lower(),
    'from': yesterday, 
    'apiKey': os.environ.get("NEWS_API_KEY")
}

response = (requests.get(stock_url, stock_parameters)).json()

yesterday_closing_price = float(response['Time Series (Daily)'][yesterday]["4. close"])
day_before_yesterday_closing_price = float(response['Time Series (Daily)'][day_before_yesterday]["4. close"])


if yesterday_closing_price > day_before_yesterday_closing_price:
    stock_direction = "up"
    print("stock increase")
    close_price_differences = yesterday_closing_price - day_before_yesterday_closing_price
elif day_before_yesterday_closing_price > yesterday_closing_price:
    stock_direction = "down"
    print("stock decrease")
    close_price_differences = day_before_yesterday_closing_price - yesterday_closing_price


price_differences_ratio = round((close_price_differences / day_before_yesterday_closing_price) * 100, 4)

print(price_differences_ratio)

if abs(price_differences_ratio) > 5: 
    news_response = requests.get(news_url, news_parameters).json()
    top_3_news_headline = [news_response["articles"][i]['title'] for i in range(3)] 
    top_3_news_brief = [news_response["articles"][i]["description"] for i in range(3)]
    
    if stock_direction == "up":
        icon = "🔺"
    elif stock_direction == "down":
        icon = "🔻"
    for i in range(3):
        message = f"{STOCK} {icon} {price_differences_ratio}% \n Headline: {top_3_news_headline[i]}\n Brief: {top_3_news_brief[i]}"
        client = Client(account_sid, auth_token)
        message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=f"{message}",
        to='whatsapp:+420735032331'
        )
   




