import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

scryData = pd.read_csv('2020_09_25_data_processed/fin_card_data.csv')
#scryData = scryData[scryData['price'] < 500]
#scryData = scryData[scryData['rarity'] < 2]

print(scryData['price'].max())
print(scryData['price'].min())
print(scryData['price'].mean())
print(scryData['price'].median())

sns.countplot(data=scryData, x='exp')
plt.show()

sns.countplot(data=scryData, x='rarity')
plt.show()

sns.catplot(data=scryData, kind='count', x='rarity', hue='exp')
plt.show()


basicCorr = scryData.corr(method='spearman')
print(basicCorr)
print(basicCorr.info(verbose=True))
sns.heatmap(basicCorr, vmin=-1, vmax=1, cmap='coolwarm', xticklabels=True,
            yticklabels=True, annot=False)
plt.show()
#
#sns.catplot(x='exp', y='rarity', hue='exp', data=scryData, kind='bar')
#plt.show()
#
#sns.regplot(x='edhrec_rank', y='price', data=scryData, line_kws={'color':'red'})
#plt.show()


sns.countplot(x='first_printing', data=scryData)
plt.show()
