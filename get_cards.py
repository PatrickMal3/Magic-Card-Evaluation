from urllib.request import urlopen as uReq
import urllib.parse
import urllib
import time
import json
import pandas as pd
import re

#######
# Functions
#######

# returns an array of all unique card names
def get_card_names():

    # scryfall url
    url = "https://api.scryfall.com/catalog/card-names"

    # call scryfall url
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()

    # read price from scryfall json
    page_json = json.loads(page_html)
    name_lst = page_json['data']

    return(name_lst)

# returns json data of all printings of a card
def get_printings_info(card_id):
    # scryfall url
    url = "https://api.scryfall.com/cards/search?order=released&q=oracleid%3A" + card_id + "&unique=prints"

    # call scryfall url
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()

    # read json data from scryfall 
    page_json = json.loads(page_html)

    return(page_json)

# returns the lowest paper card price for non oversized cards
def get_price(page_json):

    price_lst = []

    all_printings = page_json['data']

    for printing in all_printings:
        if 'paper' in printing['games'] and printing['oversized'] == False:
            if printing['prices']['usd'] != None:
                try: price_lst.append(float(printing['prices']['usd']))
                except: price_lst.append(float(7777777.77))
            else:
                try: price_lst.append(float(printing['prices']['usd_foil']))
                except: price_lst.append(float(7777777.77))

    try:
        price_lst.sort()
        #print(price_lst)
        return(price_lst[0])
    except:
        return(None)

# returns all printing dates of a card
def get_dates(page_json):

    date_lst = []

    all_printings = page_json['data']

    for printing in all_printings:
        if 'paper' in printing['games']:
            date_lst.append(printing['released_at'])

    return(date_lst)

# retrieves all significant card infos and creates a dict with those infos
def create_card_info(card_name):
    time.sleep(0.1)

    # scryfall url
    url = "https://api.scryfall.com/cards/named?fuzzy=" + urllib.parse.quote(card_name)

    # call scryfall url
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()

    # read json data from scryfall 
    page_json = json.loads(page_html)

    oracle_id = page_json['oracle_id']
    cmc = page_json['cmc']
    try: mana_cost = page_json['mana_cost']
    except: mana_cost = None
    type_line = page_json['type_line']
    layout = page_json['layout']
    try: oracle_text = page_json['oracle_text']
    except: oracle_text = None
    color_id = page_json['color_identity']
    legalities = page_json['legalities']
    is_reserved = page_json['reserved']
    is_reprint = page_json['reprint']
    set_name = page_json['set']
    set_type = page_json['set_type']
    is_booster = page_json['booster']
    rarity = page_json['rarity']
    try: edhrec_rank = page_json['edhrec_rank']
    except: edhrec_rank = None
    try: power = page_json['power']
    except: power = None 
    try: toughness = page_json['toughness']
    except: toughness = None 

    printings_page = get_printings_info(oracle_id)
    dates = get_dates(printings_page)
    try: last_printing = dates[0]
    except: last_printing = None
    try: first_printing = dates[-1]
    except: first_printing = None
    num_printings = len(dates) 
    price = get_price(printings_page)

    card_dict = {'names':[card_name], 
                 'oracle_id':[oracle_id],
                 'cmc':[cmc],
                 'mana_cost':[mana_cost],
                 'type_line':[type_line],
                 'layout':[layout],
                 'oracle_text':[oracle_text],
                 'color_id':[color_id],
                 'legalities':[legalities],
                 'is_reserved':[is_reserved],
                 'is_reprint':[is_reprint],
                 'set_name':[set_name],
                 'set_type':[set_type],
                 'is_booster':[is_booster],
                 'rarity':[rarity],
                 'edhrec_rank':[edhrec_rank],
                 'power':[power],
                 'toughness':[power],
                 'num_printings':[num_printings],
                 'first_printing':[first_printing],
                 'last_printing':[last_printing],
                 'price':[price]}


    card_data = pd.DataFrame(card_dict)
    return(card_data)

#######
# Main
#######

# define the row template
card_data_dict = {'names':[], 
                  'oracle_id':[],
                  'cmc':[],
                  'mana_cost':[],
                  'type_line':[],
                  'layout':[],
                  'oracle_text':[],
                  'color_id':[],
                  'legalities':[],
                  'is_reserved':[],
                  'is_reprint':[],
                  'set_name':[],
                  'set_type':[],
                  'is_booster':[],
                  'rarity':[],
                  'edhrec_rank':[],
                  'power':[],
                  'toughness':[],
                  'num_printings':[],
                  'first_printing':[],
                  'last_printing':[],
                  'price':[]}

# create the initial dataframe out of the row template
card_dataframe = pd.DataFrame(card_data_dict)

# retrieve all unique card names
card_names = []
card_names = get_card_names()

# loop through all card names
# gather all info
# and assamble dataframe
for name in card_names:
    card_info = create_card_info(name)
    card_dataframe = card_dataframe.append(card_info)
    # print dataframe shape as progress info
    # mtg has about 20000 cards
    print(card_dataframe.shape)

# save dataframe to csv file
card_dataframe.to_csv('card_data.csv', index=False)
