from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os

# Adding link to google form for data entry
load_dotenv()
google_form = os.getenv("GOOGLE_FORM")

# Loading Real Estate Website webpage
contents = "https://appbrewery.github.io/Zillow-Clone/"
response = requests.get(contents)
zillow_website = response.text

# Accessing webpage using Beautiful Soup
soup = BeautifulSoup(zillow_website, "html.parser")
listings = soup.find_all(name="li", class_="ListItem-c11n-8-84-3-StyledListCardWrapper")

for item in listings:
    link = item.find("a").get("href")
    address = item.find("address").getText(strip=True)
    price_text = item.find("span").getText(strip=True)
    price = ''.join(c for c in price_text if c.isdigit())
    print(f"Link: {link + "\n"}Address: {address + "\n"}Price: {price + "\n"}")




