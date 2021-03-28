from newsapi import NewsApiClient
from constants import APIKEY
import json

# Init
newsapi = NewsApiClient(api_key=APIKEY)

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(q='bitcoin',
                                          category='business',
                                          language='en',
                                          country='us')

# /v2/everything
all_articles = newsapi.get_everything(q='bitcoin',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param='2021-02-28',
                                      to='2021-03-28',
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)

with open('data.json', 'w') as outfile:
    json.dump(all_articles, outfile)

# /v2/sources
sources = newsapi.get_sources()