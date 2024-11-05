#!/usr/bin/env python3
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix, accuracy_score
import warnings
from time import time
import sys
start_time = time()
warnings.filterwarnings("ignore")

column_names = [
    "name", "start_date", "start_time", "duration", "reverseDelta", "IoTMac", "hostMac", 
    "IoTIP", "IoTIP_int", "hostIP", "hostIP_int", "ipProto", "IoTPort", "hostPort", 
    "PacketCount", "BytesCount", "reversePacketCount", "reverseBytesCount", "SmallPktCount", 
    "LargePktCount", "NonEmptyPktCount", "DataByteCount", "AvgIAT", "FirstNonEmptyPktSize", 
    "MaxPktSize", "StdevPayloadSize", "StdevIAT", "AvgPacketSize", "reverseSmallPktCount", 
    "reverseLargePktCount", "reverseNonEmptyPktCount", "reverseDataByteCount", "reverseAvgIAT", 
    "reverseFirstNonEmptyPktSize", "reverseMaxPktSize", "reverseStdevPayloadSize", "reverseStdevIAT", 
    "reverseAvgPacketSize", "reverseFlowExists", "remote", "broadcast", "HTTP", "HTTPS", "DNS", 
    "NTP", "TCP_others", "UDP_others", "year_month"
]

df_train2 = pd.read_csv(sys.argv[1], names=column_names)
df_test2 = pd.read_csv(sys.argv[2],names=column_names)


df_train = df_train2.drop(columns = ['name','IoTIP_int', 'hostIP_int', 'year_month'])
df_test = df_test2.drop(columns = ['name','IoTIP_int', 'hostIP_int', 'year_month'])
# Dropped dataset, IoTIP_int, hostIP_int, year_month

# Drop original date and time columns
df_train.drop(columns=['start_date', 'start_time', 'IoTIP', 'hostMac', 'hostIP'], inplace=True)
df_test.drop(columns=['start_date', 'start_time', 'IoTIP', 'hostMac', 'hostIP'], inplace=True)

# Defines categorical variables
categories = ['IoTMac', 'ipProto', 'reverseFlowExists', 'remote', 'broadcast', 'HTTP', 'HTTPS', 'DNS', 'NTP', 'TCP_others', 'UDP_others']
for var in categories:
    df_train[var] = df_train[var].astype('category')
    df_test[var] = df_test[var].astype('category')

XTrain = df_train.drop(columns=['IoTMac'])
yTrain = df_train['IoTMac']

XTest = df_test.drop(columns=['IoTMac'])
yTest = df_test['IoTMac']

#XTrain, XTest, yTrain, yTest = train_test_split(X, y, test_size=0.2, random_state=42)

parameters = param_grid = {
    'num_leaves': [100],
    'max_depth': [20], # -1 means unlimited
    'learning_rate': [0.01],
    'n_estimators': [200],
    'verbosity': [-1]
}

grid = GridSearchCV(lgb.LGBMClassifier(random_state=42), param_grid, cv=3, scoring='neg_log_loss', n_jobs=-1)
grid.fit(XTrain, yTrain)
bestParamsModel = grid.best_estimator_

bestParamsModel.fit(XTrain, yTrain)
yPred = bestParamsModel.predict(XTest)
accuracy = accuracy_score(yTest, yPred)

print("Best parameters found: ", grid.best_params_)
print(f'Accuracy: {accuracy:.5f}')
cmatrix = confusion_matrix(yTest, yPred)
for f in cmatrix:
    f += 1
import seaborn as sns
from matplotlib.colors import LogNorm
s = sns.heatmap(cmatrix, annot=False, cmap='coolwarm', norm=LogNorm())
s.set_xlabel('Predicted Class')
s.set_ylabel('Actual Class')
crosstab = pd.crosstab(yTest,yPred,rownames=['True'],colnames=['Predicted'],margins=True)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(crosstab)
print(time() - start_time)
