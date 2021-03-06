import pymysql
from constants import NYT_PROTOCOL
from bs4 import BeautifulSoup as bs
from logger import logger
from constants import SCROLL_TO_BOTTOM, SCROLL_PAUSE_TIME
from settings import nyt
import time

class Article:
    def __init__(self, url, short_text=None):
        """ We initialise the attributes of an article:
        title: title of the article.
        date: date on which the article was posted.
        url: url of the article.
        img: Image in the article when there is one.
        author: Author of the article.
        author_pos: Job Title of the author.
        short_text: short summary of the article (1 to 2 lines in general). Scraped from the "News update" section at the bottom of the page.
        text: Full text of the article.
        rel_topics: flags that say to which topics an article is related. e.g. "Tesla acquires a company". Topics will be "Electric Cars", "Elon Musk", "M and A"
        links: other articles linked to this article.
        """
        self.short_url = url
        self.short_text = short_text
        self.url = NYT_PROTOCOL + self.short_url
        self.authors = []
        self.img = None
        self.title = None
        self.text = None
        self.links = None
        self.scraped_API = (None, None, None, None, None)

    def scrape_date(self):
        """
        scrapes the date
        """
        date = self.soup.find('div', {"class": 'css-1lvorsa'})
        if date is None:
            return None
        return date.span.text
   
    def scrape_title(self): 
        """
        scrapes the title
        """
        h1 = self.soup.find('h1')
        return h1.text

    def scrape_img(self):
        """
        scrapes the main image
        """
        logger.debug('Running scrape_img')
        images = self.soup.findAll("img", {"class": "css-11cwn6f"})
        if not len(images):
            return None
        return images[0]["src"]

    def scrape_text(self):
        """
        scrapes the text of the article
        """
        logger.debug('Running scrape_text')
        # We save the entire article text
        return self.soup.find("article", {"id": "story"}).text

    def scrape_authors(self):
        """
        scrapes the author
        """
        # We save the author
        logger.debug('Running scrape_author')
        parent = self.soup.find("p", {"class": "e1jsehar1"})
        if parent is None:
            return []
        
        ret = []
        authors = parent.findAll('a')
        for author in authors:
            ret.append(author.text)
        
        return ret

    def scrape_links(self):

        """
        scrapes links to other related articles
        """
        # We save the related articles
        ret_links = {}
        parent = self.soup.find("div", {"class": "css-1y4vkv1"})
        if parent == None:
            return {}
        
        links = parent.findAll("section", {"class": "css-1xgtmq5"}) 
        for link in links:
            text = link.find("p", {"class": "css-1ad9klu"}).text
            url = link.find("a", {"class": "css-1e1a8wb"})["href"]
            ret_links[text] = url

        return ret_links

    # Use of the API to scrape additional meta information
    def scrape_API(self):
        meta = nyt.article_metadata(url=self.short_url)[0]
        label_dict = {}
        section = meta['section']
        subsection = meta['subsection']
        abstract = meta['abstract']
        label_dict['des'] = meta['des_facet']
        label_dict['org'] = meta['org_facet']
        label_dict['per'] = meta['per_facet']
        label_dict['geo'] = meta['geo_facet']
        
        return self.short_url, section, subsection, abstract, label_dict

    def scroll(self, driver):
        while True:
            try:
                driver.find_element_by_class_name("css-18n4040")
                return
            except:
                pass
            time.sleep(SCROLL_PAUSE_TIME)
            driver.execute_script(SCROLL_TO_BOTTOM)

    # Scrape article uses all the previous class methods to scrap the maximum information on a given article
    def scrape_article(self, driver):
        """For each article that was scraped from news update, we scrape as much information as possible"""
        self.scraped_API = self.scrape_API()

        print(self.url)
        driver.get(self.url)
        self.scroll(driver)
        page = driver.page_source
        self.soup = bs(page, 'html.parser')

        self.date = self.scrape_date()
        self.title = self.scrape_title()
        self.authors = self.scrape_authors()
        self.img = self.scrape_img()
        self.text = self.scrape_text()
        self.links = self.scrape_links()
        
    # Below we define the get methods to access the article's attributes
    def get_url(self):
        return self.url

    def get_short_text(self):
        return self.short_text

    def get_date(self):
        return self.date

    def get_title(self):
        return self.title

    def get_img(self):
        return self.img

    def get_text(self):
        return self.text

    def get_author(self):
        return self.authors
    
    def get_links(self):
        return self.links
    
    def __str__(self):
        return f"""
-------------------------------------------------------------------------
{self.title}
Written by: {self.authors}

{self.text}

Posted date: {self.date}
Link of the article: {self.url}
Link to image: {self.img}
List of related articles and their links {self.links}

A summary to the article: {self.short_text}
-------------------------------------------------------------------------

"""


if __name__ == '__main__':
    from settings import mode, articles_to_scrape, topic_url
    from settings import driver_path, DEMO, DEMO_TOPIC, DEMO_ARTICLE_SCRAP
    from main import create_driver
    from db import DB
    
    url = "/2019/10/20/world/middleeast/erdogan-turkey-nuclear-weapons-trump.html"
    driver = create_driver(mode, driver_path)
    article = Article(url)
    article.scrape_article(driver)
    driver.close()
    DB(article).save("/world/africa")