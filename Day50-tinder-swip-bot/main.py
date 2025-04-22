from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv
import os
from time import sleep

load_dotenv()

LINK = "https://tinder.com/"
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

print("Email:", EMAIL)
print("Password:", PASSWORD)
# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

# Open link in Chrome
driver.get(LINK)
# Wait for page to load
sleep(2)

# Save the main window handle
main_window = driver.current_window_handle

# Login to Tinder
login = driver.find_element(By.LINK_TEXT, 'Log in')
login.click()
sleep(2)
login_facebook = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Log in with Facebook']")
login_facebook.click()

# Opens a new window for facebook login Wait for the second window to open
WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)

# Switch to the new window
for handle in driver.window_handles:
    if handle != main_window:
        driver.switch_to.window(handle)
        break

decline_cookies = driver.find_element(By.CSS_SELECTOR, "div[aria-label='Decline optional cookies']")
decline_cookies.click()

# Login to Facebook
email_input = driver.find_element(By.ID, "email")
email_input.send_keys(EMAIL)
psw_input = driver.find_element(By.ID, "pass")
psw_input.send_keys(PASSWORD)

login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
# login_button.click()

# Wait for page to load
sleep(2)

# Switch back to Tinder
driver.switch_to.window(main_window)

#Allow location
allow_location_button = driver.find_element(By.XPATH, value='//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
allow_location_button.click()

#Disallow notifications
notifications_button = driver.find_element(By.XPATH, value='//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]')
notifications_button.click()

#Allow cookies
cookies = driver.find_element(By.XPATH, value='//*[@id="content"]/div/div[2]/div/div/div[1]/button')
cookies.click()

# Locate Like button
for n in range(100):
    sleep(2)

    try:
        print("called")
        like_button = driver.find_element(By.XPATH, value=
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')
        like_button.click()
        # dislike_button = driver.find_element(By.CSS_SELECTOR,"button[id='dislike']")
        # dislike_button.click()

    # Catches the cases where there is a "Matched" pop-up in front of the "Like" button:
    except ElementClickInterceptedException:
    try:
        match_popup = driver.find_element(By.CSS_SELECTOR, value=".itsAMatch a")
        match_popup.click()

    # Catches the cases where the "Like" button has not yet loaded, so wait 2 seconds before retrying.
    except NoSuchElementException:
        sleep(2)

# Close and quit browser
driver.close()  # Close tab
driver.quit()  # Close browser
