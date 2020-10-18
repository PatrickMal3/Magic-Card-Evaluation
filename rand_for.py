import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, precision_score, roc_curve
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import plot_precision_recall_curve
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

# load in data
scryData = pd.read_csv('2020_09_25_data_processed/fin_card_data.csv', index_col=0)

bulkData = scryData
#filter_lst = [4]
#bulkData = bulkData[bulkData['rarity'].isin(filter_lst)]
#bulkData = bulkData[bulkData['last_printing'] != 2020]
y = bulkData['exp']
bulkData = bulkData.drop(['exp'], axis=1)
bulkData = bulkData.drop(['price'], axis=1)
#bulkData = bulkData.drop(['set_enum'], axis=1)
bulkData = bulkData.drop(['oracle_text'], axis=1)


#scaler = StandardScaler()
#bulkData = scaler.fit_transform(bulkData)
#bulkData = pd.DataFrame(bulkData, columns=['is_legendary','is_creature','is_instant',
#    'is_scorcery','is_land','is_enchantment','is_planeswalker','is_artifact','cmc',
#    'first_printing','last_printing','num_printings','id_white','id_blue','id_black',
#    'is_red','is_green',
#    'is_standard_legal','is_commander_legal','is_modern_legal',
#    'is_pioneer_legal','is_legacy_legal','is_pauper_legal','is_reserved','is_reprint',
#    'rarity','edhrec_rank','power','toughness','set_enum','is_booster'])

# RF classifier
# best Parameters found with random grid parameter search
RF = RandomForestClassifier(n_estimators=1000, min_samples_split=5, min_samples_leaf=1,
                            max_features='sqrt', max_depth=30, bootstrap=False)

## KFold Scoring
#acc_scores = cross_val_score(RF, bulkData, y, cv=10, scoring='accuracy')
#rec_scores = cross_val_score(RF, bulkData, y, cv=10, scoring='recall')
#pre_scores = cross_val_score(RF, bulkData, y, cv=10, scoring='precision')
#
##print(scores)
#print('KFold mean accuracy:')
#print(acc_scores.mean())
#print('')
#print('KFold mean recall:')
#print(rec_scores.mean())
#print('')
#print('KFold mean precision:')
#print(pre_scores.mean())
#print('')


# Stratified KFold Scoring
acc = []
rec = []
pre = []

skf = StratifiedKFold(n_splits=10)
skf.get_n_splits(bulkData, y)
for train_index, test_index in skf.split(bulkData, y):
    #print('Train:', train_index, 'Validation:', test_index)
    X1_train, X1_test = bulkData.iloc[train_index], bulkData.iloc[test_index]
    y1_train, y1_test = y.iloc[train_index], y.iloc[test_index]

    RF.fit(X1_train, y1_train)
    prediction = RF.predict(X1_test)
    acc_score = accuracy_score(prediction, y1_test)
    acc.append(acc_score)
    rec_score = recall_score(prediction, y1_test)
    rec.append(rec_score)
    pre_score = precision_score(prediction, y1_test)
    pre.append(pre_score)

#print(acc)
print('>>>Stratified_KFold Metrics<<<')
print('Stratified_KFold mean accuracy:')
print(np.array(acc).mean())
print('')
print('Stratified_KFold mean recall:')
print(np.array(rec).mean())
print('')
print('Stratified_KFold mean precision:')
print(np.array(pre).mean())
print('')



bulkData = scryData
#bulkData = bulkData[bulkData['rarity'].isin(filter_lst)]
#bulkData = bulkData[bulkData['last_printing'] != 2019]
#bulkData = bulkData[bulkData['price'] < 500]
y = bulkData['exp']
bulkData = bulkData.drop(['exp'], axis=1)
bulkData = bulkData.drop(['price'], axis=1)
bulkData = bulkData.drop(['oracle_text'], axis=1)

# train test split
X_train, X_test, y_train, y_test = train_test_split(bulkData, y, test_size=0.33)

# fit the train-test-split model
RF.fit(X_train, y_train)

print(X_train)

pred = RF.predict(X_test)
print('>>>Train-Test-Split Metrics<<<')
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

result_df = pd.DataFrame(X_test)
result_df['exp'] = y_test
result_df['pred'] = pred

result_df.to_csv('results.csv', index=True)

# Feature importance
print('Most important features:')
feature_importances = pd.DataFrame(RF.feature_importances_,
                                   index = X_train.columns,
                                    columns=['importance']).sort_values('importance',
                                                                         ascending=False)
print(feature_importances)
