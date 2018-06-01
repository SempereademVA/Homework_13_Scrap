

```python
# Dependencies
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from splinter import Browser
import time
import pandas as pd

###########################################
#Initialize browser
def init_browser():
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)
###########################################

scrape_dict ={}   #This dictionary will hold the required screaped data
```

# NASA Mars News


```python
#Scrape the data using selenium since the web page source does not contain the latest news.
#The latest news in generated by a script then rendered by the browser.
#Selenium can read the content that is being rendered.

driver = webdriver.Chrome()
driver.get('https://mars.nasa.gov/news/')


content = driver.find_element_by_class_name('content_title')
news_title = content.text


content = driver.find_element_by_class_name('article_teaser_body')
news_p = content.text


scrape_dict = {'News Title': news_title, 'News Summary': news_p}
```


```python
scrape_dict
```




    {'News Summary': 'The spacecraft has completed its first trajectory correction maneuver.',
     'News Title': 'InSight Steers Toward Mars'}



# NASA Mars Weather


```python
#Scrape the data using Beautiful Soup library

browser = init_browser()
url = "https://twitter.com/marswxreport?lang=en"
browser.visit(url)
html = browser.html


# Create a Beautiful Soup object
soup = bs(html, 'html.parser')


mars_weather = soup.body.find('p', {'class': "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"}).text

```


```python
scrape_dict['Weather'] = mars_weather
```


```python
scrape_dict
```




    {'News Summary': 'The spacecraft has completed its first trajectory correction maneuver.',
     'News Title': 'InSight Steers Toward Mars',
     'Weather': 'Sol 2058 (May 21, 2018), Sunny, high 4C/39F, low -71C/-95F, pressure at 7.43 hPa, daylight 05:20-17:20'}



# JPL Mars Space Images


```python
browser = init_browser()

url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

browser.click_link_by_partial_text('FULL IMAGE')
time.sleep(10)

html = browser.html

soup = bs(html, 'html.parser')

images = soup.findAll('img')

image_list =[]
for image in images:

    if 'mediumsize' in image['src']:
        print (image['src'])
        featured_image = image['src']
        image_list.append(image['src'])



featured_image_url = 'https://www.jpl.nasa.gov/spaceimages' + featured_image

```

    /spaceimages/images/mediumsize/PIA18297_ip.jpg
    /spaceimages/images/mediumsize/PIA18297_ip.jpg
    


```python
scrape_dict['Featured Image'] = featured_image_url
```


```python
scrape_dict
```




    {'Featured Image': 'https://www.jpl.nasa.gov/spaceimages/spaceimages/images/mediumsize/PIA18297_ip.jpg',
     'News Summary': 'The spacecraft has completed its first trajectory correction maneuver.',
     'News Title': 'InSight Steers Toward Mars',
     'Weather': 'Sol 2058 (May 21, 2018), Sunny, high 4C/39F, low -71C/-95F, pressure at 7.43 hPa, daylight 05:20-17:20'}



# Mars Facts


```python
url = 'https://space-facts.com/mars/'

tables = pd.read_html(url)
tables
```




    [                      0                              1
     0  Equatorial Diameter:                       6,792 km
     1       Polar Diameter:                       6,752 km
     2                 Mass:  6.42 x 10^23 kg (10.7% Earth)
     3                Moons:            2 (Phobos & Deimos)
     4       Orbit Distance:       227,943,824 km (1.52 AU)
     5         Orbit Period:           687 days (1.9 years)
     6  Surface Temperature:                  -153 to 20 °C
     7         First Record:              2nd millennium BC
     8          Recorded By:           Egyptian astronomers]




```python
tables[0]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Equatorial Diameter:</td>
      <td>6,792 km</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Polar Diameter:</td>
      <td>6,752 km</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Mass:</td>
      <td>6.42 x 10^23 kg (10.7% Earth)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Moons:</td>
      <td>2 (Phobos &amp; Deimos)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Orbit Distance:</td>
      <td>227,943,824 km (1.52 AU)</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Orbit Period:</td>
      <td>687 days (1.9 years)</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Surface Temperature:</td>
      <td>-153 to 20 °C</td>
    </tr>
    <tr>
      <th>7</th>
      <td>First Record:</td>
      <td>2nd millennium BC</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Recorded By:</td>
      <td>Egyptian astronomers</td>
    </tr>
  </tbody>
</table>
</div>




```python
df = tables[0]
df.columns = ['Parameter', 'Value']
df.head(9)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Parameter</th>
      <th>Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Equatorial Diameter:</td>
      <td>6,792 km</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Polar Diameter:</td>
      <td>6,752 km</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Mass:</td>
      <td>6.42 x 10^23 kg (10.7% Earth)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Moons:</td>
      <td>2 (Phobos &amp; Deimos)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Orbit Distance:</td>
      <td>227,943,824 km (1.52 AU)</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Orbit Period:</td>
      <td>687 days (1.9 years)</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Surface Temperature:</td>
      <td>-153 to 20 °C</td>
    </tr>
    <tr>
      <th>7</th>
      <td>First Record:</td>
      <td>2nd millennium BC</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Recorded By:</td>
      <td>Egyptian astronomers</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.set_index('Parameter', inplace=True)
df.head(9)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Value</th>
    </tr>
    <tr>
      <th>Parameter</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Equatorial Diameter:</th>
      <td>6,792 km</td>
    </tr>
    <tr>
      <th>Polar Diameter:</th>
      <td>6,752 km</td>
    </tr>
    <tr>
      <th>Mass:</th>
      <td>6.42 x 10^23 kg (10.7% Earth)</td>
    </tr>
    <tr>
      <th>Moons:</th>
      <td>2 (Phobos &amp; Deimos)</td>
    </tr>
    <tr>
      <th>Orbit Distance:</th>
      <td>227,943,824 km (1.52 AU)</td>
    </tr>
    <tr>
      <th>Orbit Period:</th>
      <td>687 days (1.9 years)</td>
    </tr>
    <tr>
      <th>Surface Temperature:</th>
      <td>-153 to 20 °C</td>
    </tr>
    <tr>
      <th>First Record:</th>
      <td>2nd millennium BC</td>
    </tr>
    <tr>
      <th>Recorded By:</th>
      <td>Egyptian astronomers</td>
    </tr>
  </tbody>
</table>
</div>




```python
html_table = df.to_html()
html_table
```




    '<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th>Value</th>\n    </tr>\n    <tr>\n      <th>Parameter</th>\n      <th></th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>Equatorial Diameter:</th>\n      <td>6,792 km</td>\n    </tr>\n    <tr>\n      <th>Polar Diameter:</th>\n      <td>6,752 km</td>\n    </tr>\n    <tr>\n      <th>Mass:</th>\n      <td>6.42 x 10^23 kg (10.7% Earth)</td>\n    </tr>\n    <tr>\n      <th>Moons:</th>\n      <td>2 (Phobos &amp; Deimos)</td>\n    </tr>\n    <tr>\n      <th>Orbit Distance:</th>\n      <td>227,943,824 km (1.52 AU)</td>\n    </tr>\n    <tr>\n      <th>Orbit Period:</th>\n      <td>687 days (1.9 years)</td>\n    </tr>\n    <tr>\n      <th>Surface Temperature:</th>\n      <td>-153 to 20 °C</td>\n    </tr>\n    <tr>\n      <th>First Record:</th>\n      <td>2nd millennium BC</td>\n    </tr>\n    <tr>\n      <th>Recorded By:</th>\n      <td>Egyptian astronomers</td>\n    </tr>\n  </tbody>\n</table>'




```python
html_table.replace('\n', '')
```




    '<table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th></th>      <th>Value</th>    </tr>    <tr>      <th>Parameter</th>      <th></th>    </tr>  </thead>  <tbody>    <tr>      <th>Equatorial Diameter:</th>      <td>6,792 km</td>    </tr>    <tr>      <th>Polar Diameter:</th>      <td>6,752 km</td>    </tr>    <tr>      <th>Mass:</th>      <td>6.42 x 10^23 kg (10.7% Earth)</td>    </tr>    <tr>      <th>Moons:</th>      <td>2 (Phobos &amp; Deimos)</td>    </tr>    <tr>      <th>Orbit Distance:</th>      <td>227,943,824 km (1.52 AU)</td>    </tr>    <tr>      <th>Orbit Period:</th>      <td>687 days (1.9 years)</td>    </tr>    <tr>      <th>Surface Temperature:</th>      <td>-153 to 20 °C</td>    </tr>    <tr>      <th>First Record:</th>      <td>2nd millennium BC</td>    </tr>    <tr>      <th>Recorded By:</th>      <td>Egyptian astronomers</td>    </tr>  </tbody></table>'




```python
df.to_html('mars_table.html')
```

# Mars Hemispheres


```python
browser = init_browser()
```


```python
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

html = browser.html
soup = bs(html, 'html.parser')
```


```python
images = soup.findAll('h3')
```


```python
images[0].text
```




    'Cerberus Hemisphere Enhanced'




```python
images
```




    [<h3>Cerberus Hemisphere Enhanced</h3>,
     <h3>Schiaparelli Hemisphere Enhanced</h3>,
     <h3>Syrtis Major Hemisphere Enhanced</h3>,
     <h3>Valles Marineris Hemisphere Enhanced</h3>]




```python
hemisphere_image_list = []
for image in images:
     hemisphere_image_list.append(image.text)
```


```python
hemisphere_image_list
```




    ['Cerberus Hemisphere Enhanced',
     'Schiaparelli Hemisphere Enhanced',
     'Syrtis Major Hemisphere Enhanced',
     'Valles Marineris Hemisphere Enhanced']




```python
images_url = soup.findAll('a', {'class': "itemLink product-item"}, href=True)
```


```python
images_url
```




    [<a class="itemLink product-item" href="/search/map/Mars/Viking/cerberus_enhanced"><img alt="Cerberus Hemisphere Enhanced thumbnail" class="thumb" src="/cache/images/dfaf3849e74bf973b59eb50dab52b583_cerberus_enhanced.tif_thumb.png"/></a>,
     <a class="itemLink product-item" href="/search/map/Mars/Viking/cerberus_enhanced"><h3>Cerberus Hemisphere Enhanced</h3></a>,
     <a class="itemLink product-item" href="/search/map/Mars/Viking/schiaparelli_enhanced"><img alt="Schiaparelli Hemisphere Enhanced thumbnail" class="thumb" src="/cache/images/7677c0a006b83871b5a2f66985ab5857_schiaparelli_enhanced.tif_thumb.png"/></a>,
     <a class="itemLink product-item" href="/search/map/Mars/Viking/schiaparelli_enhanced"><h3>Schiaparelli Hemisphere Enhanced</h3></a>,
     <a class="itemLink product-item" href="/search/map/Mars/Viking/syrtis_major_enhanced"><img alt="Syrtis Major Hemisphere Enhanced thumbnail" class="thumb" src="/cache/images/aae41197e40d6d4f3ea557f8cfe51d15_syrtis_major_enhanced.tif_thumb.png"/></a>,
     <a class="itemLink product-item" href="/search/map/Mars/Viking/syrtis_major_enhanced"><h3>Syrtis Major Hemisphere Enhanced</h3></a>,
     <a class="itemLink product-item" href="/search/map/Mars/Viking/valles_marineris_enhanced"><img alt="Valles Marineris Hemisphere Enhanced thumbnail" class="thumb" src="/cache/images/04085d99ec3713883a9a57f42be9c725_valles_marineris_enhanced.tif_thumb.png"/></a>,
     <a class="itemLink product-item" href="/search/map/Mars/Viking/valles_marineris_enhanced"><h3>Valles Marineris Hemisphere Enhanced</h3></a>]




```python
browser = init_browser()

#url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
#browser.visit(url)
```


```python
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
```


```python
image_url_list        
    
    
    
```




    ['href="http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"',
     'href="http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"',
     'href="http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"',
     'href="http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"']




```python
#Clean up the hyper links
clean_url_list = []
for i in range(len(image_url_list)):
    old=image_url_list[i]
    removed_href = old.replace("href=", "")
    remove_quote = removed_href.replace('"', "")
    clean_url_list.append(remove_quote)
    
```


```python
clean_url_list
```




    ['http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg',
     'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg',
     'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg',
     'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg']




```python
#Make the list of dictionaries

image_dictionary_list = []
temp_dict = {}
for i in range(len(hemisphere_image_list)):
    temp_dict = {'title': hemisphere_image_list[i],'img_url': clean_url_list[i]}
    image_dictionary_list.append(temp_dict)
        
```


```python
image_dictionary_list
```




    [{'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg',
      'title': 'Cerberus Hemisphere Enhanced'},
     {'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg',
      'title': 'Schiaparelli Hemisphere Enhanced'},
     {'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg',
      'title': 'Syrtis Major Hemisphere Enhanced'},
     {'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg',
      'title': 'Valles Marineris Hemisphere Enhanced'}]




```python
scrape_dict['Hemispheres'] = image_dictionary_list
```


```python
scrape_dict
```




    {'Featured Image': 'https://www.jpl.nasa.gov/spaceimages/spaceimages/images/mediumsize/PIA18297_ip.jpg',
     'Hemispheres': [{'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg',
       'title': 'Cerberus Hemisphere Enhanced'},
      {'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg',
       'title': 'Schiaparelli Hemisphere Enhanced'},
      {'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg',
       'title': 'Syrtis Major Hemisphere Enhanced'},
      {'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg',
       'title': 'Valles Marineris Hemisphere Enhanced'}],
     'News Summary': 'The spacecraft has completed its first trajectory correction maneuver.',
     'News Title': 'InSight Steers Toward Mars',
     'Weather': 'Sol 2058 (May 21, 2018), Sunny, high 4C/39F, low -71C/-95F, pressure at 7.43 hPa, daylight 05:20-17:20'}




```python
###########################################################
```