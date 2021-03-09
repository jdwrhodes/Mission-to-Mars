#%%
from splinter import Browser
from bs4 import BeautifulSoup
#%%
executablePath = {'executable_path' : "./chromedriver.exe"}
aBrowserInstance = Browser('chrome' , **executablePath)
# %%
baseUrl = 'http://www.weasner.com'
aBrowserInstance.visit(baseUrl)
# %%
print(aBrowserInstance.html)
# %%
parsedHTML = BeautifulSoup(aBrowserInstance.html, 'html.parser')
# %%
print(parsedHTML)
# %%
mainPageLinks = parsedHTML.find_all('a')
# %%
print(mainPageLinks)
# %%
print(mainPageLinks[0]['href'])
# %%
def getATags(htmlText: str):
    parsedHTML = BeautifulSoup(htmlText, 'html.parser')
    pageLinks = parsedHTML.find_all('a')
    return pageLinks
#%%
level1Html: list = []
invalidUrl: list = []

#%%
for aTag in mainPageLinks:
    href = aTag['href']
    goToLink = f'{baseUrl}/{href}'
    try:
        level1Html.append(goToLink)
        aBrowserInstance.visit(goToLink)
        objectsToVisit = getATags(aBrowserInstance.html)
    except:
        invalidUrl.append(goToLink)
# %%
def crawlSite(mainPageLinks,visitUrl, invalidUrl):
    
    for aTag in mainPageLinks:
        href = aTag['href']
        goToLink = f'{baseUrl}/{href}'
        try:
            if goToLink not in visitUrl:
                aBrowserInstance.visit(goToLink)
                visitUrl.append(goToLink)
                objectsToVisit = getATags(aBrowserInstance.html)
                crawlSite(objectsToVisit,visitUrl,invalidUrl)
        except:
            invalidUrl.append(goToLink)
#%%
# level1Html: list = []
invalidUrl: list = []
# newUrl = []
visitUrl = []
invalidUrl = []

crawlSite(mainPageLinks,visitUrl,invalidUrl)

# %%
