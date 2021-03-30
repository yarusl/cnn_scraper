from constants import NYTIMES_NEWS
from bs4 import BeautifulSoup as bs
from logger import logger
from settings import driver_path

def get_available_topics(driver):
    """
    returns a topics list that can be scraped
    """
    logger.info("Scrapping the available topics")
    driver.get('https://www.' + NYTIMES_NEWS)
    driver.find_element_by_class_name("css-fzvsed").click()
    
    soup = bs(driver.page_source, 'html.parser')
    driver.find_element_by_id("close-modal").click()
    
    find_all = soup.find_all("a", 'css-s1nhwm')
    result = {}
    for element in find_all[1:]:
        result[element.text] = element["href"]

    return result

def topic_selector(topics):
    """
    displays to the user available topics 
    and return the one that the user has selected
    """
    print("\nThe available topics are:")

    keys = list(topics.keys())
    for i in range(1, len(keys) + 1):
        print(i, "-", keys[i - 1])

    chosen = "-1"
    while not chosen.isdigit or (int(chosen) not in range(1, len(topics) + 1)):
        chosen = input("Which topic would you like to scrap? \nSelect the topic number: ")

    key = keys[int(chosen) - 1]
    topic_url = topics[key]
    print('Topic url is', topic_url)
    return topic_url
