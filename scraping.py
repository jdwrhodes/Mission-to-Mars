# %%
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# %%
# Set the executable path and initialize chrome browser in splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# %%
# Visit the mars nasa news site
url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1) 
# 'wait_time' is telling the browser to wait before loading the next page a set amount of time


# %%
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')
# the period after div is used to select the class you wish to return
# select_one finds the first matching tag


# %%
slide_elem.find('div', class_='content_title')


# %%
# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# %%
# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# %% [markdown]
# ### Featured Images

# %%
# visit url
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# %%
# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1] # the [1] means we are storing the Second button found, due to python indexing
full_image_elem.click() # <--- used to "click"


# %%
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# %%
# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src') # get() indicates what you want to retrieve
img_url_rel


# %%
# Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# %%
df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
df.head()

df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# %%
df.to_html()


# %%
browser.quit()


