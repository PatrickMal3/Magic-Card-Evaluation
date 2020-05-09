import pandas as pd
import datetime as dt
import numpy as np
import re

#######
# read in Data from scryfall 
#######

# data includes Oracle Texts
scryData = pd.read_csv('newPrices.csv')

# Emergency filter:
filter_name_lst = ['Eutropia the Twice-Favored',
                   'Hero of the Pride']

scryData = scryData[~scryData['name'].isin(filter_name_lst)]

#######
# define new dataframe
#######

lst = []
myData = pd.DataFrame(lst)

#######
# feature creation
#######

#myData['id'] = scryData['id']
myData['name'] = scryData['name']

# break up type line
#myData['type'] = scryData['type_line']

myData['is_legendary'] = scryData['type_line'].str.contains('Legendary', regex = False).astype(int)
myData['is_creature'] = scryData['type_line'].str.contains('Creature', regex = False).astype(int)
myData['is_instant'] = scryData['type_line'].str.contains('Instant', regex = False).astype(int)
myData['is_sorcery'] = scryData['type_line'].str.contains('Sorcery', regex = False).astype(int)
myData['is_land'] = scryData['type_line'].str.contains('Land', regex = False).astype(int)
myData['is_enchantment'] = scryData['type_line'].str.contains('Enchantment', regex = False).astype(int)
myData['is_planeswalker'] = scryData['type_line'].str.contains('Planeswalker', regex = False).astype(int)
myData['is_artifact'] = scryData['type_line'].str.contains('Artifact', regex = False).astype(int)

myData['cmc'] = scryData['cmc']
scryData['released_at'] = pd.to_datetime(scryData['released_at'], errors = 'coerce')
myData['year'] = scryData['released_at'].dt.year
myData['is_id_white'] = scryData['color_identity'].str.contains('W', regex = False).astype(int)
myData['is_id_blue'] = scryData['color_identity'].str.contains('U', regex = False).astype(int)
myData['is_id_black'] = scryData['color_identity'].str.contains('B', regex = False).astype(int)
myData['is_id_red'] = scryData['color_identity'].str.contains('R', regex = False).astype(int)
myData['is_id_green'] = scryData['color_identity'].str.contains('G', regex = False).astype(int)
scryData['legalities'] = scryData['legalities'].astype(str)
myData['is_standard_legal'] = scryData['legalities'].str.contains("'standard': 'legal'", regex = False).astype(int)
myData['is_commander_legal'] = scryData['legalities'].str.contains("'commander': 'legal'", regex = False).astype(int)
myData['is_modern_legal'] = scryData['legalities'].str.contains("'modern': 'legal'", regex = False).astype(int)
myData['is_pioneer_legal'] = scryData['legalities'].str.contains("'pioneer': 'legal'", regex = False).astype(int)
myData['is_legacy_legal'] = scryData['legalities'].str.contains("'legacy': 'legal'", regex = False).astype(int)
myData['is_pauper_legal'] = scryData['legalities'].str.contains("'pauper': 'legal'", regex = False).astype(int)

myData['is_reserved'] = scryData['reserved'].astype(int)
myData['is_reprint'] = scryData['reprint'].astype(int)
#myData['set'] = scryData['set']
#myData['rarity'] = scryData['rarity']
myData['rarity'] = scryData['rarity'].replace({'mythic' : 1,
                                               'rare' : 2,
                                               'uncommon' : 3,
                                               'common' : 4})

##### DANGER some values are FALSE
myData['edhrec_rank'] = scryData['edhrec_rank'].fillna(20000)
scryData['power'] = scryData['power'].str.replace('.\+\*', '*', regex = True)
scryData['power'] = scryData['power'].str.replace('*', '-1', regex = False)
scryData['power'] = scryData['power'].fillna(-2)
myData['power'] = scryData['power']#.replace({'*' : -2})
scryData['toughness'] = scryData['toughness'].str.replace('.\+\*', '*', regex = True)
scryData['toughness'] = scryData['toughness'].str.replace('*', '-1', regex = False)
scryData['toughness'] = scryData['toughness'].fillna(-2)
myData['toughness'] = scryData['toughness']#.replace({'*' : -2})
myData['price'] = scryData['price']

# replace bool values with 1/0


# set type could be interesting
#myData['set_type'] = scryData['set_type']

# oracle text must be put into diegestible data
#myData['oracle_text'] = scryData['oracle_text']

# flavor: Yes / NO
#myData['flavor_text'] = scryData['flavor_text']

# artist could also be interesting
#myData['artist'] = scryData['artist']


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

myData.to_csv('fin_card_data.csv', index=False)
