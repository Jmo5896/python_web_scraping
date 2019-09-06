import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time

def scrape_mars():
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path)
    mars_title, mars_p = mars_news(browser)
    mars_dict = {
        'mars_title': mars_title,
        'mars_p': mars_p,
        'featured_image_url': mars_img(browser),
        'mars_weather': mars_weather(browser),
        'mars_facts':mars_facts(),
        'hemisphere_image_urls': mars_hemi(browser)
    }
    browser.quit()
    return mars_dict

def mars_news(browser):
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    slide = soup.find('li', class_='slide')
    mars_title = slide.find('div', class_='content_title').text
    mars_p = slide.find('div', class_='article_teaser_body').text
    return mars_title, mars_p

def mars_img(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages'
    browser.visit(url)
    img_btn = browser.find_by_id('full_image')
    img_btn.click()
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    html = browser.html
    soup = bs(html, 'html.parser')
    base = 'https://www.jpl.nasa.gov'
    img_url = soup.find('img', class_='main_image')['src']
    featured_image_url = base + img_url
    return featured_image_url

def mars_weather(browser):
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_weather = soup\
        .find('li', class_='stream-item')\
        .find('p', class_='tweet-text').text
    return mars_weather

def mars_facts():
    df= pd.read_html('https://space-facts.com/mars/')[1]
    df.columns = ['fact', 'value']
    df = df.to_html(classes='table table-striped')
    return df

def mars_hemi(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    hemisphere_image_urls=[]
    for i in range(4):
        obj = {}
        btn = browser.find_by_tag('h3')[i]
        btn.click()
        html = browser.html
        soup = bs(html, 'html.parser')
        obj['link'] = soup.find('div', class_='downloads').find('a')['href']
        obj['title'] = soup.find('h2', class_='title').text
        hemisphere_image_urls.append(obj)
        browser.back()
    return hemisphere_image_urls