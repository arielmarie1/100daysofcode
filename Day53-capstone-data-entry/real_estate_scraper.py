from bs4 import BeautifulSoup
import requests


class RealEstateScraper:
    def __init__(self, link):
        self.response = requests.get(link)
        self.website = self.response.text
        # Accessing webpage using Beautiful Soup
        self.soup = BeautifulSoup(self.website, "html.parser")

    def get_listings(self):
        listings = self.soup.find_all(
            name="li",
            class_="ListItem-c11n-8-84-3-StyledListCardWrapper"
        )
        listings_data = []

        for item in listings:
            link = item.find("a").get("href")
            address = item.find("address").getText(strip=True)
            price_text = item.find("span").getText(strip=True)
            price = ''.join(c for c in price_text if c.isdigit())
            listing_data = {
                "link": link,
                "address": address,
                "price": price
            }

            # Append the dictionary to the list of listings data
            listings_data.append(listing_data)

        return listings_data
