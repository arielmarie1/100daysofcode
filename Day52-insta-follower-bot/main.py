from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from time import sleep
import random as rd
from dotenv import load_dotenv
import os

load_dotenv()

LINK = "https://www.instagram.com/"
SIMILAR_ACCOUNT = os.getenv("SIMILAR_ACCOUNT")
EMAIL = os.getenv("INSTA_LOGIN")
PASSWORD = os.getenv("INSTA_PASSWORD")
user_data_dir = os.getenv("USERDATA_DIR")


class InstaFollower:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument(f"user-data-dir={user_data_dir}")  # Reuse the same profile
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=chrome_options)

    def insta_login(self):
        self.driver.get(LINK)

        # Close cookies pop up
        try:
            close_cookies = self.driver.find_element(By.CSS_SELECTOR, "button[class*='_a9-- _ap36 _a9_1']")
            close_cookies.click()
        except NoSuchElementException:
            print("No cookies popup!")

        # Log in to instagram
        try:
            login_email = self.driver.find_element(By.CSS_SELECTOR, "input[name='username']")
            login_email.send_keys(EMAIL)
            login_password = self.driver.find_element(By.CSS_SELECTOR, "input[name='password']")
            login_password.send_keys(PASSWORD)
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
        except NoSuchElementException:
            print("Already logged in!")

    def find_followers(self):
        # Search for similar account
        try:
            search_icon = self.driver.find_element(By.CSS_SELECTOR, "svg[aria-label='Search']")
            search_icon.click()
            search_text = self.driver.find_element(By.CSS_SELECTOR, "input[aria-label='Search input']")
            search_text.send_keys(SIMILAR_ACCOUNT)
        except NoSuchElementException:
            print("Different page layout")

        # Go to similar account page
        try:
            navigate_to_account = WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, f'a[href="/{SIMILAR_ACCOUNT}/"]')))
            navigate_to_account.click()
        except TimeoutException:
            print("No account found.")

        # Click on account followers
        try:
            account_followers = WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, f'a[href="/{SIMILAR_ACCOUNT}/followers/"]')))
            account_followers.click()
        except TimeoutException:
            print("No account followers found.")

    def follow(self, max_follows=100, follow=False):
        last_count = 0
        attempts = 0
        follows = 0
        fake_follows = 0

        try:
            WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, "span[class*='_ap3a _aaco _aacw _aacx _aad7 _aade']")))
            print("Followers loaded...")
            scroll_box = self.driver.find_element(By.XPATH, ".//div[contains(@class, 'xyi19xy')]")
            # long xpath: "/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]"
        except TimeoutException:
            print("Followers page took too long to load")
            return

        while True:
            # Collect current follower links
            try:
                followers = self.driver.find_elements(By.CSS_SELECTOR,
                                                      "span[class*='_ap3a _aaco _aacw _aacx _aad7 _aade']")
                follow_buttons = self.driver.find_elements(By.CSS_SELECTOR,
                                                           "div[class*='_ap3a _aaco _aacw _aad6 _aade']")
                print(f"Found {len(followers)} accounts")
                remaining = max_follows - last_count
                for user, button in zip(followers[last_count:last_count + remaining],
                                        follow_buttons[last_count:last_count + remaining]):
                    if follow:
                        try:
                            button.click()
                            sleep(rd.uniform(1, 5))  # Wait arbitrary amount of time

                            # In order to not get blocked on Instagram this part of the code was not tested.
                            try:
                                # Check if popup shows up (means already following)
                                WebDriverWait(self.driver, 10).until(
                                    ec.element_to_be_clickable((By.XPATH, "//button[text()='Cancel']")))
                                cancel_button = self.driver.find_element(By.XPATH, "//button[text()='Cancel']")
                                cancel_button.click()
                                print(f"Skipped {user.text} (already followed)")
                            except NoSuchElementException:
                                # No popup window means not following user yet. Add to "follows" count.
                                print(f"Followed {user.text}")
                                follows += 1
                        except Exception as e:
                            print(f"Error following {user.text}: {e}")
                    else:
                        # print(f"Fake followed {user.text}")
                        fake_follows += 1

                # Break if the desired number is reached
                if len(followers) >= max_follows:
                    break

                # Scroll down
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
                sleep(2)

                # Check if new accounts loaded
                if len(followers) == last_count:
                    attempts += 1
                    if attempts >= 3:
                        print("No more new accounts loading. Stopping.")
                        break
                else:
                    attempts = 0  # reset if new ones appeared
                    last_count = len(followers)

            except TimeoutException:
                print("Account followers not loading.")

        print(f"Followed: {follows} accounts. Fake followed: {fake_follows} accounts")

    def close_browser(self):
        # Close and quit browser
        self.driver.close()  # Close tab
        self.driver.quit()  # Close browser


bot = InstaFollower()
bot.insta_login()
bot.find_followers()
bot.follow()
bot.close_browser()
