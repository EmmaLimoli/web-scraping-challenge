# use mongoDB with Flask templating to create new HTML page
# display info in jupyter notebook
# convert jupyter notebook to python script and return python dict containing scraped data

# dependencies
from bs4 import BeautifulSoup
import pandas as pd
import requests
from splinter import Browser
import pymongo 
import pprint

# chromedriver/splinter connection
def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

# create global dictionary to import into Mongo
mars_info_dict = {}

# NASA Mars News (title/para scraping)
def nasa_mars ():
    # init_browser
    browser = init_browser()

    # URL connect
    url_one = 'https://mars.nasa.gov/news/'
    browser.visit(url_one)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # collect and extract latest news title and paragraph text
    article = soup.find("div", class_='list_text')
    news = article.find('div', class_='content_title').text
    para = article.find('div', class_='article_teaser_body').text

    # dict entry from Mars News (scrap 1)
    mars_info_dict['news_title'] = news
    mars_info_dict['news_paragraph'] = para

    return mars_info_dict
    browser.quit()