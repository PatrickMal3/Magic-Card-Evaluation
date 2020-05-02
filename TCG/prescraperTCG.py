from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from selenium import webdriver
import re
import pandas as pd
import time

card_data = pd.read_csv('missing_prices.csv', sep=',')

# start browser
driver = webdriver.Firefox()

# TCGplayer
# URL constants
url_start = "https://shop.tcgplayer.com/magic/"
url_middle = "?advancedSearch=true&ProductName="
url_end = "&Price_Condition=Less+Than"

# globals
prices_lst = []
my_counter = 0
row_size = card_data.shape[0]

for index, row in card_data.iterrows():
    id_code = row['id']

    # create name variable
    card_name = row['name']
    name_code = re.sub('[^\w\s-]', '', card_name)
    name_code = re.sub('  ', ' ', name_code)

    # create set variable
    set_name = row['last_set']
    set_code = re.sub('[^\w\s]', '', set_name)
    set_code = re.sub('\s', '-', set_code)

    #set url
    url = url_start + set_code + url_middle + name_code + url_end

    #send driver to url
    driver.get(url)

    #find the lowest price
    xpath_element = "/html/body/main/div[3]/div[1]/section[2]/div/div/div[1]/div[2]/dl/dd"
    price = driver.find_elements_by_xpath(xpath_element)
    try:
        prices_lst.append(re.sub('\$', '', price[0].text))
    except:
        prices_lst.append("NaN")

    my_counter = my_counter + 1
    process = round(my_counter / row_size *100, 4)
    print(my_counter , "/" , row_size, process, "%")
    time.sleep(2)

    prices_df = pd.DataFrame({'prices': prices_lst})

    prices_df.to_csv('prices.csv', index=False)
