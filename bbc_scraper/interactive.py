from constants import BBC_NEWS
from bs4 import BeautifulSoup as bs
from logger import logger

def get_available_topics(driver):
    """
    returns a topics list that can be scraped
    """
    logger.info("Scrapping the available topics")
    driver.get('https://www.' + BBC_NEWS)
    page = driver.page_source
    soup = bs(page, 'html.parser')
    find_all = soup.find_all("li", 'nw-c-nav__wide-menuitem-container')
    result = []
    for element in find_all:
        result.append(element.a["href"])
    home_result = result[0]
    topics_l = [ele[6:] for ele in result[1:]]
    topics_l.insert(0, home_result)
    return topics_l[0:]


def topic_selector(topics):
    """
    displays to the user available topics 
    and return the one that the user has selected
    """
    print("\nThe available topics are:")

    for i in range(1, len(topics)):
        print(i, "-", topics[i])

    chosen_topic_no = "-1"
    while not chosen_topic_no.isdigit or (int(chosen_topic_no) not in range(len(topics))):
        chosen_topic_no = input("Which topic would you like to scrap? \nSelect the topic number: ")

    topic_url = 'https://www.' + BBC_NEWS + '/' + topics[int(chosen_topic_no)] + '/'
    print('Topic url is', topic_url)
    return topic_url
