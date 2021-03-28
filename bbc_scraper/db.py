from settings import USER, PASSWORD, HOST, DATABASE
import pymysql

connection = pymysql.connect(host=HOST,
                             user=USER,
                             password=PASSWORD,
                             database=DATABASE,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

class DB():
    def __init__(self, aritcle):
        self.aritcle = aritcle
        
    def get_id(self, fetched):
        """ 
        returns id if not none 
        """
        if fetched:
            return fetched["id"]
        return None

    def save_author(self, name, title):
        """ saves the author and returns his id """
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
        if self.author:
            return self.save_author(self.author, self.author_pos)
        return None

    def get_text_id(self):
        """ returns text id if short text is defined """
        if self.short_text:
            return self.save_text(self.short_text, self.text)
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
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"""
                        INSERT INTO tag (name, url)
                        VALUES (%s, %s);""", 
                        (name, url))
                connection.commit()
            except pymysql.err.IntegrityError:
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
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"""
                        INSERT INTO article_tag (article_id, tag_id)
                        VALUES (%s, %s);""", 
                    (tag_id, article_id))
                connection.commit()
            except pymysql.err.IntegrityError:
                pass

    def save_tags(self, article_id):
        """ saves all tags """
        for tag, tag_url in self.tags.items():
            tag_id = self.save_tag(tag, tag_url)
            self.save_article_tag(article_id, tag_id)

    def save_link(self, name, url): 
        """ saves one link to an article and returns its id """
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"""
                        INSERT INTO link (name, url)
                        VALUES (%s, %s);
                    """, 
                    (name, url))
                connection.commit()
            except pymysql.err.IntegrityError:
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
                cursor.execute(f"""
                        INSERT INTO article_link (article_id, link_id)
                        VALUES (%s, %s);""", 
                        (article_id, link_id))
                connection.commit()
            except pymysql.err.IntegrityError:
                pass

    def save_links(self, article_id):
        """ saves all links """
        for link, link_url in self.links.items():
            link_id = self.save_link(link, link_url)
            self.save_article_link(article_id, link_id)

    def save(self, topic_url):
        """Saves the article in the database"""
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM article WHERE url=%s', (self.url,))
            if cursor.fetchone() != None:
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
            
            cursor.execute(query, (self.title, self.date, self.url, self.img, text_id, author_id, topic_id))
            connection.commit()
            
            cursor.execute(f'SELECT * FROM article WHERE url=%s', (self.url,))
            articel_id = self.get_id(cursor.fetchone())
        
        self.save_tags(articel_id)
        self.save_links(articel_id)