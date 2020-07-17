import pandas as pd
import datetime as dt
import re

scryData = pd.read_csv('card_data.csv')


#######
# feature filtering
#######

# layouts to filter out
filter_layout_lst = ['art_series', 'augment', 'double_faced_token', 'emblem',
            'host', 'planar', 'scheme', 'token', 'vanguard']
scryData = scryData[~scryData['layout'].isin(filter_layout_lst)]

# filter corrupted and special
filter_names_lst = ['Shu General', 'Ancient Spider', 'Longbow Archer',
                    'Livonya Silone',
                    'Noxious Hydra Breath', 'Tel-Jilad Archers',
                    'Bayou Dragonfly', 'Zhang Fei, Fierce Warrior',
                    'Lu Bu, Master-at-Arms']
scryData = scryData[~scryData['names'].isin(filter_names_lst)]

# filter by sets
filter_set_lst = ['unh', 'ust', 'und', 'ugl', 'tfth', 'htr', 'htr17', 'htr18',
                  'ana', 'tbth', 'pcel', 'tdag', 'prm', 'hho']
scryData = scryData[~scryData['set_name'].isin(filter_set_lst)]

filter_settype_lst = ['funny', 'token']#, 'archenemy', 'planechase']
scryData = scryData[~scryData['set_type'].isin(filter_settype_lst)]


print(scryData.info(verbose = True))
print(' ')
print(scryData.shape)

#######
# save cleaned dataframe to csv
#######

scryData.to_csv('filtered_card_data.csv', index=False)
