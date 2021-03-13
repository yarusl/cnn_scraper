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
        self.title = title
        self.short_text = short_text
        self.date = date
        self.url = BBC_PROTOCOL + url
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
        self.tags = {}
        for ele in soup.findAll("a", {"class": "ed0g1kj1"}):
            self.tags[ele.text] = ele["href"]

        # self.text
        # We save the entire article text
        self.text = ""
        for text_bloc in soup.findAll("div", {"class": "e1xue1i83"}):
            self.text += text_bloc.text

        # self.author
        # We save the author
        author = soup.find("p", {"class": "e5xb54n0"})
        if author is not None:
            self.author = author.strong.text
            try:
                self.author_pos = author.span.contents[2]
            except IndexError:
                print(f"No job position given")

        # self.links
        # We save the related articles
        self.links = {}
        links = soup.findAll("li", {"class": "e1nh2i2l2"})
        for link in links:
            self.links[link.p.span.text] = BBC_PROTOCOL + link.a["href"]


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
    def format_to_sql(self, val):
        if val:
            return val.replace('"', "'")
        return val

    def save_author(self, name, title):
        # return author_id
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"""
                        INSERT INTO author (name, title)
                        VALUES (
                            "{self.format_to_sql(name)}",
                            "{self.format_to_sql(title)}" 
                            );
                    """)
                
                connection.commit()
            except pymysql.err.IntegrityError:
                pass

            cursor.execute(f"SELECT * FROM author WHERE name = \"{name}\" limit 1;")
            return cursor.fetchone()["id"]

    def save_text(self, summary, article_text):
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"""
                        INSERT INTO txt (summary, article_text)
                        VALUES (
                            "{self.format_to_sql(summary)}",
                            "{self.format_to_sql(article_text)}" 
                            );
                    """)
                connection.commit()
            except pymysql.err.IntegrityError:
                pass

            cursor.execute(f"""
                SELECT * FROM txt 
                WHERE 
                    summary=\"{summary}\" and 
                    article_text=\"{article_text}\" 
                limit 1;""")
            
            return cursor.fetchone()["id"]

    def save_topic(self, name, url):
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"""
                        INSERT INTO topic (name, url)
                        VALUES (
                            "{self.format_to_sql(name)}",
                            "{self.format_to_sql(url)}" 
                            );
                    """)
                connection.commit()
            except pymysql.err.IntegrityError:
                pass

            cursor.execute(f"""
                SELECT * FROM topic 
                WHERE 
                    name=\"{name}\" 
                limit 1;""")
            
            return cursor.fetchone()["id"]

    def get_author_id(self):
        if self.author:
            return self.save_author(self.author, self.author_pos)
        return None

    def get_text_id(self):
        if self.short_text:
            return self.save_text(self.short_text, self.text)
        return None

    def get_topic_name(self, topic_url):
        return '/'.join(topic_url.split('/')[4:])

    def get_topic_id(self, topic_url):
        topic_name = self.get_topic_name(topic_url)
        return self.save_topic(topic_name, topic_url)

    def save_tag(self, name, url):
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"""
                        INSERT INTO tag (name, url)
                        VALUES (
                            "{self.format_to_sql(name)}",
                            "{self.format_to_sql(url)}" 
                            );
                    """)
                connection.commit()
            except pymysql.err.IntegrityError:
                pass

            cursor.execute(f"""
                SELECT * FROM tag 
                WHERE 
                    name=\"{name}\" 
                limit 1;""")
            
            return cursor.fetchone()["id"]
    
    def save_article_tag(self, article_id, tag_id):
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"""
                        INSERT INTO article_tag (article_id, tag_id)
                        VALUES (
                            "{article_id}",
                            "{tag_id}" 
                            );
                    """)
                connection.commit()
            except pymysql.err.IntegrityError:
                pass

    def save_tags(self, article_id):
        for tag, tag_url in self.tags.items():
            tag_id = self.save_tag(tag, tag_url)
            self.save_article_tag(article_id, tag_id)

    def save_link(self, name, url):
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"""
                        INSERT INTO link (name, url)
                        VALUES (
                            "{self.format_to_sql(name)}",
                            "{self.format_to_sql(url)}" 
                            );
                    """)
                connection.commit()
            except pymysql.err.IntegrityError:
                pass

            cursor.execute(f"""
                SELECT * FROM link
                WHERE 
                    name=\"{name}\" 
                limit 1;""")
            
            return cursor.fetchone()["id"]
    
    def save_article_link(self, article_id, link_id):
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"""
                        INSERT INTO article_link (article_id, link_id)
                        VALUES (
                            "{article_id}",
                            "{link_id}" 
                            );
                    """)
                connection.commit()
            except pymysql.err.IntegrityError:
                pass

    def save_links(self, article_id):
        for link, link_url in self.links.items():
            link_id = self.save_link(link, link_url)
            self.save_article_link(article_id, link_id)

    def save(self, topic_url):
        """Saves the article in the database"""
        author_id = self.get_author_id()
        text_id = self.get_text_id()
        topic_id = self.get_topic_id(topic_url)

        articel_id = None

        with connection.cursor() as cursor:
            try:
                query = f"""
                    INSERT INTO article (
                        title, 
                        r_date, 
                        url, 
                        img, 
                        txt_id, 
                        author_id, 
                        topic_id
                    ) VALUES (
                        "{self.format_to_sql(self.title)}", 
                        "2018-01-01",
                        "{self.format_to_sql(self.url)}",
                        "{self.format_to_sql(self.img)}",
                        "{text_id}",
                        "{author_id}",
                        "{topic_id}"
                    );"""
                
                cursor.execute(query)
                connection.commit()
            except Exception as e:
                print(e)

            cursor.execute(f'SELECT * FROM article WHERE url="{self.format_to_sql(self.url)}"')
            articel_id = cursor.fetchone()["id"]

        self.save_tags(articel_id)   
        self.save_links(articel_id)
