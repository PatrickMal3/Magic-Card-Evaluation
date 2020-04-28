from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from selenium import webdriver
import re

#url = "https://www.tcgplayer.com/search/magic/product?productLineName=magic&q=sol ring"
url = "https://shop.tcgplayer.com/magic/masters-25?advancedSearch=true&ProductName=lightning+bolt&Price_Condition=Less+Than"
driver = webdriver.Firefox()
driver.get(url)

page_html = driver.page_source
soup_str = str(soup(page_html, 'html.parser'))

lowest_seller = driver.find_elements_by_xpath("/html/body/main/div[3]/div[1]/section[2]/div/div/div[1]/div[2]/dl/dd")

print(lowest_seller[0].text)

#save soup to file
#with open('test.html', 'w') as file:
    #file.write(soup_str)
