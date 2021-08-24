#!/usr/bin/env python
# coding: utf-8



from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import re
import pymongo



# Function `scrape` will execute all of scraping code from `mission_to_mars.ipynb`
# Return one Python dictionary containing all of the scraped data. 
def scrape():
    # Set the executable path and initialize the chrome browser in splinter

    executable_path = {'executable_path':r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver"}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_data = {}
    news_output = mars_news(browser)
    mars_data['news_title'] = news_output[0]
    mars_data['news_paragraph'] = news_output[1]
#     mars_data['image'] = mars_image(browser)
    mars_data['facts'] = mars_facts(browser)
    mars_data['hemis'] = mars_hemispheres(browser)
    return mars_data

# Scrapes NASA Mars News Site
# Pulls out latest news title and paragraph description
def mars_news(browser):
    
#Connecting to NASA site
    url_nasa =  "https://redplanetscience.com/"
    browser.visit(url_nasa)

    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    latest_news = soup.findAll('div', class_="content_title")
    news_title = latest_news[1].text

    descriptions = soup.findAll('div', class_= "article_teaser_body")
    news_desc = descriptions[0].text

    news_output = [news_title, news_desc]


    return news_output

# Scrapes JPL Mars Space Image Site 
# Pulls out featured image of Mars
def mars_image(browser_exec):
    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = bs(html, 'html.parser')

    return

# Scrapes Space Facts Site
# Pulls out table with Mars facts and converts the table from Pandas to HTML format
def mars_facts(browser_exec):
    mars_facts = pd.read_html("https://galaxyfacts-mars.com")[0]
    print(mars_facts)
    mars_facts.reset_index(inplace=True)
    mars_facts.columns=["ID", "Properties", "Mars", "Earth"]

    return mars_facts

# Scrapes Astrogeology USGS Site
# Pulls out high resolution images for each of Mar's hemispheres
# Results of image titles and urls are in list of dictionary format
def mars_hemispheres(browser_exec):
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')


    items = soup.find_all('div', class_='item')
    urls = []
    titles = []
    for item in items:
        urls.append(url + item.find('a')['href'])
        titles.append(item.find('h3').text.strip())
    img_urls = []
    for oneurl in urls:
        browser.visit(oneurl)
        html = browser.html
        soup = bs(html, 'html.parser')
    #     savetofile(textfilename,soup.prettify())
        oneurl = url+soup.find('img',class_='wide-image')['src']
        img_urls.append(oneurl)

    hemisphere_image_urls = []

    for i in range(len(titles)):
        hemisphere_image_urls.append({'title':titles[i],'img_url':img_urls[i]})

    return hemisphere_image_urls




