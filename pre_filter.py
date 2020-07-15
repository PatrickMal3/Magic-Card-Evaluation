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
filter_set_lst = ['unh', 'ust', 'und', 'ugl', 'tfth', 'htr', 'htr17', 'htr18',
                  'ana', 'tbth', 'pcel', 'tdag', 'prm', 'hho']

scryData = scryData[~scryData['set'].isin(filter_set_lst)]

filter_settype_lst = ['funny', 'token']

scryData = scryData[~scryData['set_type'].isin(filter_set_lst)]

print(scryData.info(verbose = True))
print(' ')
print(scryData.shape)

#######
# save cleaned dataframe to csv
#######

scryData.to_csv('prefiltered_card_data.csv', index=False)
