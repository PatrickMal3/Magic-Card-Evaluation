import pandas as pd
import datetime as dt
import re

#######
# read in Data from scryfall 
#######

# data includes Oracle Texts
scryData = pd.read_json('scryfall-oracle-cards.json')

#######
# feature filtering
#######

# layouts to filter out
#### transform might be interesting!!!
filter_layout_lst = ['art_series', 'augment', 'double_faced_token', 'emblem',
            'host', 'planar', 'scheme', 'token', 'transform', 'vanguard']

scryData = scryData[~scryData['layout'].isin(filter_layout_lst)]

# filter corrupted and special
filter_names_lst = ['Shu General', 'Ancient Spider', 'Longbow Archer',
                    'Livonya Silone', 'Garruk the Slayer',
                    'Noxious Hydra Breath', 'Tel-Jilad Archers',
                    'Bayou Dragonfly', 'Zhang Fei, Fierce Warrior',
                    'Lu Bu, Master-at-Arms', 'Sol, Advocate Eternal']

scryData = scryData[~scryData['name'].isin(filter_names_lst)]

# filter sets
filter_set_lst = ['unh', 'ust', 'und', 'ugl']
scryData = scryData[~scryData['set'].isin(filter_set_lst)]

#######
# define new dataframe
#######

lst = []
myData = pd.DataFrame(lst)

#######
# feature creation
#######

myData['id'] = scryData['id']
myData['name'] = scryData['name']
myData['type'] = scryData['type_line']
myData['cmc'] = scryData['cmc']
#myData['mana_cost'] = scryData['mana_cost']
myData['year'] = scryData['released_at'].dt.year
#myData['colors'] = scryData['colors']
#myData['c_white'] = scryData['colors'].str.contains('W', regex = False)
#myData['c_blue'] = scryData['colors'].str.contains('U', regex = False)
#myData['c_black'] = scryData['colors'].str.contains('B', regex = False)
#myData['c_red'] = scryData['colors'].str.contains('R', regex = False)
#myData['c_green'] = scryData['colors'].str.contains('G', regex = False)
myData['id_white'] = scryData['color_identity'].str.contains('W', regex = False)
myData['id_blue'] = scryData['color_identity'].str.contains('U', regex = False)
myData['id_black'] = scryData['color_identity'].str.contains('B', regex = False)
myData['id_red'] = scryData['color_identity'].str.contains('R', regex = False)
myData['id_green'] = scryData['color_identity'].str.contains('G', regex = False)

scryData['legalities'] = scryData['legalities'].astype(str)
myData['standard_legal'] = scryData['legalities'].str.contains("'standard': 'legal'",
                                                               regex = False)
myData['commander_legal'] = scryData['legalities'].str.contains("'commander': 'legal'",
                                                               regex = False)
myData['modern_legal'] = scryData['legalities'].str.contains("'modern': 'legal'",
                                                               regex = False)
myData['pioneer_legal'] = scryData['legalities'].str.contains("'pioneer': 'legal'",
                                                               regex = False)
myData['legacy_legal'] = scryData['legalities'].str.contains("'legacy': 'legal'",
                                                               regex = False)
myData['pauper_legal'] = scryData['legalities'].str.contains("'pauper': 'legal'",
                                                               regex = False)

myData['reserved'] = scryData['reserved']
myData['reprint'] = scryData['reprint']
#myData['set'] = scryData['set']
#myData['set_type'] = scryData['set_type']
myData['rarity'] = scryData['rarity']
#myData['flavor_text'] = scryData['flavor_text']
#myData['artist'] = scryData['artist']
myData['edhrec_rank'] = scryData['edhrec_rank']
myData['edhrec_rank'] = scryData['edhrec_rank'].fillna(20000)
myData['power'] = scryData['power']
myData['power'] = scryData['power'].fillna(-1)
myData['toughness'] = scryData['toughness']
myData['toughness'] = scryData['toughness'].fillna(-1)
myData['last_set'] = scryData['set_name']


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

myData.to_csv('new.csv', index=False)
scryData.to_csv('old.csv', index=False)

#######
# legacy
#######

# find color cost!!!!
#myString = '{4}{W}{B}{B}{R/G}{2/U}'
#x = re.findall('{B}', myString)
#print(len(x))
#x = re.findall('{R/G}', myString)
#print(len(x))
#x = re.findall('[0-9]}', myString)
#x = re.findall('[0-9]', x[0])
#print(x[0])
