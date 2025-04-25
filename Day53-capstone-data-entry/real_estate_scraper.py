from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
import requests


class RealEstateScraper:
    def __init__(self, link):
        options = Options()
        options.add_argument("--headless")  # Run without opening a browser window
        self.driver = webdriver.Chrome(options=options)

        # Open the webpage
        self.driver.get(link)
        sleep(2)

        # Get the page source after it has loaded
        page_source = self.driver.page_source
        print(page_source)

        # Accessing webpage using Beautiful Soup
        self.soup = BeautifulSoup(self.page_source, "html.parser")
        print(self.soup.prettify())

    def get_listings(self):
        parent_div = self.soup.find("div", class_="property-section")
        listings = parent_div.find("div", class_="col-md-6 col-md-12 position-relative")
        # listings = self.soup.find("div", class_=["col-md-6", "col-md-12", "position-relative"])

# col-md-6 col-md-12 position-relative
        if listings:
            print(listings)
        else:
            print("Element not found.")

        listings_data = []

        for item in listings:
            link = item.find("a").get("href")
            print(link)
            location = item.find("h2", class_="p-0 m-0").getText(strip=True)
            print(location)
            price_text = item.find("h6").getText(strip=True)
            price = ''.join(c for c in price_text if c.isdigit())
            print(price)
            listing_data = {
                "link": link,
                "location": location,
                "price": price
            }

            # Append the dictionary to the list of listings data
            listings_data.append(listing_data)

        for item in listings_data:
            print(item["link"], item["location"], item["price"])

        return listings_data


contents = "https://www.nepremicnine.net/oglasi-oddaja/ljubljana-mesto/stanovanje/"

soup_bot = RealEstateScraper(contents)
# listings_data = soup_bot.get_listings()
