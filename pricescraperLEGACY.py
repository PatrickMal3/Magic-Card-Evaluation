from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from selenium import webdriver
import re
import pandas as pd

card_data = pd.read_csv('testSet.csv', sep=',')

# start browser
driver = webdriver.Firefox()

# TCGplayer
# URL constants
#url_start = "https://shop.tcgplayer.com/magic/"
#url_middle = "?advancedSearch=true&ProductName="
#url_end = "&Price_Condition=Less+Than"
#
#for index, row in card_data.iterrows():
#    print(row['name'])
#
#    # create name variable
#    card_name = row['name']
#    name_code = re.sub('[^\w\s]', '', card_name)
#    name_code = re.sub('  ', ' ', name_code)
#
#    # create set variable
#    set_name = row['last_set']
#    set_code = re.sub('[^\w\s]', '', set_name)
#    set_code = re.sub('\s', '-', set_code)
#
#    #set url
#    url = url_start + set_code + url_middle + name_code + url_end
#
#    #send driver to url
#    driver.get(url)
#
#    #find the lowest price
#    xpath_element = "/html/body/main/div[3]/div[1]/section[2]/div/div/div[1]/div[2]/dl/dd"
#    lowest_seller = driver.find_elements_by_xpath(xpath_element)
#
#    #print the lowest price
#    if(lowest_seller):
#        print(lowest_seller[0].text)
#    else:
#        print("NaN")


url_start = "https://www.mtggoldfish.com/price/"
url_middle = "/"
url_end = "#paper"

for index, row in card_data.iterrows():
    print(row['name'])

    # create name variable
    card_name = row['name']
    name_code = re.sub('[^\w\s]', '', card_name)
    name_code = re.sub('  ', ' ', name_code)
    name_code = re.sub(' ', '+', name_code)

    # create set variable
    set_name = row['last_set']
    set_code = re.sub('[^\w\s]', '', set_name)
    set_code = re.sub(' ', '+', set_code)

    #set url
    url = url_start + set_code + url_middle + name_code + url_end

    #send driver to url
    driver.get(url)

    #find the lowest price
    xpath_element = "/html/body/main/div[3]/div[1]/div/div[1]/div[1]/div/div/div[2]/div[2]"
    lowest_seller = driver.find_elements_by_xpath(xpath_element)

    #print the lowest price
    if(lowest_seller):
        print(lowest_seller[0].text)

