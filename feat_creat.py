import pandas as pd
import datetime as dt
import re

#######
# read in Data from scryfall 
#######

# data includes Oracle Texts
scryData = pd.read_json('scryfall-oracle-cards.json')

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
myData['year'] = scryData['released_at'].dt.year
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
myData['set'] = scryData['set']
#myData['set_type'] = scryData['set_type']
myData['rarity'] = scryData['rarity']
#myData['flavor_text'] = scryData['flavor_text']
#myData['artist'] = scryData['artist']
myData['edhrec_rank'] = scryData['edhrec_rank'].fillna(20000)
myData['power'] = scryData['power'].fillna(-1)
myData['toughness'] = scryData['toughness'].fillna(-1)
myData['last_set'] = scryData['set_name']
myData['prices'] = scryData['prices']


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

myData.to_csv('my_card_data.csv', index=False)
#scryData.to_csv('old.csv', index=False)
