# TO DO: 
# - Implement CV later since it will probably add a lot to the already long runtime

# Note:
# Care in running the grid search it will take a very long time
# Current best params for sample: {'learning_rate': 0.05, 'max_depth': 10, 'n_estimators': 100, 'num_leaves': 50}

import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import metrics

# Dropped dataset, IoTIP_int, hostIP_int, year_month
df = pd.read_csv('newSample.csv')

# Drop original date and time columns
df.drop(columns=['start_date', 'start_time'], inplace=True)

# Defines categorical variables
categories = ['IoTMac', 'hostMac', 'IoTIP', 'hostIP', 'ipProto', 'reverseFlowExists', 'remote', 'broadcast', 'HTTP', 'HTTPS', 'DNS', 'NTP', 'TCP_others', 'UDP_others']
for var in categories:
    df[var] = df[var].astype('category')

X = df.drop(columns=['IoTMac'])
y = df['IoTMac']

XTrain, XTest, yTrain, yTest = train_test_split(X, y, test_size=0.2, random_state=42)

parameters = param_grid = {
    'num_leaves': [30, 50, 100],
    'max_depth': [10, 20, -1], # -1 means unlimited
    'learning_rate': [0.01, 0.05, 0.1],
    'n_estimators': [50, 100, 200]
}

grid = GridSearchCV(lgb.LGBMClassifier(random_state=42), param_grid, cv=3, scoring='neg_log_loss', n_jobs=-1)
grid.fit(XTrain, yTrain)

bestParamsModel = grid.best_estimator_

bestParamsModel.fit(XTrain, yTrain)

print("Best parameters found: ", grid.best_params_)
print('Training accuracy {:.4f}'.format(bestParamsModel.score(XTrain, yTrain)))
print('Testing accuracy {:.4f}'.format(bestParamsModel.score(XTest,yTest)))

    