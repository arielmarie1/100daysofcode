from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


# Entering data into google forms using selenium
class GoogleFormBot:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=chrome_options)

    def fill_form(self, google_form, real_estate_listings, num_listing=99999):
        self.driver.get(google_form)
        keys = ["address", "price", "link"]
        for listing in real_estate_listings[:num_listing]:
            form_text_input = self.driver.find_elements(By.CSS_SELECTOR, "input[class*='whsOnd zHQkBf']")
            for item, key in zip(form_text_input, keys):
                item.click()
                item.send_keys(listing[key])
            submit = self.driver.find_element(By.CSS_SELECTOR, "div[role='button']")
            submit.click()
            sleep(2)
            resubmit = self.driver.find_element(By.CSS_SELECTOR, "a")
            resubmit.click()
            sleep(2)

    def close_browser(self):
        # Close and quit browser
        self.driver.close()  # Close tab
        self.driver.quit()  # Close browser
