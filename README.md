# BBCScraper

![](https://raw.githubusercontent.com/yarusl/bbc_scraper/main/img/logo.png)

## Features

- Scrapes latest news on any topic e.g.  [wales](https://www.bbc.com/news/wales) or [business](https://www.bbc.com/news/business)
- Scrapes multiple pages of the latest news updates on a topic
- If you're not sure which topic you want to scrape, the sraper will provide you a list of potentialy available topics
-------------

# Usage
To use the scraper simply download the project and go to the project main directory:

`$ git clone https://github.com/yarusl/bbc_scraper.git`

`$ cd bbc_scraper/bbc_scraper`

If you're using linux or mac you should run this command before running the main.py script (once it's done, you don't have to run this command anymore in the future):

`$ chmod 755 drivers/*`

And then run the main.py file:

`$ python3 main.py`

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
pages_to_scrape = 1
</pre>

## Troubleshooting

The main issues you might face are related to the chromedriver. If you have any issues with the chromdriver it's recomended to find another one from [this link](https://chromedriver.chromium.org/downloads) and replace the existing chromedriver file with the one you download. 

<b>If you found any bugs please report it on the [official report](https://github.com/yarusl/bbc_scraper.git) </b>
