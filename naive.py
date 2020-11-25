import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, precision_score, roc_curve

scryData = pd.read_csv('2020_09_25_data_processed/fin_card_data.csv', index_col=0)

bulkData = scryData
y = bulkData['bulk']
bulkData = bulkData.drop(['bulk'], axis=1)
bulkData = bulkData.drop(['price'], axis=1)
bulkData = bulkData.drop(['oracle_text'], axis=1)

X_train, X_test, y_train, y_test = train_test_split(bulkData, y, test_size=0.33)

pred = np.zeros(len(X_test))
print(pred)
print('>>>Naive Classificator all Zeros<<<')
print('Accuracy:')
print(accuracy_score(pred, y_test))

pred = np.ones(len(X_test))
print(pred)
print('>>>Naive Classificator all Zeros<<<')
print('Accuracy:')
print(accuracy_score(pred, y_test))

pred = np.where(X_test['rarity'] == 1, 1, 0)
print(pred)
print('>>>Naive Classificator all Zeros<<<')
print('Accuracy:')
print(accuracy_score(pred, y_test))

pred = np.where(X_test['rarity'] < 3, 1, 0)
print(pred)
print('>>>Naive Classificator all Zeros<<<')
print('Accuracy:')
print(accuracy_score(pred, y_test))
