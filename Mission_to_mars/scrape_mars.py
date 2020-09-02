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


# NASA Mars News (title/para scraping)
def scrape():
    # init_browser
    browser = init_browser()
    # create global dictionary to import into Mongo
    mars_dict = {}

    # URL connect
    url_one = 'https://mars.nasa.gov/news/'
    browser.visit(url_one)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # collect and extract latest news title and paragraph text
    # article = soup.find("div", class_='list_text')
    news = soup.find_all('div', class_='content_title')[0].text
    para = soup.find('div', class_='article_teaser_body')

    # URL connect featured image
    url_two = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_two)
    html = browser.html
    soup_image = BeautifulSoup(html, 'html.parser')
    # collect and extract image
    image_html = soup_image.body
    image_path_two = image_html.find("div", class_='carousel_items')
    featured_image_url = image_path_two.find('article')['style'].\
        replace('background-image:url(','').replace(');','')[23:-1]
    link = 'https://www.jpl.nasa.gov/'

    # dict entry from featured image (scrape 2)
    featured_image = link + featured_image_url 

    # Mars weather (twitter) url connect
    url_three = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_three)
    html = browser.html
    soup_twitter = BeautifulSoup(html, 'html.parser')
    # collect and extract latest tweet
    twitter_html = soup_twitter.body
    mars_w = twitter_html.find('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')
    mars_weather = mars_w.find('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0').text

# Mars Facts (table) url connect
    url_four = 'https://space-facts.com/mars/'
    tables = pd.read_html(url_four)

    # collect and extract table
    data_tables = tables[0]
    data_tables.columns = [0,1]
    data_tables.set_index(0, inplace=True)
    html_data_table = data_tables.to_html()
    html_data_table.replace('\n','')

# Mars Hemispheres (loop) url connect
    url_five = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_five)
    html_five = browser.html
    soup_hem = BeautifulSoup(html_five, 'html.parser')
    
    # collect and extract table
    hemisphere = soup_hem.find_all('div', class_='item')

    image_list = []

    main_link = 'https://astrogeology.usgs.gov/'

    for x in hemisphere:

        img_url = x.find('a', class_='itemLink product-item')['href']
        h3 = x.find('h3').text
        browser.visit(main_link + img_url)
        img_brow = browser.html
        soup_hemispheres = BeautifulSoup(img_brow, 'html.parser')
        url_img_find = main_link + soup_hemispheres.find('img', class_='wide-image')['src']
        image_list.append({"Title of image": h3, "The image URL": url_img_find})

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(image_list)
        
    # global dict
    mars_dict = {
        'news_title': news,
        'news_paragraph': para,
        "featured_image": featured_image,
        "tweet": mars_weather,
        "table": html_data_table,
        "hemispheres": image_list

    }

    browser.quit()
    
    return mars_dict