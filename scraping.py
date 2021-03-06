# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    
    # Run all scraping functions and store results in a dictionary. This is what will actually be stored in mongo and displayed on the website.
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemisphere_data(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data    

def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1) 
    # 'wait_time' is telling the browser to wait before loading the next page a set amount of time

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # the period after div is used to select the class you wish to return
        # select_one finds the first matching tag
        
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_paragraph = slide_elem.find('div', class_='article_teaser_body').get_text()
        
    except AttributeError:
        return None, None

    return news_title, news_paragraph

def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]  # the [1] means we are storing the Second button found, due to python indexing
    full_image_elem.click()  # <--- used to "click"

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src') # get() indicates what you want to retrieve

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def hemisphere_data(browser):
    hemisphere_image_urls = []
    image_counter = 3
    try:

        for x in range(1,5):
        
            url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'
            browser.visit(url)
            
            img_title = ''
            img_url = ''

            full_image_elem = browser.find_by_tag('img')[image_counter] 
            full_image_elem.click()
            
            html = browser.html
            img_soup = soup(html, 'html.parser')
            
            img_url = [i['href'] for i in img_soup.find_all('a', href=True) if i['href'] != '#'][1]

            img_title = img_soup.find('h2', class_='title').get_text()

            full_url = f'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/{img_url}'

            hemisphere_image_urls.append({'img_url': full_url, 'title': img_title})

            image_counter += 1
        return hemisphere_image_urls
    
    except BaseException:
        return None

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())