#%%
from splinter import Browser
from bs4 import BeautifulSoup
#%%
executablePath = {'executable_path' : "chromedriver.exe"}
aBrowserInstance = Browser('chrome' , **executablePath)
# %%
baseUrl = 'https://old.reddit.com/r/pythoncoding/'
aBrowserInstance.visit(baseUrl)
# %%
print(aBrowserInstance.html)
# %%
def getATags(htmlText: str):
    parsedHTML = BeautifulSoup(htmlText, 'html.parser')
    pageLinks = parsedHTML.find_all('a')
    return pageLinks
# %%
soup = BeautifulSoup(aBrowserInstance.html, 'html.parser')
allPTags = soup.find_all('p')
# %%
allPTags
# %%
subredditTitles = []
for tag in allPTags:
    if tag.strong != None:
        if 'subreddit' in tag.strong.text:
            subredditTitles.append(tag.strong.text)
            print(tag.strong.text)
# %%
for line in soup:
    print(line.get_text().split('\n'))
# %%
