# from selenium import webdriver
# from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

PROMISED_DOWN = 150
PROMISED_UP = 10
SPEEDTEST_LINK = "https://www.speedtest.net/"


class InternetSpeedCheck:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.up = 0
        self.down = 0

    def get_internet_speed(self):
        self.driver.get(SPEEDTEST_LINK)
    # Reject cookies
        try:
            reject_button = WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable((By.ID, "onetrust-reject-all-handler")))
            reject_button.click()
        except TimeoutException:
            print("No reject cookies button found.")

    # Start Speedtest by clicking GO
        try:
            go_button = WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, "a span.start-text")))
            go_button.click()
        except TimeoutException:
            print("Go button not found.")
            return
        print("Running Speed test... please wait")

        # Wait for the download speed result to appear (max 60 seconds)
        try:
            WebDriverWait(self.driver, 60).until(
                lambda driver: (
                    (text := self.driver.find_element(By.CSS_SELECTOR, "span[class*='download-speed']").text)
                    and text not in ["", "0", "—"]))
            download_speed = self.driver.find_element(By.CSS_SELECTOR, "span[class*='download-speed']")
            self.down = float(download_speed.text)
            print(f"Download Speed: {self.down} Mbps")
        except TimeoutException:
            print("Download speed did not appear in time.")

    # Wait for the upload speed result to appear (max 60 seconds)
        try:
            WebDriverWait(self.driver, 60).until(
                lambda driver: (
                    (text := self.driver.find_element(By.CSS_SELECTOR, "span[class*='upload-speed']").text)
                    and text not in ["", "0", "—"]))
            upload_speed = self.driver.find_element(By.CSS_SELECTOR, "span[class*='upload-speed']")
            self.up = float(upload_speed.text)
            print(f"Upload Speed: {self.up} Mbps")
        except TimeoutException:
            print("Upload speed did not appear in time.")

    def twitter_complaint(self):
        print("Tweeting at provider...")


bot = InternetSpeedCheck()
bot.get_internet_speed()
bot.twitter_complaint()

bot.driver.close()  # Close tab
bot.driver.quit()  # Close browser
