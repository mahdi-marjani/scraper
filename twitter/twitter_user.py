from dotenv import load_dotenv
import os

from selenium import webdriver
from selenium.webdriver.firefox.service import Service

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver, EventFiringWebElement
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

from time import sleep

class TwitterUser:
    def __init__(self, link: str) -> None:
        load_dotenv()
        self.USERNAME: str = os.environ['NAME']
        self.PASSWORD: str = os.environ['PASSWORD']

        self.service = Service(executable_path='./geckodriver.exe')
        self.options = webdriver.FirefoxOptions()
        self.driver = webdriver.Firefox(service=self.service, options=self.options)
        self.driver.maximize_window()

        self.insta_url: str = link
        self.driver.get(self.insta_url)

        self.array = list()
        self.objects = {}

    # ---------------- Twitter User Info ----------------

    def press_login_button(self) -> None:
        xpath = "//span[contains(text(), 'Log in')]"
        login_button = self.driver.find_element(By.XPATH, xpath)
        login_button.click()

    def login_username(self) -> None:
        xpath = "//input[@name='text']"
        username = self.driver.find_element(By.XPATH, xpath)
        username.send_keys(self.USERNAME)

    def press_next(self) -> None:
        xpath = "//span[contains(text(), 'Next')]"
        next_button = self.driver.find_element(By.XPATH, xpath)
        next_button.click()

    def login_password(self) -> None:
        xpath = "//input[@name='password']"
        password = self.driver.find_element(By.XPATH, xpath)
        password.send_keys(self.PASSWORD)

    def press_big_login_button(self) -> None:
        xpath = "//div[@data-testid='LoginForm_Login_Button']"
        big_login_button = self.driver.find_element(By.XPATH, xpath)
        big_login_button.click()

    def get_handle_name(self) -> None:
        xpath = "//div[@data-testid='UserName']"
        user_tag = self.driver.find_element(By.XPATH, xpath).text
        
        index = user_tag.find('@')
        name = user_tag[:index-2] 
        username = user_tag[index:]

        self.objects['name'] = name
        self.objects['username'] = username

        print("Name:", name)
        print("Username:", username)

    def get_description(self) -> None:
        xpath = "//div[@data-testid='UserDescription']"
        description = self.driver.find_element(By.XPATH, xpath).text
        self.objects['description'] = description
        
        print("Description:", description)

    def get_tweets(self, number_of_tweets: int) -> list[str]:
        links = []
        wait = WebDriverWait(self.driver, 10)

        xpath = '//article[@data-testid="tweet"]'
        articles = self.driver.find_elements(By.XPATH, xpath)

        counter = 0

        while True:
            for article in articles:
                hrefs = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid=User-Name] a[role=link][href*=status]')))
            
                for href in hrefs:
                    link = href.get_attribute('href')
                    if link not in links and len(links) < number_of_tweets + 1:
                        links.append(link)
                        counter += 1
                        print(f'Link {counter}:', link)

                sleep(1)
                self.driver.execute_script('window.scrollBy(0, 200)', "")
                articles = self.driver.find_elements(By.XPATH, xpath)

            if len(links) == number_of_tweets:
                break

        return links

    # ---------------- Tweeter Thread ----------------

    def get_username(self) -> tuple[str, str]:
        xpath = "//div[@data-testid='User-Name']"
        user_tag = self.driver.find_element(By.XPATH, xpath).text
        
        index = user_tag.find('@')
        name = user_tag[:index-2] 
        username = user_tag[index:]

        print(name)
        print(username)

        return name, username
    
    def get_photo(self) -> str | None:
        xpath = "//div[@data-testid='tweetPhoto']"
        photo = self.driver.find_element(By.XPATH, xpath).text

        print(photo)

        return photo if photo else None

    def get_info_per_link(self, link: str, number_of_replies_from_each_thread: int) -> dict:
        self.driver.get(link)
        wait = WebDriverWait(self.driver, 10)

        users = dict()

        sleep(5)

        xpath = '//article[@data-testid="tweet"]'
        articles = self.driver.find_elements(By.XPATH, xpath)
        
        counter = 0

        while True:
            for article in articles:
                name, username = self.get_username()
                photo = self.get_photo()
                sleep(1.2)

                if (name, username) not in users.keys():
                    users[(name, username)] = photo
    
                    counter += 1

                sleep(1)
                self.driver.execute_script('window.scrollBy(0, 400)', "")
                articles = self.driver.find_elements(By.XPATH, xpath)

                if number_of_replies_from_each_thread == counter:
                    break

            if number_of_replies_from_each_thread == counter:
                break
            

        print(users)
        sleep(1)

        return users

                

    
# data-testid="tweetText"
# data-testid="tweetPhoto"
# //div[@data-testid='User-Name']