#!/usr/bin/env python3
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import SequentialFeatureSelector as sfs
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from time import time
import sys
start_time = time()
seed = 42
test_size = 0.2
column_names = [
    "name", "start_date", "start_time", "duration", "reverseDelta", "IoTMac", "hostMac", 
    "IoTIP", "IoTIP_int", "hostIP", "hostIP_int", "ipProto", "IoTPort", "hostPort", 
    "PacketCount", "BytesCount", "reversePacketCount", "reverseBytesCount", "SmallPktCount", 
    "LargePktCount", "NonEmptyPktCount", "DataByteCount", "AvgIAT", "FirstNonEmptyPktSize", 
    "MaxPktSize", "StdevPayloadSize", "StdevIAT", "AvgPacketSize", "reverseSmallPktCount", 
    "reverseLargePktCount", "reverseNonEmptyPktCount", "reverseDataByteCount", "reverseAvgIAT", 
    "PktSize", "reverseMaxPktSize", "reverseStdevPayloadSize", "reverseStdevIAT", 
    "reverseAvgPacketSize", "reverseFlowExists", "remote", "broadcast", "HTTP", "HTTPS", "DNS", 
    "NTP", "TCP_others", "UDP_others", "year_month"
]

df_train = pd.read_csv(sys.argv[1], names=column_names)
df_test = pd.read_csv(sys.argv[2],names=column_names)

target_columns = ['IoTMac']
y_train = df_train.filter(items = target_columns)
X_train = df_train.drop(['name','start_date', 'start_time', 'year_month','IoTIP', 'IoTIP_int', 'hostMac', 'IoTMac', 'hostIP', 'hostIP_int'], axis=1)

y_test = df_test.filter(items = target_columns)
X_test = df_test.drop(['name','start_date', 'start_time', 'year_month','IoTIP', 'IoTIP_int', 'hostMac', 'IoTMac', 'hostIP', 'hostIP_int'], axis=1)

# Split the dataset into training and test sets (80% train, 20% test)
#X_train, X_test, y_train, y_test = train_test_split(X, y.values.ravel(), test_size=test_size, random_state=seed)

#Create a random forest model (we found 25 esimators was best)

parameters = param_grid = {
    'max_features': [5],
    'max_depth': [15], # -1 means unlimited
    'n_estimators': [150],
    'verbose': [0]
}
grid = GridSearchCV(RandomForestClassifier(random_state=seed), param_grid, cv=3, scoring='neg_log_loss', n_jobs=-1)
grid.fit(X_train, y_train)
bestParamsModel = grid.best_estimator_
bestParamsModel.fit(X_train, y_train)

# Make predictions and evaluate the model

y_pred = bestParamsModel.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
y_test2 = y_test['IoTMac']
#print("Best parameters found: ", grid.best_params_)
print(f'Accuracy: {accuracy:.5f}')
cmatrix = confusion_matrix(y_test, y_pred)
for f in cmatrix:
    f += 1
import seaborn as sns
from matplotlib.colors import LogNorm
sns_map = sns.heatmap(cmatrix, annot=False, cmap='coolwarm', norm=LogNorm())
sns_map.set_xlabel('Predicted Class')
sns_map.set_ylabel('Actual Class')
crosstab = pd.crosstab(y_test2,y_pred,rownames=['True'],colnames=['Predicted'],margins=True)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(crosstab)
print(time() - start_time)
