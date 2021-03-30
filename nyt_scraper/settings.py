from cli import parse_args
mode, topic_url, articles_to_scrape, driver_path = parse_args()

# For testing: If True only one article is scrapped
DEMO = False

# Database details
HOST = 'localhost'
DATABASE = 'nytimes'

# your variables
USER = 'root'
PASSWORD = ''

# Settings for the logger
LOG = 'log_file.log'
NYTname = 'scrapper'
