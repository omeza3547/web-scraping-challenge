from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd
import pymongo
import requests

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # NASA Mars News

    url= "https://mars.nasa.gov/news/"
    browser.visit(url)
    html= browser.html
    soup= BeautifulSoup(html,"html.parser")

    latest_news_title= soup.find("div", class_="bottom_gradient").find("h3").text
    p_text= soup.find("div", class_= "article_teaser_body").text


    # JPL Mars Space Images

    img_url= "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_url)
    time.sleep(5)
    img_html= browser.html
    i_soup= BeautifulSoup(img_html,"html.parser")
    img_path= i_soup.find("article", class_= "carousel_item")\
    ["style"].replace("background-image: url(","").replace(");", "")[1:-1]
    mars_url= "https://www.jpl.nasa.gov"
    featured_image_url= mars_url+img_path

    # Mars Weather

    w_url= "https://twitter.com/marswxreport?lang=en"
    browser.visit(w_url)
    time.sleep(5)
    html= browser.html
    soup= BeautifulSoup(html, "html.parser")
    mars_weather = (soup.find('div', attrs={"data-testid": "tweet"}).get_text()).split('InSight ')[1]
    

    # Mars Facts

    f_url= "https://space-facts.com/mars/"
    browser.visit(f_url)
    time.sleep(5)
    m_facts= pd.read_html(f_url)
    mars_df= m_facts[0]
    mars_facts= mars_df.rename(columns={0: "Aspect", 1: "Detail"}).set_index("Aspect")
    mars_df_table= mars_facts.to_html()
    mars_df_table.replace("\n","")    

    # Mars Hemispheres

    h_url= "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(h_url)
    time.sleep(5)
    h_html= browser.html
    soup= BeautifulSoup(h_html, "html.parser")

    h_images= soup.find("div", class_= "collapsible results")
    hems= h_images.find_all("a")

    hems_list= []

    for hemisphere in hems:
        if hemisphere.h3:
            title=hemisphere.h3.text
            link=hemisphere["href"]
            home_url="https://astrogeology.usgs.gov/"
            next_url=home_url+link
            browser.visit(next_url)
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            hemisphere2=soup.find("div",class_= "downloads")
            img=hemisphere2.ul.a["href"]
            hemisphere_dict={}
            hemisphere_dict["Title"]=title
            hemisphere_dict["Image_URL"]=img
            hems_list.append(hemisphere_dict)
            browser.back()

    hems_list

    Mars_info={
        "Mars_news_title": latest_news_title,
        "Mars_news_text": p_text,
        "Mars_featured_img": featured_image_url,
        "Mars_weather": mars_weather,
        "Mars_facts": mars_df_table,
        "Mars_hemispheres": hems_list
    }

    browser.quit()

    return Mars_info

# if __name__ == "__main__":
#     data = scrape()
#     print(data)