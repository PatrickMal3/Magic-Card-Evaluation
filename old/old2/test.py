import pandas as pd
import datetime as dt
import re

#######
# read in Data from scryfall 
#######

# data includes Oracle Texts
scryData = pd.read_json('scryfall-all-cards.json')

scryData.to_csv('all.csv', index=False)
