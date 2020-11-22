import tensorflow as tf
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


scryData = pd.read_csv('2020_07_14_data_processed/fin_card_data.csv')

bulkData = scryData
y = bulkData['exp']
bulkData = bulkData.drop(['exp'], axis=1)
bulkData = bulkData.drop(['name'], axis=1)
bulkData = bulkData.drop(['price'], axis=1)

X_train, X_test, y_train, y_test = train_test_split(bulkData, y, test_size=0.33)

model = Sequential()
model.add(Dense(100, input_dim=31, activation= "relu"))
model.add(Dense(50, activation= "relu"))
model.add(Dense(1))
model.summary()

model.compile(loss=tf.losses.MeanSquaredError(),
        optimizer=tf.optimizers.Adam(),
        metrics=['accuracy'])

model.fit(X_train, y_train, epochs=90, validation_data=(X_test, y_test))

test_loss, test_acc = model.evaluate(X_test, y_test, verbose=2)
print(test_acc)
