import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib
import seaborn as sb

myData = pd.read_csv('fin_card_data.csv')

sb.set(style='ticks', color_codes=True)

# price vs edhrec_rank
ax = sb.scatterplot(y='first_printing', x='edhrec_rank', 
                    hue='is_commander_legal',
                    marker='+', data=myData)
#ax.set(xlim=(0,10000))



ax.xaxis.set_major_locator(plticker.MultipleLocator(5000))
ax.xaxis.set_major_formatter(plticker.ScalarFormatter())
plt.title('Card price compared to EDHREC Rank')
plt.ylabel('Card Price in US$')
plt.xlabel('EDHREC Rank')
plt.show()




