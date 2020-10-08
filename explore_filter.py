import pandas as pd

scryData = pd.read_csv('2020_09_25_data_processed/fin_card_data.csv')


filter_rarity_lst = [3,4]
scryData = scryData[~scryData['rarity'].isin(filter_rarity_lst)]
scryData = scryData[scryData['price'] > 1]


scryData.to_csv('explore_data.csv', index=False)
