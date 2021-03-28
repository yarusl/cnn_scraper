import pymysql
from constants import BBC_PROTOCOL
from bs4 import BeautifulSoup as bs

class Article:
    def __init__(self, title, short_text=None, date, url, img):
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
        
        self.author = None
        self.author_pos = None
        self.img = img
        self.date = date
        self.title = title
    
    def scrape_tags(self, soup):
        # BBC Related topics for this article are saved in a dict
        tags = {}
        for ele in soup.findAll("a", {"class": "ed0g1kj1"}):
            tags[ele.text] = ele["href"]

        return tags

    def scrape_text(self, soup):
        # We save the entire article text
        text = ""
        for text_bloc in soup.findAll("div", {"class": "e1xue1i83"}):
            text += text_bloc.text
        return text

    def scrape_author(self, soup):
        # We save the author
        author = soup.find("p", {"class": "e5xb54n0"})
        if author is not None:
            author_name = author.strong.text
            try:
                author_pos = author.span.contents[2]
            except IndexError:
                print(f"No job position given")
        return author_name, author_pos

    def scrape_links(self, soup):
        # We save the related articles
        links = {}
        links = soup.findAll("li", {"class": "e1nh2i2l2"})
        for link in links:
            links[link.p.span.text] = BBC_PROTOCOL + link.a["href"]
        return links

    def scrape_art(self, driver):
        """For each article that was scraped from news update, we scrape as much information as possible"""

        print(self.url)
        driver.get(self.url)
        page = driver.page_source
        soup = bs(page, 'html.parser')

        self.tags = self.scrape_tags(soup)
        self.text = self.scrape_text(soup)
        self.author_name, self.author_pos = self.scrape_author(soup)
        self.links = self.scrape_links(soup)

    def __str__(self):
        return f"""
-------------------------------------------------------------------------
{self.title}
Written by: {self.author} - {self.author_pos}

{self.text}

Posted date: {self.date}
Link of the article: {self.url}
Link to image: {self.img}
List of tags for the article and their links {self.tags}
List of related articles and their links {self.links}

A summary to the article: {self.short_text}
-------------------------------------------------------------------------

"""
    
    
