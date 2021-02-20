class Article: 
    def __init__(self, title, text, date, url, img):
        self.title = title
        self.text = text
        self.date = date
        self.url = url
        self.img = img

    def __str__(self):
        """ 
        returns a readable string 
        representation of this Article
        """
        pass