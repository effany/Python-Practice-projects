import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 50.075539 # Your latitude
MY_LONG = 14.437800 # Your longitude

my_email = "your mail"
password = "your app pass"

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}



#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.

def iss_position_within_range():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG -5 <= iss_longitude <= MY_LONG + 5:
        return True
    

def is_night():
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    print("sunset", sunset)
    time_now = datetime.now()
    if time_now.hour >= sunset or time_now.hour <= sunrise:
        return True 
     

def send_email(to_address):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs=to_address, msg=f"Subject: Look up!\n\nIss is now over your head!! Dont miss it")


while True:
    time.sleep(60)
    if is_night() and iss_position_within_range():
        print("email sent")
        send_email("effany28119@gmail.com") 
    else:
        print("not yet")
