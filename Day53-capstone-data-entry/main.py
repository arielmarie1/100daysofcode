from google_form_bot import GoogleFormBot
from real_estate_scraper import RealEstateScraper
from dotenv import load_dotenv
import os

# Adding link to google form for data entry
load_dotenv()
google_form = os.getenv("GOOGLE_FORM")

# Loading Real Estate Website webpage
contents = "https://appbrewery.github.io/Zillow-Clone/"

soup_bot = RealEstateScraper(contents)
listings_data = soup_bot.get_listings()
bot = GoogleFormBot()
bot.fill_form(google_form, listings_data)
bot.close_browser()
