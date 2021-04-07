import pymysql
from constants import BBC_PROTOCOL
from bs4 import BeautifulSoup as bs
from logger import logger

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
        self.short_text = short_text
        self.url = BBC_PROTOCOL + url
        self.author_name = None
        self.author_pos = None
 
    def scrape_date(self):
        """
        scrapes the date
        """
        date = self.soup.find('dd', {"class": 'e1ojgjhb2'})
        if date is None:
            return None
        return date.text
   
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
        images = self.soup.findAll("img", {"class": "ssrcss-evoj7m-Image ee0ct7c0"})
        if not len(images):
            return None
        return images[0]["src"]

    def scrape_tags(self):
        """
        scrapes tags related to the article
        """
        # BBC Related topics for this article are saved in a dict
        logger.debug('Running scrape_tags')
        tags = {}
        for ele in self.soup.findAll("a", {"class": "ed0g1kj1"}):
            tags[ele.text] = ele["href"]

        return tags

    def scrape_text(self):
        """
        scrapes the text of the article
        """
        logger.debug('Running scrape_text')
        # We save the entire article text
        text = ""
        for text_bloc in self.soup.findAll("div", {"class": "e1xue1i83"}):
            text += text_bloc.text
        return text

    def scrape_author(self):
        """
        scrapes the author
        """
        # We save the author
        logger.debug('Running scrape_author')
        author = self.soup.find("p", {"class": "e5xb54n0"})
        if author is not None:
            author_name = author.strong.text.lstrip('By')
            try:
                author_pos = author.span.contents[2]
            except IndexError:
                author_pos = None
                logger.error(f"No job position given")
            
            return author_name, author_pos
        return None, None

    def scrape_links(self):
        """
        scrapes links to other related articles
        """
        # We save the related articles
        ret_links = {}
        links = self.soup.findAll("li", {"class": "e1nh2i2l2"})
        for link in links:
            print(link.p.span.text)
            print(links)
            ret_links[link.p.span.text] = BBC_PROTOCOL + link.a["href"]
        
        return ret_links

    def scrape_article(self, driver):
        """For each article that was scraped from news update, we scrape as much information as possible"""
        
        print(self.url)
        driver.get(self.url)
        page = driver.page_source
        self.soup = bs(page, 'html.parser')

        self.date = self.scrape_date()
        self.title = self.scrape_title()
        self.img = self.scrape_img()
        self.tags = self.scrape_tags()
        self.text = self.scrape_text()
        self.author_name, self.author_pos = self.scrape_author()
        self.links = self.scrape_links()

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

    def get_tags(self):
        return self.tags
    
    def get_text(self):
        return self.text

    def get_author(self):
        return self.author_name, self.author_pos
    
    def get_links(self):
        return self.links

    def __str__(self):
        return f"""
-------------------------------------------------------------------------
{self.title}
Written by: {self.author_name} - {self.author_pos}

{self.text}

Posted date: {self.date}
Link of the article: {self.url}
Link to image: {self.img}
List of tags for the article and their links {self.tags}
List of related articles and their links {self.links}

A summary to the article: {self.short_text}
-------------------------------------------------------------------------

"""
