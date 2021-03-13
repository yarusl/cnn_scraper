from Article import Article
from constants import BBC_NEWS
from bs4 import BeautifulSoup as bs


class BBCScraper:
    def __init__(self, driver, topic_url, pages_to_scrape=1):
        if pages_to_scrape <= 0:
            raise Exception(f"Variable 'pages_to_scrape' should be at least 1. You can't scrape less than one page")

        self.driver = driver
        self.topic_url = topic_url
        self.articles = []  # list of instances of class Article
        self.pages_to_scrape = pages_to_scrape
        self.validate_url(topic_url)

    def validate_url(self, topic_url):
        """ 
        validate if the URL is bbc + validate if the topic is scrapable:
        meaning that the page has a 
        'Latest Updates' section.
        """
        # validate URL is bbc news

        short_url = topic_url.lstrip('https://').lstrip('www.').rstrip('/')

        if short_url[:len(BBC_NEWS)] != BBC_NEWS or 'https://' != topic_url[:8]:
            raise Exception("Invalid website")

        # Check if there is a "UPDATE" section in the page
        self.driver.get(topic_url)
        page = self.driver.page_source
        soup = bs(page, 'html.parser')
        if soup.find("h2", {"id": "latest-updates"}) is None:
            raise Exception('No news updates category in the page')

    def scrape(self):
        """ 
        scrapes all the articles from 
        n-pages
        """
        next_page = 'qa-pagination-next-page'

        self.driver.get(self.topic_url)
        for p in range(1, self.pages_to_scrape + 1):
            self.articles += self.scrape_latest_updates()
            if p != self.pages_to_scrape:
                print("Going to the next page")
                self.driver.find_elements_by_class_name(next_page)[0].click()

        # for each article present in the news update section we scrape all available data
        for article in self.articles:
            article.scrape_art(self.driver)

        return self.articles

    def save(self):
        """Saves each one of the articles in the database"""
        for article in self.articles:
            article.save(self.topic_url)

    def get_text(self, el_soup):
        if el_soup is None:
            return None
        return el_soup.text

    def get_url(self, el_soup):
        if el_soup is None:
            return None

        return el_soup["href"]

    def get_src(self, el_soup):
        if el_soup is None:
            return None
        return el_soup["src"]

    def get_date(self, el_soup):
        if el_soup is None:
            return None
        return el_soup.text

    def scrape_latest_updates(self):
        """
        scrapes all articles from
        the 'Latest Updates' section
        """
        articles = []

        soup = bs(self.driver.page_source, 'html.parser')
        soup = soup.find("h2", {"id": "latest-updates"}).find_parent('div')
        elements = soup.find_all("li", {"class": "lx-stream__post-container"})
        for el_soup in elements:
            url = self.get_url(el_soup.find("a", {"class": "qa-story-cta-link"}))
            if url is None or url[0:6] != '/news/':
                continue
            title = self.get_text(el_soup.find("h3", {"class": "lx-stream-post__header-title"}))
            text = self.get_text(el_soup.find("p", {"class": "lx-stream-related-story--summary"}))
            date = self.get_date(el_soup.find("span", {"class": "qa-visually-hidden-meta"}))
            img = self.get_src(el_soup.find("img", {"class": "lx-stream-related-story--index-image"}))

            # FILTER articles to be scrapped
            # We will only take articles which have a url (to scrap a full content only)
            # and that are on the news section of the website
            articles.append(Article(title, text, date, url, img))

        return articles

    def __str__(self):
        """ 
        returns a readable representation 
        of the result of the scrape 
        """
        res = ""
        for article in self.articles:
            res += str(article) + '\n'
        res += f"Articles scraped: {len(self.articles)}"
        return res

    def __del__(self):
        """ closes the browser """
        try:
            self.driver.quit()
        except Exception as e:
            print(f"the delete function did not work on its try due to : {e}")
