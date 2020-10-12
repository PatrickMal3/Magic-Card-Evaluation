import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, ExtraTreesClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, precision_score, roc_curve
from sklearn.model_selection import StratifiedKFold
from sklearn.svm import LinearSVC, SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import svm

# load in data
scryData = pd.read_csv('2020_07_14_data_processed/fin_card_data.csv')

bulkData = scryData
#filter_lst = [1,2]
#bulkData = bulkData[bulkData['rarity'].isin(filter_lst)]
y = bulkData['exp']
bulkData = bulkData.drop(['exp'], axis=1)
bulkData = bulkData.drop(['name'], axis=1)
bulkData = bulkData.drop(['price'], axis=1)
#bulkData = bulkData.drop(['edhrec_rank'], axis=1)


scaler = MinMaxScaler()
bulkData = scaler.fit_transform(bulkData)
bulkData = pd.DataFrame(bulkData, columns=['is_legendary','is_creature','is_instant',
    'is_scorcery','is_land','is_enchantment','is_planeswalker','is_artifact','cmc',
    'first_printing','last_printing','num_printings','id_white','id_blue','id_black',
    'is_red','is_green',
    'is_standard_legal','is_commander_legal','is_modern_legal',
    'is_pioneer_legal','is_legacy_legal','is_pauper_legal','is_reserved','is_reprint',
    'rarity','edhrec_rank','power','toughness','set_enum','is_booster'])


# classifier
RF = RandomForestClassifier(n_estimators=800, min_samples_split=5, min_samples_leaf=1,
                             max_features='sqrt', max_depth=70, bootstrap=False)

EXTRA = ExtraTreesClassifier(n_estimators=400, min_samples_split=5, min_samples_leaf=1,
                             max_features='auto', max_depth=90, bootstrap=False)

KNN = KNeighborsClassifier(weights='distance', n_neighbors=18, metric='manhattan',
        leaf_size=89, algorithm='ball_tree')

GBC = GradientBoostingClassifier(n_estimators=800, learning_rate=0.05, max_features=4,
                                 max_depth=4)

SVM = svm.SVC()


#mySVC = SVC(kernel='rbf', C=10, gamma=0.1)
mySVC = SVC(kernel='poly', C=10, gamma=1)

vtc = VotingClassifier(estimators=[#('rf', RF), ('svm', SVM),
                                    ('rf', RF),
                                    ('gbc', GBC)], voting='hard')

#vtc = VotingClassifier(estimators=[('svm', SVM)], voting='hard')

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
