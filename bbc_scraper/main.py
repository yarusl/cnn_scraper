from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import bs4 as bs
from Article import Article

from interactive import (
        get_available_topics, 
        topic_selector
    )

from constants import (
        SILENT_MODE, 
        INTERACTIVE_MODE
    )
from BBCScraper import BBCScraper
from settings import mode, pages_to_scrape, topic_url
import sys

def get_driver_path():
    """ 
    returns the path to the driver 
    according to the operation system
    """
    platforms = {
        'linux' : "./drivers/l_chromedriver",
        'linux1' : "./drivers/l_chromedriver",
        'linux2' : "./drivers/l_chromedriver",
        'darwin' : "./drivers/chromedriver",
        'win32' : "./drivers/chromedriver.exe"
    }
    if sys.platform not in platforms:
        raise Exception('Unknown platform: %s' % sys.platform, \
                            "\nYou should download the chromedriver yourself "\
                            "and write the path to the chromedriver in the "\
                            "variable 'path_to_driver', which is located in the"\
                            "'main' function")
    
    return platforms[sys.platform]

def create_driver(mode, executable_path):
    chrome_options = Options()
    
    if mode == SILENT_MODE:
        chrome_options.add_argument("--headless")
    elif mode == INTERACTIVE_MODE:
        chrome_options.add_experimental_option("detach", True)
    else:
        raise Exception("Invalid mode")

    return webdriver.Chrome(executable_path=executable_path, options=chrome_options)

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

    path_to_driver = get_driver_path()  
    driver = create_driver(mode, path_to_driver)

    if mode == INTERACTIVE_MODE:
        topics = get_available_topics(driver)
        topic_url = topic_selector(topics)
        pages_to_scrape = int(input("How many pages you want to scrape? "))

    bbc_scraper = BBCScraper(driver, topic_url, pages_to_scrape)
    bbc_scraper.scrape()
    print(bbc_scraper)
    del bbc_scraper
    
if __name__ == "__main__":
    main()