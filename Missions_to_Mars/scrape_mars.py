from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:\Windows\System32\chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# Scrape Mars News
def scrape_marsnews():
    browser = init_browser()

    # Visit mars.nasa.gov
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    # Parse page using Beautiful Soup

    html = browser.html
    soup = bs(html, "html.parser")

    # Get the news title
    news_one=soup.select_one("ul.item_list li.slide")
    news_title = news_one.find('div', class_='content_title').get_text()

    # Get the new details
    news_parag = soup.find('div', class_='article_teaser_body').text

    # Close the browser after scraping
    browser.quit()

    # Return results
    return [news_title,news_parag]
# Scrape Mars Images
def scrape_marsimage():
    browser = init_browser()

    # Visit jpl.nasa.gov
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    #base_url="https://www.jpl.nasa.gov/"
    browser.visit(url)

    time.sleep(1)

    # Parse page using Beautiful Soup

    html = browser.html
    soup = bs(html, "html.parser")

    # Get the image url
    more_info_url=browser.find_by_id("full_image").click()
    browser.is_element_present_by_text('more info',wait_time=1)
    full_image_button=browser.links.find_by_partial_text('more info')
    full_image_button.click()
   
    html=browser.html
    soup = bs(html, "html.parser")
    image_url=soup.select_one('figure.lede a img').get('src')

    #Featured_image_url=f'{base_url}{image_url}'
    Featured_image_url = f'https://www.jpl.nasa.gov/{image_url}'

    # Close the browser after scraping
    browser.quit()

    # Return results
    return Featured_image_url
# Scrape Mars Facts
def scrape_marsfacts():
    browser = init_browser()

    # Visit space facts url
    url = "https://space-facts.com/mars/"
    browser.visit(url)

    time.sleep(1)

    # Parse page using Beautiful Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Read the table of contents
    table_read=pd.read_html(url)
    marsfact = table_read[0]
    marsfact.columns=['Description','Values']
    marsfact_dict=marsfact.to_dict('records')
    # Close the browser after scraping
    browser.quit()

    # Return results
    return marsfact_dict
# Scrape Mars Hemisphere
def scrape_marshemispheres():
    browser = init_browser()

    # Visit astrogeology url
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

   # time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    
    hemisphere_images_url=[]
    
    for x in range(4):
        browser.find_by_tag('h3')[x].click()
        html = browser.html
        soup = bs(html, "html.parser")

        images=soup.find('img',class_='wide-image')['src']
        image_url=f'https://astrogeology.usgs.gov/{images}'
        title=soup.find('h2').text
        browser.back()
        hemisphere_images_url.append({"title": title, "img_url":image_url })
    browser.quit()
    return hemisphere_images_url
