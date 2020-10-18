import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score 
from sklearn.metrics import precision_score, roc_curve
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import FeatureUnion
from sklearn.ensemble import GradientBoostingClassifier

scryData = pd.read_csv('2020_09_25_data_processed/fin_card_data.csv', index_col=0)

bulkData = scryData
y = bulkData['exp']
bulkData = bulkData.drop(['exp'], axis=1)
bulkData = bulkData.drop(['price'], axis=1)
bulkData['oracle_text'] = bulkData['oracle_text'].str.replace('[,.\/+-1234567890]', ' ', regex=True)

X_train, X_test, y_train, y_test = train_test_split(bulkData, y, test_size=0.33)

get_text_data = FunctionTransformer(lambda x: x['oracle_text'])

get_numeric_data = FunctionTransformer(lambda x: x.loc[:, x.columns != 'oracle_text'])

gbc = GradientBoostingClassifier(n_estimators=400, max_features=10, max_depth=8,
                                 learning_rate=0.5)

vectorizer = CountVectorizer()
transformer = TfidfTransformer()

numeric_pl = Pipeline([('num_data', get_numeric_data)])
text_pl = Pipeline([('text_data', get_text_data),
                    ('vect', vectorizer),
                    ('trans', transformer)])

pl = Pipeline([
    ('union', FeatureUnion([
        ('numeric', numeric_pl)
        #('text', text_pl)
    ])),
    ('clf', gbc)
    ])

pl.fit(X_train, y_train)

pred = pl.predict(X_test)
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
