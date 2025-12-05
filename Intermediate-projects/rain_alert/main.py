import requests
from twilio.rest import Client
import os

account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("API_KEY")

weather_params = {
    "lat": 50.07, 
    "lon": 14.43,
    "appid": api_key,
    "cnt": 4
}

response = requests.get(OWM_Endpoint, params = weather_params)
response.raise_for_status()
weather_data = response.json()

will_rain = False 

for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"] 
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    from_='whatsapp:+14155238886',
    body="Bring you umbrella today.",
    to='whatsapp:+420735032331'
    )
