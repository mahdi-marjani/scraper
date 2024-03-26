from twitter_user import TwitterUser

from time import sleep

class Twitter:
    def __init__(self, link) -> None:
        self.twitter_user = TwitterUser(link)   


    def main(self) -> None:
        print()
        print()

        sleep(3)

        try:
            self.twitter_user.press_login_button()
            sleep(3)
            self.twitter_user.login_username()

        except:
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

        sleep(5)

        links = self.twitter_user.get_tweets()

        sleep(1)

        print()
        print()

        all_info: dict[str, dict[tuple[str, str], list[tuple[str | None, list[str] | None, list[str] | None, str | None]]]] = dict() 

        link_counter: int = 1

        for link in links:
            info = self.twitter_user.get_info_per_link(link, link_counter)
            all_info[link] = info

            link_counter += 1

        print()
        print()
        print()
        print()
        print()
        print(f'SUMMARIZED INFORMATION FROM THE {self.twitter_user.number_of_tweets_from_user} TWEETS OF THE USER PAGE:')
        for url, data in all_info.items():
            print()
            print()
            print()
            print()
            url_string = f'URL: {url}'
            print('_' * len(url_string))
            print()
            print(url_string)
            for key, value in data.items():
                print()
                print(f'    {key}')

                for info in value:
                    print('        Tweet Text:')
                    print(f'        {info[0]}')
                    print()

                    print('        Tweet Photo Link:')
                    print(f'        {info[1]}')
                    print()

                    print('        Tweet Video Link:')
                    print(f'        {info[2]}')
                    print()

                    print('        Card Wrapper Link:')
                    print(f'        {info[3]}')
                    print()
                    print()

            print('_' * len(url_string))
        print()
        print()
        print()
        print()
        print()

        self.twitter_user.quit_browser()

print()
link = input("Enter the link of the user page you want to scrape: ")
twitter = Twitter(link)
twitter.main()
