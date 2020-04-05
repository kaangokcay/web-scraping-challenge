from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time
import pandas as pd
import requests as req

def init_browser():
   executable_path = {"executable_path":r"C:/bin/chromedriver"}
   return Browser('chrome', **executable_path, headless=False) 

def scrape():
   browser = init_browser()


   # NASA Mars News

   url = 'https://mars.nasa.gov/news/'
   browser.visit(url)

   time.sleep(1)

   browser_html = browser.html
   news_soup = bs(browser_html, "html.parser")

   slide_element = news_soup.select_one("ul.item_list li.slide")

   news_title = slide_element.find("div", class_="content_title").find("a").text

   news_p = slide_element.find("div", class_="article_teaser_body").text



   # JPL Mars Space Images - Featured Image

   url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
   browser.visit(url)

   time.sleep(1)

   browser.click_link_by_partial_text('FULL IMAGE')
   image_html = browser.html

   image_soup = bs(image_html, "html.parser")
   featured_img_rel = image_soup.select_one(".carousel_item").get("style")
   featured_img_rel = featured_img_rel.split("\'")[1]

   featured_img_url = f'https://www.jpl.nasa.gov{featured_img_rel}'



   # Mars Weather

   twitter_response = req.get('https://twitter.com/marswxreport?lang=en')

   twitter_soup = bs(twitter_response.text, "html.parser")

   tweet_containers = twitter_soup.find_all("div", class_='js-tweet-text-container')

   mars_weather = tweet_containers[0].text



   # Mars Facts

   mars_facts_url = 'https://space-facts.com/mars/'
   
   tables = pd.read_html(mars_facts_url)

   table_one_df = tables[0]

   table_one_df.columns = ["Description", "Value"]

   table_one_df.set_index("Description", inplace=True)

   html_table = table_one_df.to_html()
   html_table = html_table.replace('\n', '')



   # Mars Hemispheres

   hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
   browser.visit(hemi_url)

   time.sleep(1)

   hemi_html = browser.html
   hemi_soup = bs(hemi_html, "html.parser")

   def get_first_url(soup_div):

      title = soup_div.find("h3").text
      image_parent = soup_div.find("div", class_="description")
      image_link_partial = image_parent.find("a")["href"]
      
      return([title, image_link_partial])

   def get_image_url(page_url, browser):

      browser.visit(link)
      time.sleep(1)
      
      image_html = browser.html
      image_soup = bs(image_html, "html.parser")
      full_img_parent = image_soup.select_one("div.wide-image-wrapper div.downloads")
      img_url = full_img_parent.find("a")["href"]
   
      return(img_url)


   results = hemi_soup.select("div.result-list div.item")

   parent_url = 'https://astrogeology.usgs.gov'
   
   titles = []
   img_partials = []
   links = []
   hemisphere_image_urls = []

   for result in results:

      [title, img_partial] = get_first_url(result)
      titles.append(title)
      img_partials.append(img_partial)
      link = 'https://astrogeology.usgs.gov' + img_partial
      img_url = get_image_url(link, browser)
      links.append(link)
      hemi_dict = {"title": title, "img_url": img_url}
      hemisphere_image_urls.append(hemi_dict)


   title_one = hemisphere_image_urls[0]['title']
   title_two = hemisphere_image_urls[1]['title']
   title_three = hemisphere_image_urls[2]['title']
   title_four = hemisphere_image_urls[3]['title']

   image_one = hemisphere_image_urls[0]['img_url']
   image_two = hemisphere_image_urls[1]['img_url']
   image_three = hemisphere_image_urls[2]['img_url']
   image_four = hemisphere_image_urls[3]['img_url']

 
   mars_dictionary = {
      "News_Title": news_title,
      "News_p": news_p,
      "Featured_Image": featured_img_url,
      "Mars_Weather": mars_weather,
      "Mars_Facts": html_table,
      "Title_One": title_one,
      "Title_Two": title_two,
      "Title_Three": title_three,
      "Title_Four": title_four,
      "Image_One": image_one,
      "Image_Two": image_two,
      "Image_Three": image_three,
      "Image_Four": image_four}
   
   return mars_dictionary

