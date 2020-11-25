import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, ExtraTreesClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, precision_score, roc_curve
from sklearn.model_selection import StratifiedKFold
from sklearn.svm import LinearSVC, SVC
from sklearn import svm
from xgboost import XGBClassifier

# load in data
scryData = pd.read_csv('2020_09_25_data_processed/fin_card_data.csv')

bulkData = scryData
y = bulkData['bulk']
bulkData = bulkData.drop(['bulk'], axis=1)
bulkData = bulkData.drop(['name'], axis=1)
bulkData = bulkData.drop(['price'], axis=1)
bulkData = bulkData.drop(['oracle_text'], axis=1)

# classifier
RF = RandomForestClassifier(n_estimators=800, min_samples_split=5, min_samples_leaf=1,
                             max_features='sqrt', max_depth=70, bootstrap=False)

SVM = svm.SVC(C=10, gamma=0.0001, kernel='rbf')

xgboost = XGBClassifier(colsample_bytree=1.0, eval_metric='mae', max_depth=5,
        min_child_weight=3, subsample=0.8)

vtc = VotingClassifier(estimators=[('svm', SVM), 
    ('rf', RF), ('xgboost', xgboost)], voting='hard')

#vtc = VotingClassifier(estimators=[('xgboost', xgboost)], voting='hard')
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

    vtc.fit(X1_train, y1_train)
    prediction = vtc.predict(X1_test)
    acc_score = accuracy_score(prediction, y1_test)
    acc.append(acc_score)
    rec_score = recall_score(prediction, y1_test)
    rec.append(rec_score)
    pre_score = precision_score(prediction, y1_test)
    pre.append(pre_score)

#print(acc)
print('Stratified_KFold mean accuracy:')
print(np.array(acc).mean())
print('')
print('Stratified_KFold mean recall:')
print(np.array(rec).mean())
print('')
print('Stratified_KFold mean precision:')
print(np.array(pre).mean())
print('')
