from constants import BBC_NEWS
from bs4 import BeautifulSoup as bs

def get_available_topics(driver):
    """
    returns a topics list that can be scraped
    """
    driver.get('https://www.'+BBC_NEWS)
    page = driver.page_source
    soup = bs(page, 'html.parser')
    find_all = soup.find_all("li",'nw-c-nav__wide-menuitem-container')
    result = []
    for element in find_all:
        result.append(element.a["href"])
    return result

def topic_selector(topics):
    """
    displays to the user available topics 
    and return the one that the user has selected
    """
    pass