class Article: 
    def __init__(self, title, author, date, url, img):
        self.title = title
        self.author = author 
        self.date = date
        self.url = url
        self.img = img
    
    def __str__(self):
        """ 
        returns a readable string 
        representation of this Article
        """
        pass