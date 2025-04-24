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

