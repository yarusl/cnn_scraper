from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from settings import mode, pages_to_scrape, topic_url
from os import path 

from settings import driver_path
from interactive import (
    get_available_topics,
    topic_selector
)

from constants import (
    SILENT_MODE,
    INTERACTIVE_MODE
)
from BBCScraper import BBCScraper

import sys



def create_driver(mode, executable_path):
    """
    Create a Chromedriver ready for scraping with 2 modes
    Mode by default = INTERACTIVE. Meaning we ask the user to choose the topic they want to scrape and the number of pages.
    Other mode = SILENT. With input from the CLI the user can run the scrape directly from a URL. (see cli.py for details on usage)
    """
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
    using in the 'driver_path' variable
    """
    
    global topic_url, mode, pages_to_scrape, driver_path
    driver = create_driver(mode, driver_path)

    if mode == INTERACTIVE_MODE:
        try:
            topics = get_available_topics(driver)
            topic_url = topic_selector(topics)
            pages_to_scrape = int(input("How many pages you want to scrape? "))
        except ValueError as e:
            print(f"the interactive mode did not work on its try due to a ValueError: {e}")
        except TypeError as e:
            print(f"the interactive mode did not work on its try due to a TypeError: {e}")
        except SyntaxError as e:
            print(f"the interactive mode did not work on its try due to a SyntaxError: {e}")
        except Exception as e:
            print(f"the interactive mode did not work on its try due a general exception: {e}")

    bbc_scraper = BBCScraper(driver, topic_url, pages_to_scrape)
    bbc_scraper.scrape()
    bbc_scraper.print_info()
    bbc_scraper.save()
    del bbc_scraper


if __name__ == "__main__":
    main()
