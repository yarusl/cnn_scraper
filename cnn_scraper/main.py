from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import bs4 as bs

from interactive import (
        get_available_topics, 
        topic_selector
    )

from constants import (
        SILENT_MODE, 
        INTERACTIVE_MODE
    )
from CnnScraper import CnnScraper
#soup = bs.BeautifulSoup(source, 'html.parser')


def create_driver(mode, driver_path):
    chrome_options = Options()
    
    if not mode:
        chrome_options.add_argument("--headless")

    return webdriver.Chrome(driver_path, options=chrome_options)

def main():
    """ 
    The program has two modes. 
    
    The first one is called SILENT_MODE, and that means 
    that you specify the information you want in the 
    program itself by changing the variables in this function.
    
    The second mode is the INTERACTIVE_MODE mode, witch is 
    enabled by default. This mode will display to you all 
    the topics that are available for scraping and ask you 
    which one of them you want to scrape. Then it will ask 
    you how many pages you want to scrape.

    You also need to scpecify the path to the webdriver you're 
    using in the 'path_to_driver' variable
    """

    mode = INTERACTIVE_MODE # choose a mode 
    path_to_driver = './chromedriver' # path to your webdriver
    driver = create_driver(mode, path_to_driver)
    
    if mode == SILENT_MODE:
        topic_url = '' # your url example: "https://www.bbc.com/news/the_reporters"
        pages_to_scrape = 1 # how many pages you want to scrape 

    elif mode == INTERACTIVE_MODE:
        topics = get_available_topics(driver)
        topic_url = topic_selector(topics)
        pages_to_scrape = int(input("How many pages you want to scrape?"))
    
    else:
        raise Exception("Invalid mode")
    
    cnn_scraper = CnnScraper(driver, topic_url, pages_to_scrape)
    cnn_scraper.scrape()
    print(cnn_scraper)
    del cnn_scraper

def demo_main():
    # for testing and debuging purposes
    mode = SILENT_MODE
    path_to_driver = './chromedriver.exe' # path to your webdriver
    driver = create_driver(mode, path_to_driver)
    topic_url = '' # your url
    pages_to_scrape = 1 # how many pages you want to scrape

def demo_mac():
    print('hello world')
    # for testing and debuging purposes
    mode = SILENT_MODE
    path_to_driver = './chromedriver' # path to your webdriver
    driver = create_driver(mode, path_to_driver)
    topic_url = '' # your url
    pages_to_scrape = 1 # how many pages you want to scrape
    cnn_scraper = CnnScraper(driver, topic_url, pages_to_scrape)
    cnn_scraper.validate_topic(topic_url)
    
if __name__ == "__main__":
    main()