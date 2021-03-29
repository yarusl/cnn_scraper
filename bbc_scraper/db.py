from settings import USER, PASSWORD, HOST, DATABASE
import pymysql
from logger import logger


# Connecting to the database
logger.debug('Connecting to the database with pymysql')
connection = pymysql.connect(host=HOST,
                             user=USER,
                             password=PASSWORD,
                             database=DATABASE,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
                
class DB():
    """
    This class purpose is to interact in SQL with the database. This class is used by Article.py to store the scrapped data.
    """
    def __init__(self, article):
        self.article = article
                
    def get_id(self, fetched):
        """ 
        returns id if not none 
        """
        if fetched:
            return fetched["id"]
        return None

    def save_author(self, name, title):
        """ saves the author and returns his id """
        logger.debug('Running save_author')
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"""
                        INSERT INTO author (name, title)
                        VALUES ( %s, %s );""", 
                    (name, title))
                
                connection.commit()
            except pymysql.err.IntegrityError:
                pass

            cursor.execute(f"SELECT * FROM author WHERE name = %s limit 1;", (name,))
            return self.get_id(cursor.fetchone())

    def save_text(self, summary, article_text):
        """ saves text and returns its id"""
        logger.debug('Running save_text')
        with connection.cursor() as cursor:
            cursor.execute(f"""
                    INSERT INTO txt (summary, article_text)
                    VALUES (%s, %s); """, (summary, article_text ))
            connection.commit()

            query = f"""
                SELECT * FROM txt 
                WHERE 
                    summary=%s and 
                    article_text=%s 
                limit 1;"""
            cursor.execute(query, (summary, article_text ))
            
            return self.get_id(cursor.fetchone())

    def save_topic(self, name, url):
        """ saves topic and returns its id """
        logger.debug('Running save_topics')
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"""
                        INSERT INTO topic (name, url)
                        VALUES ( %s, %s);""", 
                        (name, url))
                connection.commit()
            except pymysql.err.IntegrityError:
                pass

            cursor.execute(f"""
                SELECT * FROM topic 
                WHERE 
                    name= %s 
                limit 1;""", (name,))
            
            return self.get_id(cursor.fetchone())

    def get_author_id(self):
        """ returns authors id if author is defined """
        author, author_pos = self.article.get_author()
        if author:
            return self.save_author(author, author_pos)
        return None

    def get_text_id(self):
        """ returns text id if short text is defined """
        short_text = self.article.get_short_text()
        text = self.article.get_text()
         
        if text:
            return self.save_text(short_text, text)
        return None

    def get_topic_name(self, topic_url):
        """ extracts topic name from ropic url """
        return '/'.join(topic_url.split('/')[4:])

    def get_topic_id(self, topic_url):
        """ returns topic id """
        topic_name = self.get_topic_name(topic_url)
        return self.save_topic(topic_name, topic_url)

    def save_tag(self, name, url):
        """ saves one tag and returns its id """
        logger.debug('Running save_tag')
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"""
                        INSERT INTO tag (name, url)
                        VALUES (%s, %s);""", 
                        (name, url))
                connection.commit()
            except pymysql.err.IntegrityError:
                logger.error('Integrity error raised in save_tag from db.py')
                pass

            cursor.execute(f"""
                SELECT * FROM tag 
                WHERE 
                    name = %s 
                limit 1;""", 
                (name,))
            
            return self.get_id(cursor.fetchone())
    
    def save_article_tag(self, article_id, tag_id):
        """ saves a relationship between a tag and article """
        logger.debug('Running save_article_tag')
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"""
                        INSERT INTO article_tag (article_id, tag_id)
                        VALUES (%s, %s);""", 
                    (tag_id, article_id))
                connection.commit()
            except pymysql.err.IntegrityError:
                logger.error('Integrity error raised in save_article_tag from db.py')
                pass

    def save_tags(self, article_id):
        """ saves all tags """
        logger.debug('Running save_tags')
        for tag, tag_url in self.article.get_tags().items():
            tag_id = self.save_tag(tag, tag_url)
            self.save_article_tag(article_id, tag_id)

    def save_link(self, name, url): 
        """ saves one link to an article and returns its id """
        logger.debug('Running save_link')
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"""
                        INSERT INTO link (name, url)
                        VALUES (%s, %s);
                    """, 
                    (name, url))
                connection.commit()
            except pymysql.err.IntegrityError:
                logger.error('Integrity error raised in save_link from db.py')
                pass

            cursor.execute(f"""
                SELECT * FROM link
                WHERE 
                    name= %s 
                limit 1;""", 
                (name,))
            
            return self.get_id(cursor.fetchone())
    
    def save_article_link(self, article_id, link_id):
        """ saves a relationship between an article and link"""
        with connection.cursor() as cursor:
            try:
                logger.debug('Running save_article_links')
                cursor.execute(f"""
                        INSERT INTO article_link (article_id, link_id)
                        VALUES (%s, %s);""", 
                        (article_id, link_id))
                connection.commit()
            except pymysql.err.IntegrityError:
                pass

    def save_links(self, article_id):
        """ saves all links """
        logger.debug('Running save_links')
        for link, link_url in self.article.get_links().items():
            link_id = self.save_link(link, link_url)
            self.save_article_link(article_id, link_id)

    def save(self, topic_url):
        """Saves the article in the database"""
        url = self.article.get_url()
        title = self.article.get_title() 
        date = self.article.get_date()
        img = self.article.get_img()

        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM article WHERE url=%s', (url,))
            adsf = cursor.fetchone()
            if adsf != None:
                print()
                logger.debug(f"Article alread exists. Url: {url}")
                return

        author_id = self.get_author_id()
        topic_id = self.get_topic_id(topic_url)
        text_id = self.get_text_id()
        with connection.cursor() as cursor:
            query = f"""
                INSERT INTO article (
                    title, 
                    r_date, 
                    url, 
                    img, 
                    txt_id, 
                    author_id, 
                    topic_id
                ) VALUES ( %s, %s, %s, %s, %s, %s, %s );"""
            
            cursor.execute(query, (title, date, url, img, text_id, author_id, topic_id))
            connection.commit()
            
            cursor.execute(f'SELECT * FROM article WHERE url=%s', (url,))
            articel_id = self.get_id(cursor.fetchone())
        
        self.save_tags(articel_id)
        self.save_links(articel_id)