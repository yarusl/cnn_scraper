from cli import parse_args
mode, topic_url, pages_to_scrape, driver_path = parse_args()

# For testing: If True only one article is scrapped
DEMO = True

# Database details
HOST = 'localhost'
DATABASE = 'bbc_scraper'

# your variables
USER = 'root'
PASSWORD = ''

# Settings for the logger
LOG = 'log_file.log'
BBCname = 'BBCscrapper'