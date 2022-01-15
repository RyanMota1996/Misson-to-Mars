from winreg import HKEY_LOCAL_MACHINE
import pandas as pd
import datetime as dt
from pandas.io.html import read_html
from splinter import Browser, browser
from bs4 import BeautifulSoup as soup
import selenium
import numpy
from webdriver_manager.chrome import ChromeDriverManager

def scrap_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph= mars_news(browser)
    hemisphere_img_urls=hemisphere(browser)
    data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'Featured image' : featured_image,
        'facts': mars_facts(),
        'hemisphere': hemisphere_img_urls,
        'last_modified': dt.datetime.now()
    }
    browser.quit()
    return data

def mars_news(browser):
   url = 'https://mars.nasa.gov/news/'
   browser.visit(url)
   browser.is_element_present_by_css('ul.item_list li.slide',wait_time=1)
   html=browser.html
   news_soup = soup(html, 'html.parser')
   try:
        slide_elem= news_soup.select_one('ul.item_list li.slide')
        news_title=slide_elem.find('div', class_='content_title').get_text()
        news_p= slide_elem.find('div',class_='article_teaser_body').get_text()
   except AttributeError: 
        return None,None
   return news_title, news_p

def featured_image(browser):
    url= 'https://spaceimages-mars.com/'
    browser.visit(url)
    full_img_elem=browser.find_by_tag('button')[0]
    full_img_elem.click()
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem=browser.links.find_by_partial_text('more info')
    more_info_elem.click()
    html=browser.html
    img_soup=soup(html,'html.parser')
    try:
        img_url_rel = img_soup.select_one('figure.lede a img').get('src')
    except AttributeError:
        return None
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url

def mars_facts():
    try:
        df=pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
    df.columns=['description','value']
    df.set_index('description', inplace=True)
    return df.to_html()
def hemisphere(browser):
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    hemisphere_img_urls = []
    imgs_links= browser.find_by_css("a.product-item h3")

    for x in range(len(imgs_links)):
        hemisphere= {}

        browser.find_by_css('a.product-item h3')[x].click()
        sample_img= browser.links.find_by_text('Sample').first
        hemisphere['img_url']=sample_img['href']
        hemisphere['title']=browser.find_by_css('h2.title').text
        hemisphere_img_urls.append(hemisphere)
        browser.back()
        return hemisphere_img_urls
    
if __name__ == '__main__':
    print("Hello")
    print(scrap_all())