# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 12:48:35 2024

@author: camer
"""

from sklearn.neural_network import MLPClassifier 
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler


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

# Load data and clean 'name' column
df = pd.read_csv('sample2.csv', names=column_names)
df['name'] = df['name'].str.replace(r'_\d{4}_\d{2}\.csv$', '', regex=True)

# Step 3: Encode 'name' as dummy variables
target_columns = ['IoTMac']
y = df.filter(items = target_columns)
df = df.drop(['name','start_date', 'start_time', 'year_month','IoTIP', 'hostIP', 'IoTIP_int', 'IoTPort', 'IoTMac'], axis=1)
df2 = pd.get_dummies(df, drop_first=True)

X = df2
print(X.head())
print(y.head())
# Split the dataset into training and test sets 20-80
X_train, X_test, y_train, y_test = train_test_split(X, y.values.ravel(), test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
# Initialize and train the Random Forest classifier
model = MLPClassifier(alpha = .007,learning_rate_init=.01,learning_rate='constant',early_stopping=True,max_iter=100,random_state=42)
model.fit(X_train, y_train)

# Make predictions and evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f'Accuracy: {accuracy:.5f}')