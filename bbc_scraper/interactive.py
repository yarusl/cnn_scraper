from constants import BBC_NEWS
from bs4 import BeautifulSoup as bs

def get_available_topics(driver):
    """
    returns a topics list that can be scraped
    """
    driver.get('https://www.'+BBC_NEWS)
    page = driver.page_source
    soup = bs(page, 'html.parser')
    find_all = soup.find_all("li",'nw-c-nav__wide-menuitem-container')
    result = []
    for element in find_all:
        result.append(element.a["href"])
    home_result = result[0]
    topics_l = [ele[6:] for ele in result[1:]]
    topics_l.insert(0,home_result)
    return topics_l

def topic_selector(topics):
    """
    displays to the user available topics 
    and return the one that the user has selected
    """
    print("topic list",topics)
    print("The available topics are",topics)
    topics_dict = {}
    topics_dict[0] = "News Homepage"
    for i in range(1,len(topics)):
        topics_dict[i] = topics[i]
    print(topics_dict)
    chosen_topic_no = int(input("Which topic would you like to scrap? - Select the topic number"))
    topic_url ='https://www.'+ BBC_NEWS +'/'+ topics[chosen_topic_no]+'/'
    print('topic url is',topic_url)
    return topic_url