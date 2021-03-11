#%%
from splinter import Browser
from bs4 import BeautifulSoup
#%%
executablePath = {'executable_path' : "chromedriver.exe"}
aBrowserInstance = Browser('chrome' , **executablePath)
# %%
baseUrl = 'https://astronomy-imaging-camera.com/product-category/planetary-cameras'
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
allDivTags = soup.find_all('div', class_='featured_image img_loaded')
# %%
allDivTags
# %%
productImgUrls = []
for tag in allDivTags:
    print(tag.img)
    if tag.a.img != None:
        productImgUrls.append(tag.img['src'])
# %%
productImgUrls
# %%
