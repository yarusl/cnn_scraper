from cli import parse_args
from pynytimes import NYTAPI
mode, topic_url, articles_to_scrape, driver_path = parse_args()

# For testing: If True only one article is scrapped
DEMO = True
DEMO_TOPIC = 'https://www.nytimes.com/section/world/africa'
DEMO_ARTICLE_SCRAP = 3

# Database details
HOST = 'localhost'
DATABASE = 'nytimes'

# your variables
USER = 'root'
PASSWORD = 'futur((('

# Settings for the logger
LOG = 'log_file.log'
NYTname = 'scrapper'

# API key for the NYT API
nyt = NYTAPI("qeOAmrE6yGzowmzGiIpoK0ZBHOnyJ8BG", https=False)