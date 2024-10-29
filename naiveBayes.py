import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Dropped dataset, IoTIP_int, hostIP_int, year_month
df = pd.read_csv('newSample.csv')
X = df.drop(columns=['IoTMac'])
y = df['IoTMac']

# Defines categorical variables
categories = ['IoTMac', 'hostMac', 'IoTIP', 'hostIP', 'ipProto', 'reverseFlowExists', 'remote', 'broadcast', 'HTTP', 'HTTPS', 'DNS', 'NTP', 'TCP_others', 'UDP_others']
for var in categories:
    df[var] = df[var].astype('category')

X = pd.get_dummies(X, drop_first=True)
XTrain, XTest, yTrain, yTest = train_test_split(X, y, test_size=0.2, random_state=10)

# Fits the model on the training data using Naive Bayes
model = GaussianNB()
model.fit(XTrain, yTrain)

yPred = model.predict(XTest)
print(classification_report(yTest, yPred, zero_division=0))

# Shows true positives, true negatives, false positives, false negatives
confusionMatrix = confusion_matrix(yTest, yPred)

# Heatmap visualisation of the Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(confusionMatrix, annot=True, fmt='d', cmap='Blues', xticklabels=model.classes_, yticklabels=model.classes_)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix Heatmap')
plt.show()