from pynytimes import NYTAPI
nyt = NYTAPI("qeOAmrE6yGzowmzGiIpoK0ZBHOnyJ8BG", https=False)
metadata = nyt.article_metadata(url = "https://www.nytimes.com/2019/10/20/world/middleeast/erdogan-turkey-nuclear-weapons-trump.html")
print(metadata)

