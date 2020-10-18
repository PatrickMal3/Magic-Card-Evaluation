import pandas as pd
import datetime as dt
import numpy as np
import re

#######
# create final dataframe from prefiltered scryfall card data
#######

# data includes Oracle Texts
scryData = pd.read_csv('2020_09_25_data_processed/filtered_card_data.csv')

#######
# define new dataframe
#######

lst = []
myData = pd.DataFrame(lst)

#######
# feature creation
#######

myData['name'] = scryData['names']

# break up type line
myData['is_legendary'] = scryData['type_line'].str.contains('Legendary', regex = False).astype(int)
myData['is_creature'] = scryData['type_line'].str.contains('Creature', regex = False).astype(int)
myData['is_instant'] = scryData['type_line'].str.contains('Instant', regex = False).astype(int)
myData['is_sorcery'] = scryData['type_line'].str.contains('Sorcery', regex = False).astype(int)
myData['is_land'] = scryData['type_line'].str.contains('Land', regex = False).astype(int)
myData['is_enchantment'] = scryData['type_line'].str.contains('Enchantment', regex = False).astype(int)
myData['is_planeswalker'] = scryData['type_line'].str.contains('Planeswalker', regex = False).astype(int)
myData['is_artifact'] = scryData['type_line'].str.contains('Artifact', regex = False).astype(int)

# CMC
myData['cmc'] = scryData['cmc']

# printings
scryData['first_printing'] = pd.to_datetime(scryData['first_printing'], errors = 'coerce')
myData['first_printing'] = scryData['first_printing'].dt.year
scryData['last_printing'] = pd.to_datetime(scryData['last_printing'], errors = 'coerce')
myData['last_printing'] = scryData['last_printing'].dt.year
myData['num_printings'] = scryData['num_printings']

# color id
myData['is_id_white'] = scryData['color_id'].str.contains('W', regex = False).astype(int)
myData['is_id_blue'] = scryData['color_id'].str.contains('U', regex = False).astype(int)
myData['is_id_black'] = scryData['color_id'].str.contains('B', regex = False).astype(int)
myData['is_id_red'] = scryData['color_id'].str.contains('R', regex = False).astype(int)
myData['is_id_green'] = scryData['color_id'].str.contains('G', regex = False).astype(int)

# legalities
scryData['legalities'] = scryData['legalities'].astype(str)
myData['is_standard_legal'] = scryData['legalities'].str.contains("'standard': 'legal'", regex = False).astype(int)
myData['is_commander_legal'] = scryData['legalities'].str.contains("'commander': 'legal'", regex = False).astype(int)
myData['is_modern_legal'] = scryData['legalities'].str.contains("'modern': 'legal'", regex = False).astype(int)
myData['is_pioneer_legal'] = scryData['legalities'].str.contains("'pioneer': 'legal'", regex = False).astype(int)
myData['is_legacy_legal'] = scryData['legalities'].str.contains("'legacy': 'legal'", regex = False).astype(int)
myData['is_pauper_legal'] = scryData['legalities'].str.contains("'pauper': 'legal'", regex = False).astype(int)

# reserved
myData['is_reserved'] = scryData['is_reserved'].astype(int)

# reprint
myData['is_reprint'] = scryData['is_reprint'].astype(int)

# set
#myData['set'] = scryData['set']

# rarity
myData['rarity'] = scryData['rarity'].replace({'mythic' : 1,
                                               'rare' : 2,
                                               'uncommon' : 3,
                                               'common' : 4})

##### DANGER some values are FALSE
# edhrec rank
myData['edhrec_rank'] = scryData['edhrec_rank'].fillna(20000)

# power and toughness
scryData['power'] = scryData['power'].str.replace('.\+\*', '*', regex = True)
scryData['power'] = scryData['power'].str.replace('*', '-3', regex = False)
scryData['power'] = scryData['power'].fillna(-5)
myData['power'] = scryData['power']#.replace({'*' : -2})
scryData['toughness'] = scryData['toughness'].str.replace('.\+\*', '*', regex = True)
scryData['toughness'] = scryData['toughness'].str.replace('*', '-3', regex = False)
scryData['toughness'] = scryData['toughness'].fillna(-5)
myData['toughness'] = scryData['toughness']#.replace({'*' : -2})



# set type could be interesting
myData['set_enum'] = scryData['set_type'].replace({'core' : 1,
                                               'expansion' : 2,
                                               'commander' : 3,
                                               'masters' : 4,
                                               'starter' : 5,
                                               'duel_deck' : 6,
                                               'draft_innovation' : 7,
                                               'box' : 8,
                                               'memorabilia' : 9,
                                               'treasure_chest' : 10,
                                               'promo' : 11})

#myData['is_core'] = scryData['set_type'].str.contains('core', regex = False).astype(int)
#myData['is_expansion'] = scryData['set_type'].str.contains('expansion', regex = False).astype(int)
myData['is_masters'] = scryData['set_type'].str.contains('masters', regex = False).astype(int)
#myData['is_starter'] = scryData['set_type'].str.contains('starter', regex = False).astype(int)
#myData['is_duel_deck'] = scryData['set_type'].str.contains('duel_deck', regex = False).astype(int)
#myData['is_draft_innovation'] = scryData['set_type'].str.contains('draft_innovation', regex = False).astype(int)
#myData['is_box'] = scryData['set_type'].str.contains('box', regex = False).astype(int)
#myData['is_memorobilia'] = scryData['set_type'].str.contains('memorobilia', regex = False).astype(int)
#myData['is_treasure_chest'] = scryData['set_type'].str.contains('treasure_chest', regex = False).astype(int)
#myData['is_promo'] = scryData['set_type'].str.contains('promo', regex = False).astype(int)

# in booster
myData['is_booster'] = scryData['is_booster']

# oracle text must be put into diegestible data
myData['oracle_text'] = scryData['oracle_text']
myData['oracle_text'] = myData['oracle_text'].fillna('no text')

# oracle lenght >>> could be interesting
myData['oracle_len'] = scryData['oracle_text'].str.len()
myData['oracle_len'] = myData['oracle_len'].fillna(0)

# flavor: Yes / NO
#myData['flavor_text'] = scryData['flavor_text']

# artist could also be interesting
#myData['artist'] = scryData['artist']


# price
myData['price'] = scryData['price']

########
# create Bulk variable
########
myData['exp'] = [1 if price >= 1 else 0 for price in scryData['price']]


#######
# basic infos
#######

print(scryData.info(verbose = True))
print(' ')
print(myData.info(verbose = True))
print(myData.isnull().sum())
print(' ')
print(scryData.shape)


#######
# save cleaned dataframe to csv
#######

myData.to_csv('2020_09_25_data_processed/fin_card_data.csv', index=False)
