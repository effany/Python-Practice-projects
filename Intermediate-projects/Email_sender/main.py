import smtplib
import datetime as dt
import random
import os
from dotenv import load_dotenv
load_dotenv()


today = dt.datetime.now()
day_of_week = today.weekday()
my_email = "EMAIL"
password = os.environ.get("PASSWORD")

if day_of_week == 1:
    with open("quotes.txt", "r") as file:
        quote_array = file.readlines()
        random_quote = random.choice(quote_array)

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email,
                            to_addrs="EMAIL", 
                            msg=f"Subject:Hello\n\n{random_quote}"
                            )

# date_of_birth = dt.datetime(year=1995, month=2, day=8, hour=17)
# print(date_of_birth)
