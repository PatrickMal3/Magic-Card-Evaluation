import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, precision_score, roc_curve
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import plot_precision_recall_curve
from sklearn.model_selection import cross_val_score

# load in data
scryData = pd.read_csv('fin_card_data.csv')

y = scryData['exp']
bulkData = scryData.drop(['exp'], axis=1)
bulkData = bulkData.drop(['name'], axis=1)
bulkData = bulkData.drop(['price'], axis=1)
bulkData = bulkData.drop(['edhrec_rank'], axis=1)

bulkData = scryData[['rarity', 'cmc', 'first_printing', 'last_printing',
                     'num_printings', 'set_enum', 'is_legendary',
                     'edhrec_rank']]

# train test split
X_train, X_test, y_train, y_test = train_test_split(bulkData, y, test_size=0.33)

# RF classifier
RF = RandomForestClassifier()
RF.fit(X_train, y_train)

#scores = cross_val_score(RF, bulkData, y, cv=20, scoring='f1_macro')
#print(scores)
#print(scores.mean())

pred = RF.predict(X_test)
print(confusion_matrix(pred, y_test))
print(accuracy_score(pred, y_test))
print(recall_score(pred, y_test))
print(precision_score(pred, y_test))

feature_importances = pd.DataFrame(RF.feature_importances_,
                                   index = X_train.columns,
                                    columns=['importance']).sort_values('importance',                                                                 ascending=False)

print(feature_importances)

probs = RF.predict_proba(X_test)
probs = probs[:, 1]
fpr, tpr, thresholds = roc_curve(y_test, probs)

def plot_roc_curve(fpr, tpr):
    plt.plot(fpr, tpr, color='orange', label='ROC')
    plt.plot([0, 1], [0, 1], color='darkblue', linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend()
    plt.show()

plot_roc_curve(fpr, tpr)

preRec = plot_precision_recall_curve(RF, X_test, y_test)
plt.show()
