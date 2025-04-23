from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
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

    def follow(self):
        # Find list of all followers (by username as an example without actually following people)
        # follower username <span class="_ap3a _aaco _aacw _aacx _aad7 _aade" dir="auto">exampleusername</span>
        try:
            WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, "span[class*='_ap3a _aaco _aacw _aacx _aad7 _aade']")))
            account_followers = self.driver.find_elements(By.CSS_SELECTOR,
                                                          "span[class*='_ap3a _aaco _aacw _aacx _aad7 _aade']")
            for account in account_followers[:10]:
                # print list of usernames to follow (as test that code is working)
                print(account.text)
        except TimeoutException:
            print("Account followers not loading.")

        # Actually Follow accounts
        # follow button <div class="_ap3a _aaco _aacw _aad6 _aade" dir="auto">Follow</div>
        try:
            WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, "div[class*='_ap3a _aaco _aacw _aad6 _aade']")))
            follow_button = self.driver.find_elements(By.CSS_SELECTOR,
                                                      "div[class*='_ap3a _aaco _aacw _aad6 _aade']")
            for follow in follow_button[:10]:
                print(follow.text)
                # follow_button.click()
        except TimeoutException:
            print("Account followers not loading.")

        # TODO: scroll down on followers page to access more followers (max 15)
        # TODO: follow bot with delay between follows and maximum number of follows
        # TODO: handle exceptions for when you have already followed someone and a popup appears to unfollow that user

    def close_browser(self):
        # Close and quit browser
        self.driver.close()  # Close tab
        self.driver.quit()  # Close browser


bot = InstaFollower()
bot.insta_login()
bot.find_followers()
bot.follow()
bot.close_browser()
