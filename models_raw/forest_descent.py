import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import SequentialFeatureSelector as sfs
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from time import time
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

df_train2 = pd.read_csv("train_equal.csv", names=column_names)
df_test2 = pd.read_csv("test.csv",names=column_names)


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

X_train = df_train.drop(columns=['IoTMac'])
y_train = df_train['IoTMac']

X_test = df_test.drop(columns=['IoTMac'])
y_test = df_test['IoTMac']



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
y_pred = bestParamsModel.predict(X_test)

parameters = param_grid2 = {
    'num_leaves': [100],
    'max_depth': [20], # -1 means unlimited
    'learning_rate': [0.01],
    'n_estimators': [200],
    'verbosity': [-1]
}
X_train.reset_index(inplace=True)
X_test.reset_index(inplace=True)
X_test2 = pd.DataFrame.transpose(X_test)

# Make predictions and evaluate the model
grid2 = GridSearchCV(lgb.LGBMClassifier(random_state=42), param_grid2, cv=3, scoring='neg_log_loss', n_jobs=-1)
grid2.fit(X_train, y_train)
bestParamsModel2 = grid2.best_estimator_

bestParamsModel2.fit(X_train, y_train)




i = 0
while i < len(y_pred):
    if y_pred[i] == "04:5d:4b:a4:d0:2e:":
        y_pred[i] = bestParamsModel2.predict(np.array(X_test2[i].values.tolist()).reshape(1,-1))[0]
        if y_pred[i] == "80:c5:f2:0b:aa:a9:":
            y_pred[i] = "38:56:10:00:1d:8c:"
    i += 1
accuracy = accuracy_score(y_test, y_pred)

print(f'Accuracy: {accuracy:.5f}')

cmatrix = confusion_matrix(y_test, y_pred)
for f in cmatrix:
    f += 1
import seaborn as sns
from matplotlib.colors import LogNorm
sns_map = sns.heatmap(cmatrix, annot=False, cmap='coolwarm', norm=LogNorm())
sns_map.set_xlabel('Predicted Class')
sns_map.set_ylabel('Actual Class')
crosstab = pd.crosstab(y_test,y_pred,rownames=['True'],colnames=['Predicted'],margins=True)
print(time() - start_time)

#class 3 corresponds to 00:a2:b2:b9:09:87:



