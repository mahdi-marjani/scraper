import os

from selenium import webdriver
from selenium.webdriver.firefox.service import Service

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from time import sleep

import requests

import yt_dlp

from getpass import getpass

class TwitterUser:
    def __init__(self, link: str) -> None:
        print()
        print('_______________________________________________________________________________________________________')
        print()
        print("[NOTICE: This is for authentication process in the scraping machine. I can't get your info from this.]")
        print('_______________________________________________________________________________________________________')
        print()
        self.USERNAME: str = input("Enter your twitter username: ")
        self.PASSWORD: str = getpass("Enter your password: ")
        self.number_of_tweets_from_user: int = int(input("Enter number of tweets you want to scrape from this user page: "))
        self.number_of_replies_from_each_thread: int = int(input("Enter number of replies you want to scrape per tweet: "))

        self.service = Service(executable_path='./geckodriver.exe')
        self.options = webdriver.FirefoxOptions()
        self.driver = webdriver.Firefox(service=self.service, options=self.options)
        self.driver.maximize_window()

        self.twitter_url: str = link  
        self.driver.get(self.twitter_url)

        self.array = list()
        self.objects: dict[str, str] = {}

        self.image_download_index: int = 0
        self.video_download_index: int = 0

        self.visited_text_of_users: list[tuple[str, str, str]] = []
        self.visited_images_of_users: list[tuple[str, str, str]] = []
        self.visited_videos_of_users: list[tuple[str, str, str]] = []

        self.visited_cardwrapper_of_users: list[tuple[str, str, str]] = []

        self.repeated_loop: int = 0


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

    def get_tweets(self) -> list[str]:
        links = []
        wait = WebDriverWait(self.driver, 10)

        xpath = '//article[@data-testid="tweet"]'
        articles = self.driver.find_elements(By.XPATH, xpath)

        counter = 0

        while articles:
            for article in articles:
                hrefs = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid=User-Name] a[role=link][href*=status]')))
            
                for href in hrefs:
                    link = href.get_attribute('href')
                    if link not in links and len(links) < self.number_of_tweets_from_user + 1:
                        links.append(link)
                        counter += 1
                        print(f'Link {counter}:', link)

                    if len(links) == self.number_of_tweets_from_user:
                        break

                sleep(1)
                self.driver.execute_script('window.scrollBy(0, 200)', "")
                articles = self.driver.find_elements(By.XPATH, xpath)

                if len(links) == self.number_of_tweets_from_user:
                    break

            if len(links) == self.number_of_tweets_from_user:
                break

        return links

    # ---------------- Tweeter Thread ----------------
    
    def download_photo(self, image_link: str, name: str, username: str) -> None:
        folder_name = f'downloaded_images'

        folder_path = os.path.join(os.getcwd(), folder_name)

        image_name = f'{self.image_download_index}_{name}_{username}.jpg'

        image_path = os.path.join(folder_path, image_name)
        
        response = requests.get(image_link)

        with open(image_path, 'wb') as image_file:
            image_file.write(response.content)
        
    def download_video(self, video_link: str, name: str, username: str) -> None:
        folder_name = f'downloaded_videos'
        
        extra_opts = {
            'username': f'{self.USERNAME}',
            'password': f'{self.PASSWORD}',
        }

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f'{folder_name}/{self.video_download_index}_{name}_{username}.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }

        ydl_opts.update(extra_opts)

        ydl = yt_dlp.YoutubeDL(ydl_opts)
        
        ydl.download([video_link])

    def get_info_per_link(self, link: str, link_counter: int) -> dict[tuple[str, str], list[tuple[str | None, list[str] | None, str | None, str | None]]]:
        self.driver.get(link)
        wait = WebDriverWait(self.driver, 10)

        users: dict[tuple[str, str], list[tuple[str | None, list[str] | None, str | None, str | None]]] = dict()

        sleep(5)

        xpath = '//article[@data-testid="tweet"]'
        tweets = self.driver.find_elements(By.XPATH, xpath)
        
        number_of_replies = -1
        counter = 0
        name_counter = 0

        while True:
            for tweet in tweets:
                print()
                print('________________________')
                print()
                print('Counter: ', counter)
                print('Image Counter:', self.image_download_index)
                print('Number of Replies:', number_of_replies)
                print()
                print(f'Link: {link_counter}', link)
                print('________________________')
                print()
                print('Finding username.')

                name = f'name_placeholder{name_counter}'

                if counter == 0:
                    try:
                        number_of_replies = int(tweet.find_element(By.CSS_SELECTOR, "[data-testid='reply'] span[style='text-overflow: unset;']").text)
                    except:
                        number_of_replies = 0

                try:
                    name = tweet.find_element(By.CSS_SELECTOR, "[data-testid='User-Name'] div[class='css-1rynq56 r-bcqeeo r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-b88u0q r-1awozwy r-6koalj r-1udh08x r-3s2u2q'][style='text-overflow: unset; color: rgb(231, 233, 234);'] span[class='css-1qaijid r-bcqeeo r-qvutc0 r-poiln3']").text
                    username = tweet.find_element(By.CSS_SELECTOR, "[data-testid='User-Name'] div[class='css-1rynq56 r-dnmrzs r-1udh08x r-3s2u2q r-bcqeeo r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-18u37iz r-1wvb978'][style='text-overflow: unset; color: rgb(113, 118, 123);'] span[class='css-1qaijid r-bcqeeo r-qvutc0 r-poiln3']").text
                except:
                    emoji_name = tweet.find_element(By.CSS_SELECTOR, "[data-testid='User-Name'] div[class='css-1rynq56 r-bcqeeo r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-b88u0q r-1awozwy r-6koalj r-1udh08x r-3s2u2q'][style='text-overflow: unset; color: rgb(231, 233, 234);'] span[class='css-1qaijid r-dnmrzs r-1udh08x r-3s2u2q r-bcqeeo r-qvutc0 r-poiln3'] img[class='r-4qtqp9 r-dflpy8 r-zw8f10 r-sjv1od r-10akycc r-h9hxbl']")
                    name = emoji_name.get_attribute('src')

                    if name is None:
                        name = f'name_placeholder{name_counter}'
                        name_counter += 1
                        
                    username = tweet.find_element(By.CSS_SELECTOR, "[data-testid='User-Name'] div[class='css-1rynq56 r-dnmrzs r-1udh08x r-3s2u2q r-bcqeeo r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-18u37iz r-1wvb978'][style='text-overflow: unset; color: rgb(113, 118, 123);'] span[class='css-1qaijid r-bcqeeo r-qvutc0 r-poiln3']").text
                
                print(name, username)

                sleep(1)

                tweetText = None
                tweetPhotoList = []
                tweetVideo = None
                tweetCardWrapper = None

                try:
                    print()
                    print('Finding text.')
                    tweetText = tweet.find_element(By.CSS_SELECTOR, "[data-testid='tweetText'] span[style='text-overflow: unset;']").text
                    print(f'Text found: \n{tweetText}')
                    sleep(1)
                        
                except:
                    tweetText = None
                    print('No text found.')



                try:
                    print()
                    print('Finding tweet photo.')
                    tweetPhotoPath = tweet.find_elements(By.CSS_SELECTOR, "[data-testid='tweetPhoto'] img[alt='Image'][draggable='true']")

                    for tweetPhoto in tweetPhotoPath:
                        photo = tweetPhoto.get_attribute('src')

                        if photo:
                            tweetPhotoList.append(photo)

                    if tweetPhotoList:
                        print(f'Tweet photo found: {tweetPhotoList}')  
                    else:
                        raise Exception

                    try:
                        if counter > 0:
                            tweetLinkPath = tweet.find_element(By.CSS_SELECTOR, "[data-testid=User-Name] a[role=link][href*=status]")
                            tweetLink = tweetLinkPath.get_attribute('href')
                            print(f'Tweet link found: {tweetLink}')
                        else:
                            tweetLink = link

                    except:
                        tweetLink = link

                    if tweetPhotoList is not None and tweetLink and (username, name, tweetLink) not in self.visited_images_of_users:
                        for photo in tweetPhotoList:
                            self.download_photo(photo, name, username)
                        
                        self.image_download_index += 1
                        self.visited_images_of_users.append((username, name, tweetLink))

                    sleep(1)
                except:
                    tweetPhotoList = None
                    print('No photo found.')





                try:
                    print()
                    print('Finding tweet video.')
                    tweetVideoPath = tweet.find_element(By.CSS_SELECTOR, "[data-testid='videoComponent'] source[type='video/mp4']")
                    tweetVideo = tweetVideoPath.get_attribute('src')
                    print(f'Tweet video found: {tweetVideo}')

                    try:
                        if counter > 0 :
                            tweetLinkPath = tweet.find_element(By.CSS_SELECTOR, "[data-testid=User-Name] a[role=link][href*=status]")
                            tweetLink = tweetLinkPath.get_attribute('href')
                            print(f'Tweet link found: {tweetLink}')
                        else:
                            tweetLink = link
                            
                    except:
                        tweetLink = link

                    
                    if tweetLink is not None and (username, name, tweetLink) not in self.visited_videos_of_users:
                        self.download_video(tweetLink, name, username)
                        self.video_download_index += 1
                        self.visited_videos_of_users.append((username, name, tweetLink))

                    sleep(1)
                except:
                    tweetVideo = None
                    print('No video found.')



                try:
                    print()
                    print('Finding other than text, image, and video.')
                    tweetCardWrapperPath = tweet.find_element(By.CSS_SELECTOR, "[data-testid='card.wrapper'] a[target='_blank']")
                    tweetCardWrapper = tweetCardWrapperPath.get_attribute('href')
                    print(f'Card wrapper image found: {tweetCardWrapper}')

                    try:
                        if counter > 0:
                            tweetLinkPath = tweet.find_element(By.CSS_SELECTOR, "[data-testid=User-Name] a[role=link][href*=status]")
                            tweetLink = tweetLinkPath.get_attribute('href')
                            print(f'Tweet link found: {tweetLink}')
                        else:
                            tweetLink = link


                    except:
                        tweetLink = link



                    if tweetLink is not None and (username, name, tweetLink) not in self.visited_cardwrapper_of_users:
                        self.visited_cardwrapper_of_users.append((username, name, tweetLink))
                except:
                    tweetCardWrapper = None
                    print('No card wrapper found.')





                if ((name, username)) in users.keys() and (tweetText, tweetPhotoList, tweetVideo, tweetCardWrapper) not in users[(name, username)]:
                    users[(name, username)].append((tweetText, tweetPhotoList, tweetVideo, tweetCardWrapper))
                    print()
                    print()

                    counter += 1

                elif (name, username) not in users.keys():
                    users[(name, username)] = [(tweetText, tweetPhotoList, tweetVideo, tweetCardWrapper)]
                    print()
                    print()

                    counter += 1


                sleep(1)
                self.driver.execute_script('window.scrollBy(0, 200)', "")
                tweets = self.driver.find_elements(By.XPATH, xpath)

                if self.number_of_replies_from_each_thread == counter:
                    break

                elif number_of_replies == counter - 1:
                    break

            if self.number_of_replies_from_each_thread == counter:
                break
                
            elif number_of_replies == counter - 1:
                break

            
        print('____________________________')
        print()
        print('End of tweet thread.')
        print(users)
        print('____________________________')
        print()
        print()
        print()

        sleep(1)

        return users
    
    def quit_browser(self) -> None:
        self.driver.close()
