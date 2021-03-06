from base import *
from NYT_scraper import NYT_scraper
from main import create_driver, get_driver_path
from constants import *
from selenium.webdriver.chrome.options import Options
from logger import logger

# Lets create a scraper to test the methods on a chosen arbitrary topic Url: here the technology section
test_topic_url = 'https://www.bbc.com/news/technology'
driver = create_driver(SILENT_MODE, get_driver_path())
test_nyt_scraper = NYT_scraper(driver=driver, topic_url=test_topic_url, articles_to_scrape=1)

# Test of the latest update method of NYT_scraper
try:
    test_nyt_scraper.scrape_latest_updates()
except Exception as ex:
    print(f'ERROR in scrape_latest_updates method: {ex}\n, ')

# Test of the validate_url method of NYT_scraper
try:
    test_nyt_scraper.validate_url(test_topic_url)
except Exception as ex:
    logger.error(f'ERROR in validate_url method of NYT_scraper: {ex}\n, ')

try:
    test_nyt_scraper.validate_url('www.wrong-url.com')
    logger.warning("validate_url doesn't work properly")
except Exception as ex:
    pass
