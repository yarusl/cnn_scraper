from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from NYT_scraper import NYT_scraper
from constants import (
    SILENT_MODE,
    INTERACTIVE_MODE
)
from interactive import (
    get_available_topics,
    topic_selector
)

from settings import mode, articles_to_scrape, topic_url
from settings import driver_path, DEMO, DEMO_TOPIC, DEMO_ARTICLE_SCRAP
from db import DB

from logger import logger
from settings import DEMO, DEMO_TOPIC, DEMO_ARTICLE_SCRAP


def create_driver(mode, executable_path):
        """
        Create a Chromedriver ready for scraping with 2 modes
        Mode by default = INTERACTIVE. Meaning we ask the user to choose the topic they want to scrape and the number of pages.
        Other mode = SILENT. With input from the CLI the user can run the scrape directly from a URL. (see cli.py for details on usage)
        """
        logger.debug("Running create_driver")
        chrome_options = Options()

        if mode == SILENT_MODE:
            logger.info("Silent mode chosen")
            chrome_options.add_argument("--headless")
        elif mode == INTERACTIVE_MODE:
            logger.info("Interactive mode chosen")
            chrome_options.add_experimental_option("detach", True)
        else:
            logger.debug("Invalid mode")
            raise Exception("Invalid mode")
        
        driver = webdriver.Chrome(executable_path=executable_path, options=chrome_options)
        driver.set_window_size(1000, 800)
        return driver
    
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
    using in the 'driver_path' variable
    """
    logger.debug("Running main function")
    global topic_url, mode, articles_to_scrape, driver_path
    driver = create_driver(mode, driver_path)

    if mode == INTERACTIVE_MODE:
        if DEMO:
            topic_url = DEMO_TOPIC
            articles_to_scrape = DEMO_ARTICLE_SCRAP
        else: 
            try:
                topics = get_available_topics(driver)
                topic_url = topic_selector(topics)
                articles_to_scrape = int(input("How many articles do you want to scrape? "))
            
            except ValueError as e:
                logger.warning(f"the interactive mode did not work on its try due to a ValueError: {e}")
            except TypeError as e:
                logger.warning(f"the interactive mode did not work on its try due to a TypeError: {e}")
            except SyntaxError as e:
                logger.warning(f"the interactive mode did not work on its try due to a SyntaxError: {e}")
            except Exception as e:
                logger.warning(f"the interactive mode did not work on its try due a general exception: {e}")

    nyt_scraper = NYT_scraper(driver, topic_url, articles_to_scrape)
    nyt_scraper.scrape()
    #nyt_scraper.print_info()
    nyt_scraper.save()
    del nyt_scraper

if __name__ == "__main__":
    main()