from twitter_user import TwitterUser

from time import sleep

class Twitter:
    def __init__(self, link: str, number_of_tweets_from_user: int, number_of_replies_from_each_thread: int) -> None:
        self.twitter_user = TwitterUser(link)    
        self.number_of_tweets_from_user = number_of_tweets_from_user
        self.number_of_replies_from_each_thread = number_of_replies_from_each_thread

    def main(self) -> None:
        print()
        print()

        sleep(3)

        self.twitter_user.press_login_button()
        
        sleep(3)

        self.twitter_user.login_username()

        sleep(1)

        self.twitter_user.press_next()

        sleep(1)

        self.twitter_user.login_password()

        sleep(1)

        self.twitter_user.press_big_login_button()

        sleep(5)

        self.twitter_user.get_handle_name()
        
        print()
        print()

        sleep(3)

        links = self.twitter_user.get_tweets(self.number_of_tweets_from_user)

        sleep(1)

        print()
        print()

        print(links)

        all_info = []

        for link in links:
            info = self.twitter_user.get_info_per_link(link, self.number_of_replies_from_each_thread)
            all_info.append(info)

        print()
        print()

        print(self.twitter_user.objects)

link = "https://twitter.com/cravedcuddle"
number_of_tweets_from_user = 5
number_of_replies_from_each_thread = 5
twitter = Twitter(link, number_of_tweets_from_user, number_of_replies_from_each_thread)
twitter.main()
