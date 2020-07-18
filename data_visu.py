import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

scryData = pd.read_csv('fin_card_data.csv')

basicCorr = scryData.corr(method='spearman')
sns.heatmap(basicCorr, vmin=-1, vmax=1, cmap='coolwarm', xticklabels=True,
            yticklabels=True)
plt.show()
