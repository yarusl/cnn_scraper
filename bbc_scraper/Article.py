import pymysql
from settings import USER, PASSWORD, HOST, DATABASE
# Connect to the database
connection = pymysql.connect(host=HOST,
                             user=USER,
                             password=PASSWORD,
                             database=DATABASE,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


class Article:
    def __init__(self, title, text, date, url, img):
        self.title = title
        self.text = text
        self.date = date
        self.url = url
        self.img = img

    def __str__(self):
        return f"""
-------------------------------------------------------------------------
`{self.title}`
{self.text}

Posted date: {self.date}
Link: {self.url}
Link to image: {self.img}
-------------------------------------------------------------------------

"""
    def save(self,topic_url):
        """Saves the article in the database"""
        with connection.cursor() as cursor:
            try:
                cursor.execute(f'''
                    INSERT INTO Articles (`title`, `text`, `date`, `url`, `image`,`topic_url`) 
                    VALUES (
                            `{self.title}`, 
                            `{self.text}`, 
                            `{self.date}`, 
                            `{self.url}`,
                            `{self.img}`,
                            `{topic_url}`);''')
                cursor.commit()
            except Exception as e:
                print(e)