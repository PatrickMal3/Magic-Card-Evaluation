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
from sklearn.model_selection import RandomizedSearchCV

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




n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
max_features = ['auto', 'sqrt']
max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth.append(None)
min_samples_split = [2, 5, 10]
min_samples_leaf = [1, 2, 4]
bootstrap = [True, False]# Create the random grid
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}

# RF classifier
RF = RandomForestClassifier()
rf_random = RandomizedSearchCV(estimator = RF, param_distributions = random_grid, 
                               n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)


# train test split
X_train, X_test, y_train, y_test = train_test_split(bulkData, y, test_size=0.33)

# fit the train-test-split model
RF.fit(X_train, y_train)
rf_random.fit(X_train, y_train)
print(rf_random.best_params_)

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
