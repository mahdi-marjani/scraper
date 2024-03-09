from dotenv import load_dotenv
import os

from selenium import webdriver
from selenium.webdriver.firefox.service import Service

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver, EventFiringWebElement
from selenium.webdriver.common.by import By

from time import sleep


class Instagram:
    def __init__(self) -> None:
        load_dotenv()
        self.USERNAME: str = os.environ['NAME']
        self.PASSWORD: str = os.environ['PASSWORD']

        self.service = Service(executable_path='./geckodriver.exe')
        self.options = webdriver.FirefoxOptions()
        self.driver = webdriver.Firefox(service=self.service, options=self.options)
        self.driver.maximize_window()

        self.insta_url: str = "https://www.instagram.com/"
        self.driver.get(self.insta_url)

    def website_title(self) -> str:
        title: str = self.driver.title

        return title
    
    def login_username(self) -> None:
        username_field = WebDriverWait(self.driver, 10).until(ec.presence_of_all_elements_located((By.NAME, 'username')))
        for field in username_field:
            try:
                field.send_keys(self.USERNAME)
            except:
                pass

    def login_password(self) -> None:
        password_field = WebDriverWait(self.driver, 10).until(ec.presence_of_all_elements_located((By.NAME, 'password')))
        for field in password_field:
            try:
                field.send_keys(self.PASSWORD)
            except:
                pass

    def press_login_button(self) -> None:
        xpath = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button'
        login_button = self.driver.find_element(By.XPATH, xpath)
        login_button.click()
    
    def press_save_info(self) -> None:
        xpath = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/section/div/button'
        save_info = self.driver.find_element(By.XPATH, xpath)
        save_info.click()
        
    def main(self) -> None:
        print(self.website_title())
        
        # logging in
        sleep(1)
        self.login_username()
        sleep(1)
        self.login_password()
        sleep(1)
        self.press_login_button()
        sleep(1.3)
        self.press_save_info()
        sleep(1.4)

insta = Instagram()
insta.main()


