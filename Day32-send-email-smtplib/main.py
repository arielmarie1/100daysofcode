import smtplib
from email.message import EmailMessage
import datetime as dt
import random
from dotenv import load_dotenv
import os

# Loading email
load_dotenv()
my_email = os.getenv("MY_EMAIL")
password = os.getenv("OTP")

# Monday Motivational quote
now = dt.datetime.now()
if now.weekday() == 0:

    # Open file quotes.txt
    with open("quotes.txt", encoding="utf-8") as quotes:
        all_quotes = quotes.readlines()
        quote = random.choice(all_quotes)  # Randomly select a quote from file

    # Email message
    msg = EmailMessage()
    msg['From'] = my_email
    msg['To'] = my_email
    msg["Subject"] = "Monday Motivation"
    msg.set_content(quote)

    # Sending email
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.send_message(msg)
