from urllib.request import urlopen as uReq
import time
import json
import pandas as pd
from selenium import webdriver
import re

#######
# Globals
#######

# card data
card_data = pd.read_csv('newPrices.csv', sep=',')

# URL constants
my_lst = card_data['price'].astype(str)

# start browser
driver = webdriver.Firefox()

#######
# Functions
#######

# scrapes prices from scryfall.com
def scry_scraper(card_id):
    time.sleep(0.1)
    # create scryfall url
    url_start = "https://api.scryfall.com/cards/"
    url = url_start + card_id

    # call scryfall url
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()

    # read price from scryfall json
    page_json = json.loads(page_html)
    price = page_json['prices']['usd']

    return(price)



# prints the process
def process_clock(index, max_index):
    process = round(index / max_index * 100, 4)
    print(index , "/" , max_index, process, "%")

# scrapes prices from tcgplayer.com
def tcg_scraper(card_name, set_name):
    time.sleep(2)

    # URL constants
    url_start = "https://shop.tcgplayer.com/magic/"
    url_middle = "?advancedSearch=true&ProductName="
    url_end = "&Price_Condition=Less+Than"

    # create name variable
    name_code = re.sub('[^\w\s-]', '', card_name)
    name_code = re.sub('  ', ' ', name_code)

    # create set variable
    set_code = re.sub('[^\w\s]', '', set_name)
    set_code = re.sub('\s', '-', set_code)

    # create tcgplayer url
    url = url_start + set_code + url_middle + name_code + url_end

    #send driver to url
    driver.get(url)

    #find the lowest price
    xpath_element = "/html/body/main/div[3]/div[1]/section[2]/div/div/div[1]/div[2]/dl/dd"
    try:
        price = re.sub('\$', '', driver.find_elements_by_xpath(xpath_element)[0].text)
    except:
        price = "Error"

    return(price)



# scrapes prices from cardkingdom.com
def cardkingdom_scraper(card_name):
    time.sleep(2)

    # URL constants
    url_start = "https://www.cardkingdom.com/catalog/search?filter%5Bipp%5D=20&filter%5Bsort%5D=price_asc&filter%5Bname%5D=\"" 
    url_end = "\""

    # create name variable
    name_code = re.sub('[^\w\s-]', '', card_name)
    name_code = re.sub('  ', ' ', name_code)
    name_code = re.sub(' ', '+', name_code)

    # create cardkingdom url
    url = url_start + name_code + url_end

    #send driver to url
    driver.get(url)

    #find the lowest price
    xpath_element = "/html/body/div[4]/div[3]/div[3]/div[2]/div[1]/div[2]/div/ul[2]/li[1]/form/div[1]/span[4]"
    try:
        price = re.sub('\$', '', driver.find_elements_by_xpath(xpath_element)[0].text)
    except:
        price = "Error"

    return(price)

#######
# Main
#######

# main logic
# loop through all rows of dataframe
for index, row in card_data.iterrows():
    # if card has no price yet scrape scryfall
    if not re.match("[\d]{1,20}", my_lst[index]):
        price = scry_scraper(row['id'])
        # if scryfall has no price info, scrape tcgplayer
        if not re.match("[\d]{1,20}", str(price)):
            price = tcg_scraper(row['name'], row['set_name'])
            # if tcgplayer has no price info, scrape cardkingdom
            if not re.match("[\d]{1,20}", price):
                price = cardkingdom_scraper(row['name'])
        # save price in list at index
        my_lst[index] = price
        # print the process clock
        process_clock(index, len(my_lst))
        # save price list in dataframe
        card_data['price'] = my_lst
        # save new dataframe
        card_data.to_csv('newPrices.csv', index = False)
