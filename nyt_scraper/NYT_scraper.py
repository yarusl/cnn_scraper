from Article import Article
from constants import NYT_NEWS, SCROLL_PAUSE_TIME
from bs4 import BeautifulSoup as bs
from settings import DEMO
from db import DB
import time

class NYT_scraper:
    def __init__(self, driver, topic_url, articles_to_scrape=1):
        if articles_to_scrape <= 0:
            raise Exception(f"Variable 'articles_to_scrape' should be at least 1. You can't scrape less than one page")

        self.driver = driver
        self.topic_url = topic_url
        self.articles = []  # list of instances of class Article
        self.articles_to_scrape = articles_to_scrape
        self.validate_url(topic_url)

    def validate_url(self, topic_url):
        """ 
        validate if the URL is nyt + validate if the topic is scrapable:
        meaning that the page has a 
        'Latest Updates' section.
        """
        # validate URL is nyt news
        
        short_url = topic_url.lstrip('https://').lstrip('http://').lstrip('www.')
        if short_url[:len(NYT_NEWS)] != NYT_NEWS:
            raise Exception("Invalid website")
        
        # Check if there is a "UPDATE" section in the page
        self.driver.get('https://' + short_url)
        page = self.driver.page_source
        soup = bs(page, 'html.parser')
        if soup.find("section", {"id": "stream-panel"}) is None:
            raise Exception('No news updates category in the page')

    def scroll(self): 
        scroll_scrip = "document.querySelector('li.css-ye6x8s:last-child').scrollIntoView({ behavior: 'smooth' });"
        time.sleep(SCROLL_PAUSE_TIME)
        self.driver.execute_script(scroll_scrip)
        time.sleep(SCROLL_PAUSE_TIME)

    def scrape(self):
        """ 
        scrapes all the articles from 
        n-pages
        """
        
        self.driver.get(self.topic_url)
        while len(self.articles) < self.articles_to_scrape:
            self.articles = self.scrape_latest_updates()
            self.scroll()
        
        self.articles = self.articles[:self.articles_to_scrape]
        # for each article present in the news update section we scrape all available data
        for article in self.articles:
            article.scrape_article(self.driver)

        return self.articles

    def save(self):
        """Saves each one of the articles in the database"""
        for article in self.articles:
            DB(article).save(self.topic_url)
            

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
        soup = soup.find("section", {"id": "stream-panel"})
        elements = soup.find_all("li", {"class": "css-ye6x8s"})
        for el_soup in elements:
            # FILTER articles to be scrapped
            # We will only take articles which have a url (to scrap a full content only)
            # and that are on the news section of the website

            url = self.get_url(el_soup.a)
            text = self.get_text(el_soup.p)
            articles.append(Article(url, text))
            
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

    def print_info(self):
        print(self.__str__())

    def __del__(self):
        """ closes the browser """
        try:
            self.driver.quit()
        except Exception as e:
            print(f"the delete function did not work on its try due to : {e}")