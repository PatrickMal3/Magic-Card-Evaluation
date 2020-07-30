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

# load in data
scryData = pd.read_csv('2020_07_14_data_processed/fin_card_data.csv')

y = scryData['exp']
bulkData = scryData.drop(['exp'], axis=1)
bulkData = bulkData.drop(['name'], axis=1)
bulkData = bulkData.drop(['price'], axis=1)
#bulkData = bulkData.drop(['edhrec_rank'], axis=1)

#bulkData = scryData[['rarity', 'cmc', 'first_printing', 'last_printing',
#                     'num_printings', 'set_enum', 'is_legendary',
#                     'edhrec_rank']]


# RF classifier
RF = RandomForestClassifier(n_estimators=1600, min_samples_split=5, min_samples_leaf=1,
                            max_features='sqrt', max_depth=70, bootstrap=False)

#RF = RandomForestClassifier()
# KFold Scoring
#acc_scores = cross_val_score(RF, bulkData, y, cv=10, scoring='accuracy')
#rec_scores = cross_val_score(RF, bulkData, y, cv=10, scoring='recall')
#pre_scores = cross_val_score(RF, bulkData, y, cv=10, scoring='precision')
#
##print(scores)
#print('KFold mean accuracy:')
#print(acc_scores.mean())
#print('KFold mean recall:')
#print(rec_scores.mean())
#print('KFold mean precsion:')
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
print('Stratified_KFold mean accuracy:')
print(np.array(acc).mean())
print('')
print('Stratified_KFold mean recall:')
print(np.array(rec).mean())
print('')
print('Stratified_KFold mean precision:')
print(np.array(pre).mean())
print('')


# train test split
X_train, X_test, y_train, y_test = train_test_split(bulkData, y, test_size=0.33)

# fit the train-test-split model
RF.fit(X_train, y_train)

pred = RF.predict(X_test)
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

X_test['exp'] = y_test
X_test['pred'] = pred
print(X_test)
X_test.to_csv('results.csv', index=False)

#print('Most important features:')
#feature_importances = pd.DataFrame(RF.feature_importances_,
#                                   index = X_train.columns,
#                                    columns=['importance']).sort_values('importance',                                                                 ascending=False)
#
#print(feature_importances)

#probs = RF.predict_proba(X_test)
#probs = probs[:, 1]
#fpr, tpr, thresholds = roc_curve(y_test, probs)
#
#def plot_roc_curve(fpr, tpr):
#    plt.plot(fpr, tpr, color='orange', label='ROC')
#    plt.plot([0, 1], [0, 1], color='darkblue', linestyle='--')
#    plt.xlabel('False Positive Rate')
#    plt.ylabel('True Positive Rate')
#    plt.title('Receiver Operating Characteristic (ROC) Curve')
#    plt.legend()
#    plt.show()
#
#plot_roc_curve(fpr, tpr)
#
#preRec = plot_precision_recall_curve(RF, X_test, y_test)
#plt.show()
