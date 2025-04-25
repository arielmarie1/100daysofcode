from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from time import sleep


class FilterSearchOptions:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("https://www.nepremicnine.net/")
        try:
            cookies = self.driver.find_element(By.ID, "CybotCookiebotDialogBodyButtonDecline")
            cookies.click()
        except NoSuchElementException:
            pass

    def posredovanje(self):
        print("Please choose an option: ")
        type = self.driver.find_element(By.ID, "NOp")
        options = type.find_elements(By.CSS_SELECTOR, "select option")
        for index, option in enumerate(options, start=1):
            print(f" {index}. {option.text}")
        user_choice_type = input("Enter the number corresponding to your choice: ")
        pick = type.find_element(By.CSS_SELECTOR, f"option[value='{user_choice_type}']")
        pick.click()

    def nepremicnina(self):
        print("Please choose an option: ")
        type = self.driver.find_element(By.ID, "NOn")
        options = type.find_elements(By.CSS_SELECTOR, "select option")
        for index, option in enumerate(options, start=1):
            print(f" {index}. {option.text}")
        user_choice_type = input("Enter the number corresponding to your choice: ")
        pick = type.find_element(By.CSS_SELECTOR, f"option[value='{user_choice_type}']")
        pick.click()

    def regija(self):
        print("Please choose an option: ")
        type = self.driver.find_element(By.ID, "NOr")
        options = type.find_elements(By.CSS_SELECTOR, "select option")
        for index, option in enumerate(options, start=1):
            print(f" {index}. {option.text}")
        user_choice_type = input("Enter the number corresponding to your choice: ")
        pick = type.find_element(By.CSS_SELECTOR, f"option[value='{user_choice_type}']")
        pick.click()

    def cena_od(self):
        user_choice_type = input("Starting price in EUR: ")
        cena = self.driver.find_element(By.ID, "NOc1")
        cena.click()
        cena.send_keys(user_choice_type)

    def cena_do(self):
        user_choice_type = input("Maximum price in EUR: ")
        cena = self.driver.find_element(By.ID, "NOc2")
        cena.click()
        cena.send_keys(user_choice_type)

    def submit(self):
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "a[class*='gumb potrdi']")
        submit_button.click()

    def close_browser(self):
        # Close and quit browser
        self.driver.close()  # Close tab
        self.driver.quit()  # Close browser


test = FilterSearchOptions()
test.posredovanje()
test.nepremicnina()
test.regija()
test.cena_od()
test.cena_do()
test.submit()
# test.close_browser()

# Unfortunately when hitting submit automatically it block me. Will try without this method but just going straight to the website.

