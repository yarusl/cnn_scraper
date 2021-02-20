from Article import Article
from constants import BBC_NEWS

class CnnScraper:
    def __init__(self, driver, topic_url, pages_to_scrape = 1):
        if pages_to_scrape <= 0:
            raise Exception(f"Variable 'pages_to_scrape' should be at least 1. You can't scrape less than one page")

        self.driver = driver
        self.topic_url = topic_url
        self.articles = [] # list of instances of class Article
        self.pages_to_scrape = pages_to_scrape
        self.validate_url(topic_url)

    def validate_url(self, topic_url):
        """ 
        validate if the URL is bbc + validate if the topic is scrapable:
        meaning that the page has a 
        'Latest Updates' section.
        """


        #if not topic_url[:len(BBC_NEWS)] == BBC_NEWS or bbc.com/news:
        #    raise Exception ("Invalid website")

        # if i


        #TODO MICHAEL -- look for latest-updates

        pass

    def scrape(self):
        """ 
        scrapes all the articles from 
        n-pages
        """
        next_page = '// *[ @ id = "lx-stream"] / div[2] / div / div[3] / a[1]'

        #driver.page_source.encode("utf-8") -- reminder
        page = self.driver.get(self.topic_url)
        for p in range(1, self.pages_to_scrape + 1):
            self.articles += self.scrape_latest_updates()
            if p != self.pages_to_scrape:
                print("Going to the next page")
                self.driver.find_element_by_xpath(next_page).click()

        return self.articles

    def scrape_latest_updates(self):
        """ 
        scrapes all articles from 
        the 'Latest Updates' section
        """
        articles = []
        return articles

    def __str__(self):
        """ 
        returns a readable representation 
        of the result of the scrape 
        """
        pass

    def __del__(self):
        """ closes the browser """
        #self.driver.quit()
        pass