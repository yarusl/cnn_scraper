# NYT_scraper

## Main Features of the scraper

- Scrapes latest news on any topic of the BBC website in the news section e.g.  [wales](https://www.bbc.com/news/wales) or [business](https://www.bbc.com/news/business)
- Scrapes multiple pages of the latest news updates on a topic. 
- If you're not sure which topic you want to scrape, the sraper will provide you a list of potential topics available for scraping.

#### Main scraped information for each article - i.e. - Article class attributes

title: title of the article. \
date: date on which the article was posted. \
url: url of the article. \
img: Image in the article when there is one. \
author: Author of the article.\
author_pos: Job Title of the author.\
short_text: short summary of the article (1 to 2 lines in general).\
text: Full text of the article.\
rel_topics: flags that say to which topics an article is related. \
rel_articles: other articles linked to this article.  

-------------
# Usage
## Install and run in 4 steps
### Step1 - Clone the git repository
To use the scraper simply download the project and go to the project main directory:

`$ git clone https://github.com/yarusl/nytimes_scraper.git`

`$ cd nytimes_scraper/nytimes_scraper`

##### Ensure the right permissions are in place.
If you're using linux or mac you should run this command before running the main.py script (once it's done, you don't have to run this command anymore in the future):

`$ chmod 755 drivers/*`

And then run the main.py file:

`$ python3 main.py -d PATH_TO_DRIVER`

### Step 2 - Set the parameters you want in the settings.py file
HOST = enter your mySQL host. Leave it as parametered if you are unsure if it needs changing.
USER = enter your mySQL user name
PASSWORD: enter your mySQL user password
DATABASE: name of the database you will be using. By default "mydb" (created from the init.sql file - see Step 3)

### Step 3 - run the init.sql file
- Go into your CLI
- Run your mysql
- Run the init.sql file that is located in the main directory of our BBC scraper.

### Step 4 - Run the scraper
1) Choose your mode (by default = Interactive)
2) Run the main.py 

-------------
## Modes
#### Interactive mode
The scraper has two modes, the first one is the interactive mode and it is the default mode. When the scraper runs in the interactive mode it will check which news topics could be potentially scraped. Some of them will be scrapable, some of them not. It depends on if the news topic has a "latest updates"section on the page.  

After the scraper has done with fetching the available topics it will show a promt and ask you which one of the topics you want to scrape (keep in mind that you could choose and unscrapable topic, the program doesn't check in advance if you can actually scrape the topic. It just gives you a list). 
The last thing it is going to ask you is how many pages do you want to scrape.  

After that it will print you the final result. 
<br>

#### Silent mode
The second one is the silent mode. In this mode you have to specify the link to the topic  and the number of pages by hand, changing variables in the <b>_settings.py_</b> file.

<b>_settings.py_ :</b>
<pre>mode = INTERACTIVE_MODE # SILENT_MODE
topic_url = "https://www.bbc.com/news/wales"  # your url example: "https://www.bbc.com/news/the_reporters"
articles_to_scrape = 1
</pre>
-------------
## CLI usage
Arguments for the Command Line interface:\
'-u', '--url', type=str, help='foo help' : --> url of the section to scrape in case you want to use the silent mode. No argument needed for interactive mode.\
'-p', '--pages', type=int, default=1, help='baz help' : --> number of pages to scrape in the section.\
'-d', '--driver', type=str, help='foo help' : --> your path to your driver.\

-------------
## Troubleshooting

The main issues you might face are related to the chromedriver. If you have any issues with the chromdriver it's recomended to find another one from [this link](https://chromedriver.chromium.org/downloads) and replace the existing chromedriver file with the one you download. 

<b>If you found any bugs please report it on the [official report](https://github.com/yarusl/nytimes_scraper/issues) </b>

-------------
