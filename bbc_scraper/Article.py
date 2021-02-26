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