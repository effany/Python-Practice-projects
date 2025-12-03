##################### Extra Hard Starting Project ######################

# 1. Update the birthdays.csv

# 2. Check if today matches a birthday in the birthdays.csv

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv

# 4. Send the letter generated in step 3 to that person's email address.

import smtplib
import random
import pandas as pd
import datetime as dt
import os

data = pd.read_csv("birthdays.csv", index_col=False)
name_list = list(data["name"])
email_list = list(data["email"])
day_list = list(data["day"])
month_list = list(data["day"])
today = dt.datetime.now()
files = os.listdir("./letter_templates/")
random_file = random.choice(files)
base_path = "./letter_templates/"
my_email = "YOUR EMAIL"
password = "APP PASSWORD"

def send_mail(to_addrs,message):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs=to_addrs, msg=f"Subject:Happy Birthday\n\n{message}")

for i, name in data["name"].items():
    current_month = today.month
    current_date = today.day
    if int(data["month"][i]) == current_month and int(data["day"][i] == current_date):
        with open(f"{base_path}/{random_file}") as file:
            letter = file.read()
            adjusted_letter = letter.replace("[NAME]", data["name"][i])
            send_mail(f'{data["email"][i]}', adjusted_letter)
  

## method2: new_dict = {mew_key: new_value for (index, data) in data.iterrows()}

birthdays_dict = {(data["month"], data["day"]): data for (index, data) in data.iterrows()}
today_tuple = (today.month, today.day)
if today_tuple in birthdays_dict:
    print(today_tuple, birthdays_dict[today_tuple])


## you can run the code on the cloud here 
# https://www.pythonanywhere.com/registration/register/beginner/