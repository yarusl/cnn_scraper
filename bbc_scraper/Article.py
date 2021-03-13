import pymysql
from constants import BBC_PROTOCOL
from settings import USER, PASSWORD, HOST, DATABASE
from bs4 import BeautifulSoup as bs
# Connect to the database
connection = pymysql.connect(host=HOST,
                             user=USER,
                             password=PASSWORD,
                             database=DATABASE,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


class Article:
    def __init__(self, title, short_text, date, url, img):
        self.title = title
        self.short_text = short_text
        self.date = date
        self.url = BBC_PROTOCOL+url
        self.img = img
        self.author = None
        self.author_pos = None

    def scrape_art(self, driver):
        """For each article that was scraped from news update, we scrape as much information as possible"""

        print(self.url)
        driver.get(self.url)
        page = driver.page_source
        soup = bs(page, 'html.parser')

        # self.rel_topics
        # BBC Related topics for this article are saved in a dict
        self.related_top = {}
        for ele in soup.findAll("a", {"class": "ed0g1kj1"}):
            self.related_top[ele.text] = ele["href"]

        # self.text
        # We save the entire article text
        self.text = ""
        for text_bloc in soup.findAll("div", {"class": "e1xue1i83"}):
            self.text += text_bloc.text

        # self.author
        # We save the author
        author = soup.find("p", {"class": "e5xb54n0"})
        # TODO check the and span.contents[2]
        if author is not None:
            self.author = author.strong.text
            try:
                self.author_pos = author.span.contents[2]
            except IndexError as e:
                print(f"Job position not written in position 2 of the span.content section {e}")


        # self.rel_articles
        # We save the related articles
        self.rel_articles = {}
        rel_articles = soup.findAll("li", {"class": "e1nh2i2l2"})
        for link in rel_articles:
            self.rel_articles[link.p.span.text] = BBC_PROTOCOL + link.a["href"]

    def __str__(self):
        return f"""
-------------------------------------------------------------------------
{self.title}
Written by: {self.author} - {self.author_pos}

{self.text}

Posted date: {self.date}
Link of the article: {self.url}
Link to image: {self.img}
List of tags for the article and their links {self.related_top}
List of related articles and their links {self.rel_articles}

A summary to the article: {self.short_text}
-------------------------------------------------------------------------

"""

    def save(self, topic_url):
        """Saves the article in the database"""
        with connection.cursor() as cursor:
            try:
                variaable= f'INSERT INTO articles (title, text, date, url, image,topic_url) VALUES ({self.title}, {self.text}, {self.date}, {self.url},{self.img},{topic_url});'
                print(variaable)
                cursor.execute(variaable)
                cursor.commit()
            except Exception as e:
                print(e)