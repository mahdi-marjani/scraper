from twitter_user import TwitterUser

from time import sleep

class Twitter:
    def __init__(self, link) -> None:
        self.twitter_user = TwitterUser(link)   
        self.number_of_tweets_from_user: int = int(input("Enter number of tweets you want to scrape from this user page: "))
        self.number_of_replies_from_each_thread: int = int(input("Enter number of replies you want to scrape per tweet: "))

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

        all_info: dict[str, dict[tuple[str, str], tuple[str | None, str | None, str | None]]] = dict() 

        link_counter: int = 1

        for link in links:
            info = self.twitter_user.get_info_per_link(link, self.number_of_replies_from_each_thread, link_counter)
            all_info[link] = info

            link_counter += 1

        print()
        print()
        print('-------------------------------------------------------------------------------')
        for url, data in all_info.items():
            print(f'URL: {url}')
            for key, value in data.items():
                print(f'\t{key}: {value}')
        print('-------------------------------------------------------------------------------')
        print()
        print()

print()
link = input("Enter the link of the user page you want to scrape: ")
twitter = Twitter(link)
twitter.main()
