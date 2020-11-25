import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

scryData = pd.read_csv('2020_09_25_data_processed/fin_card_data.csv', index_col=0)

lst = []
wordData = pd.DataFrame(lst)

wordData['oracle_text'] = scryData['oracle_text']
wordData['bulk'] = scryData['bulk']

y = wordData['bulk']
wordData = wordData.drop(['bulk'], axis=1)

count_vect = CountVectorizer(binary=True, analyzer='word', ngram_range=(1,4))

X_train, X_test, y_train, y_test = train_test_split(wordData, y, test_size=0.33)

X_train_vectors = count_vect.fit_transform(X_train['oracle_text'])
#print(X_train_vectors.shape)
X_test_vectors = count_vect.transform(X_test['oracle_text'])
#print(count_vect.get_feature_names())
#print(X_train_counts.shape)
 
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, precision_score, roc_curve

clf = MultinomialNB()

clf.fit(X_train_vectors, y_train)

pred = clf.predict(X_test_vectors)
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

bulkData = scryData
y = bulkData['bulk']
bulkData = bulkData.drop(['bulk'], axis=1)
bulkData = bulkData.drop(['price'], axis=1)
bulkData = bulkData.drop(['oracle_text'], axis=1)
























