from sklearn import svm
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

seed = 42

# Load and preprocess data
sample = pd.read_csv("data/newSample.csv")
data = sample.drop(columns=['start_date', 'start_time', 'IoTIP', 'IoTPort', 'hostIP', 'hostPort', 'BytesCount', 'reversePacketCount', 'reverseBytesCount', 'reverseMaxPktSize', 'reverseStdevIAT', 'reverseAvgPacketSize', 'reverseFlowExists', 'broadcast'])

# Define input features (X) and target (y)
x = data.drop(columns=['IoTMac'])
y = data['IoTMac']

# Convert categorical variables into dummy/indicator variables
X = pd.get_dummies(x)

# Encode the target variable (y) for multi-class classification
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)


# Normalize the input data
scaler = StandardScaler()
X_normalized = scaler.fit_transform(X)

# Split data into training, validation, and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_normalized, y, test_size=0.2, random_state=42)


clf = svm.SVC(C=5, gamma=1000, kernel='rbf')
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f'Accuracy: {accuracy:.5f}')
cmatrix = confusion_matrix(y_test, y_pred)
for f in cmatrix:
    f += 1



import seaborn as sns
from matplotlib.colors import LogNorm
sns.heatmap(cmatrix, annot=False, cmap='coolwarm', norm=LogNorm())

# 0.82700 - poly
# 0.85450 - rbf - gamma = 10000
# 0.92350, rbf, C = 5, gamma = 1000