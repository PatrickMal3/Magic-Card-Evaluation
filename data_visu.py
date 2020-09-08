import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

scryData = pd.read_csv('2020_08_22_data_processed/fin_card_data.csv')

basicCorr = scryData.corr(method='spearman')
print(basicCorr.info(verbose=True))
sns.heatmap(basicCorr, vmin=-1, vmax=1, cmap='coolwarm', xticklabels=True,
            yticklabels=True, annot=False)
plt.show()

sns.catplot(x='exp', y='rarity', hue='exp', data=scryData, kind='bar')
plt.show()
