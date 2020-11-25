import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, precision_score, roc_curve
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import plot_precision_recall_curve
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RandomizedSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import BaggingClassifier
from xgboost import XGBClassifier


# load in data
scryData = pd.read_csv('2020_09_25_data_processed/fin_card_data.csv')

y = scryData['exp']
bulkData = scryData.drop(['exp'], axis=1)
bulkData = bulkData.drop(['name'], axis=1)
bulkData = bulkData.drop(['price'], axis=1)
bulkData = bulkData.drop(['oracle_text'], axis=1)
#bulkData = bulkData.drop(['edhrec_rank'], axis=1)

#bulkData = scryData[['rarity', 'cmc', 'first_printing', 'last_printing',
#                     'num_printings', 'set_enum', 'is_legendary',
#                     'edhrec_rank']]




#n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
#max_features = ['auto', 'sqrt']
#max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
#max_depth.append(None)
#min_samples_split = [2, 5, 10]
#min_samples_leaf = [1, 2, 4]
#bootstrap = [True, False]# Create the random grid
#random_grid = {'n_estimators': n_estimators,
#               'max_features': max_features,
#               'max_depth': max_depth,
#               'min_samples_split': min_samples_split,
#               'min_samples_leaf': min_samples_leaf,
#               'bootstrap': bootstrap}
#
#n_neighbors = [int(x) for x in np.linspace(start = 2, stop = 20, num = 10)]
#weights = ['uniform', 'distance']
#algorithm = ['auto', 'ball_tree', 'kd_tree', 'brute']
#leaf_size = [int(x) for x in np.linspace(start = 5, stop = 100, num = 10)]
#metric = ['minkowski', 'manhattan', 'euclidean']
#random_grid = {'n_neighbors': n_neighbors,
#               'weights': weights,
#               'algorithm': algorithm,
#               'leaf_size': leaf_size,
#               'metric': metric}
#
#C = [1,10,100]
#gamma = [1, 0.1, 10, 0.01]
#kernel = ['linear']
#random_grid = {'C': C,
#               'gamma': gamma}
             


max_depth = [4,5,6,7,8,9]
min_child_weight = [3,4,5,8,9]
gamma = [1,2,5,10]
subsample = [0.2,0.5,0.7,1]
colsample_bytree = [0.1,0.2,0.5,1]
random_grid = {'max_depth':max_depth, 
               'min_child_weight':min_child_weight,
               'gamma':gamma,
               'subsample':subsample,
               'colsample_bytree':colsample_bytree}


# RF classifier
RF = RandomForestClassifier()
EXTRA = ExtraTreesClassifier()
KNN = KNeighborsClassifier()
mySVC = LinearSVC()
gbc = GradientBoostingClassifier()
bc = BaggingClassifier()
xgboost = XGBClassifier()
rf_random = RandomizedSearchCV(estimator = bc, param_distributions = random_grid, 
                               n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)


# train test split
X_train, X_test, y_train, y_test = train_test_split(bulkData, y, test_size=0.33)

# fit the train-test-split model
#RF.fit(X_train, y_train)
rf_random.fit(X_train, y_train)
#mySVC.fit(X_train, y_train)
print(rf_random.best_params_)

pred = rf_random.predict(X_test)
#pred = mySVC.predict(X_test)
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
