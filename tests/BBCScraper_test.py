from base import *
from BBCScraper import BBCScraper
from main import create_driver, get_driver_path
from constants import *
from selenium.webdriver.chrome.options import Options

# Lets create a scraper to test the methods on a chosen arbitrary topic Url: here the technology section
test_topic_url = 'https://www.bbc.com/news/technology'
driver = create_driver(SILENT_MODE, get_driver_path())
test_bbc_scraper = BBCScraper(driver=driver, topic_url=test_topic_url, pages_to_scrape=1)

# Test of the latest update method of BBCScrapper
try:
    test_bbc_scraper.scrape_latest_updates()
except Exception as ex:
    print(f'ERROR in scrape_latest_updates method: {ex}\n, ')

# Test of the validate_url method of BBCScrapper
try:
    test_bbc_scraper.validate_url(test_topic_url)
except Exception as ex:
    print(f'ERROR in validate_url method of BBCScraper: {ex}\n, ')

try:
    test_bbc_scraper.validate_url('www.wrong-url.com')
    print("validate_url doesn't work properly")
except Exception as ex:
    pass
