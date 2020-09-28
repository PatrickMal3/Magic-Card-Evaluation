import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, precision_score, roc_curve
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

scryData = pd.read_csv('2020_09_25_data_processed/fin_card_data.csv', index_col=0)

bulkData = scryData
y = bulkData['exp']
bulkData = bulkData.drop(['exp'], axis=1)
bulkData = bulkData.drop(['price'], axis=1)

scaler = StandardScaler()
bulkData = scaler.fit_transform(bulkData)
bulkData = pd.DataFrame(bulkData, columns=['is_legendary','is_creature','is_instant',
    'is_scorcery','is_land','is_enchantment','is_planeswalker','is_artifact','cmc',
    'first_printing','last_printing','num_printings','id_white','id_blue','id_black',
    'is_red','is_green',
    'is_standard_legal','is_commander_legal','is_modern_legal',
    'is_pioneer_legal','is_legacy_legal','is_pauper_legal','is_reserved','is_reprint',
    'rarity','edhrec_rank','power','toughness','set_enum','is_booster'])

from sklearn.svm import LinearSVC

Model = LinearSVC(random_state=0, tol=1e-5)

X_train, X_test, y_train, y_test = train_test_split(bulkData, y, test_size=0.33)

# fit the train-test-split model
Model.fit(X_train, y_train)

pred = Model.predict(X_test)
print('Train-Test-Split Confusion Matrix:')
print(confusion_matrix(pred, y_test))
print('')
print('Train-Test-Split accuracy:')
print(accuracy_score(pred, y_test))
print('')
print('Train-Test-Split recall:')
print(recall_score(pred, y_test))
print('')
print('Train-Test-Split precision:')
print(precision_score(pred, y_test))
print('')
