from base import *
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../bbc_scraper/')))
import Article

def test():
    title = "title" 
    text = "text"
    date = "date"
    url = "url"
    img = "img"
    article = Article.Article(title, text, date, url, img)

    expected_1 = """
-------------------------------------------------------------------------
`title`
text

Posted date: date
Link: url
Link to image: img
-------------------------------------------------------------------------

"""
    assert str(article) == expected_1
    
if __name__ == '__main__':
    test()