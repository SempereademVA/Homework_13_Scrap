
# coding: utf-8


# Dependencies
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from splinter import Browser
import time
import pandas as pd
import pprint
from datetime import datetime



scrape_dict ={}   #This dictionary will hold the required scraped data


###############################################################

#Initialize browser
def init_browser():
    print("#################Init Browser######################")
    executable_path = {'executable_path': r'C:\Users\Marc\Desktop\GW Class\Test_Server\chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

###############################################################

# Function to scrape Mars Information

def scrape_mars():
    #<----------------------------- Scrape NASA Mars News ---------------------------->

    #Scrape the data using selenium since the web page source does not contain the latest news.
    #The latest news in generated by a script then rendered by the browser.
    #Selenium can read the content that is being rendered.

    driver = webdriver.Chrome(r'C:\Users\Marc\Desktop\GW Class\Test_Server\chromedriver')

    driver.get('https://mars.nasa.gov/news/')

    #Let the web page have time to download
    time.sleep(10)

    content = driver.find_element_by_class_name('content_title')
    news_title = content.text

    content = driver.find_element_by_class_name('article_teaser_body')
    news_p = content.text

    scrape_dict = {'NewsTitle': news_title, 'News_Summary': news_p}


    #<----------------------------- Scrape NASA Mars Weather ---------------------------->


    #Scrape the data using Beautiful Soup library

    browser = init_browser()
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html

    # Create a Beautiful Soup object
    soup = bs(html, 'html.parser')

    #Let the web page have time to download
    time.sleep(10)

    mars_weather = soup.body.find('p', {'class': "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"}).text

    scrape_dict['Weather'] = mars_weather

    #<----------------------------- Scrape JPL Mars Space Images ---------------------------->

    browser = init_browser()

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)


    browser.click_link_by_partial_text('FULL IMAGE')
    #Let the web page have time to download
    time.sleep(10)

    #Ready to read the page contents
    html = browser.html

    soup = bs(html, 'html.parser')

    images = soup.findAll('img')

    image_list =[]
    for image in images:
        if 'mediumsize' in image['src']:
            featured_image = image['src']
            image_list.append(image['src'])

    #There is really one featured image that is repeated so just pull out the featured_imge.  No need for the list

    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image

    scrape_dict['FeaturedImage'] = featured_image_url


    #<----------------------------- Scrape Mars Facts ---------------------------->

    url = 'https://space-facts.com/mars/'

    tables = pd.read_html(url)

    #Let the web page have time to download
    time.sleep(10)

    df = tables[0]
    df.columns = ['Parameter', 'Value']

    df.set_index('Parameter', inplace=True)

    html_table = df.to_html()

    html_table.replace('\n', '')

    df.to_html('mars_table.html')


    #<----------------------------- Scrape Mars Hemispheres  ---------------------------->

    browser = init_browser()

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    #Let the web page have time to download
    time.sleep(10)

    images = soup.findAll('h3')

    #Create list of hemisphere names
    hemisphere_image_list = []
    for image in images:
        hemisphere_image_list.append(image.text)

    #Create list of image urls
    images_url = soup.findAll('a', {'class': "itemLink product-item"}, href=True)
    browser = init_browser()


    image_url_list =[]
    for hemisphere in hemisphere_image_list:
        
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        
        browser.click_link_by_partial_text(hemisphere)
        time.sleep(10)
        html = browser.html
        soup = bs(html, 'html.parser')
        
        full_images_url = soup.findAll('a', {'target': "_blank"}, href=True)
        
        x=full_images_url[0]
        x=str(x)
        words = x.split(' ')
        image_url_list.append(words[1])

    #Clean up the hyper links
    clean_url_list = []
    for i in range(len(image_url_list)):
        old=image_url_list[i]
        removed_href = old.replace("href=", "")
        remove_quote = removed_href.replace('"', "")
        clean_url_list.append(remove_quote)
        print("The clean URL is ")
        print(clean_url_list[i])
        

    #Make the list of dictionaries

    image_dictionary_list = []
    temp_dict = {}
    for i in range(len(hemisphere_image_list)):
        temp_dict = {'title': hemisphere_image_list[i],'img_url': clean_url_list[i]}
        image_dictionary_list.append(temp_dict)
            

    scrape_dict['Hemispheres'] = image_dictionary_list

   
    print()
    print('Scrape Mars Done!')
    print('Here is the data')
    print()

    for k,v in scrape_dict.items():
        print(k + ': ', v)
    return scrape_dict
    print()