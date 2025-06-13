import smtplib
from dotenv import load_dotenv
import os

# Adding link to google form for data entry
load_dotenv()
my_email = os.getenv("MY_EMAIL")
password = os.getenv("OTP")

connection = smtplib.SMTP("smtp.gmail.com", port=587)
connection.starttls()
connection.login(user=my_email, password=password)
connection.sendmail(from_addr=my_email, to_addrs=my_email, msg="Hello")
connection.close()
