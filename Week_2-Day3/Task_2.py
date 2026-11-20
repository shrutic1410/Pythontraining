

import numpy as np
import pandas as pd

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# --------------------------------------------------

data = pd.DataFrame({
    "age": [22, 25, 30, 35, 40, 45, 50, 55],
    "income": [20000, 25000, 30000, 35000,
               40000, 45000, 50000, 55000]
})

scaler = StandardScaler()
standard_scaled = scaler.fit_transform(data)

standard_df = pd.DataFrame(
    standard_scaled,
    columns=data.columns
)

print("Original Data:")
print(data)

print("\nStandardScaler Output:")
print(standard_df)

print("\nMean after Standard Scaling:")
print(standard_df.mean())

print("\nStandard Deviation after Standard Scaling:")
print(standard_df.std(ddof=0))

# --------------------------------------------------
# 2. MinMaxScaler demonstration
# --------------------------------------------------

minmax_scaler = MinMaxScaler()
minmax_scaled = minmax_scaler.fit_transform(data)

minmax_df = pd.DataFrame(
    minmax_scaled,
    columns=data.columns
)

print("\nMinMaxScaler Output:")
print(minmax_df)

print("\nMinimum Values:")
print(minmax_df.min())

print("\nMaximum Values:")
print(minmax_df.max())

# --------------------------------------------------
# 3. Load Breast Cancer Dataset
# --------------------------------------------------

cancer = load_breast_cancer()

X = cancer.data
y = cancer.target

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# --------------------------------------------------
# 4. KNN without scaling
# --------------------------------------------------

knn_without = KNeighborsClassifier(n_neighbors=5)

knn_without.fit(X_train, y_train)

y_pred_without = knn_without.predict(X_test)

accuracy_without = accuracy_score(
    y_test, y_pred_without
)

# --------------------------------------------------
# 5. KNN with StandardScaler
# --------------------------------------------------

standard_scaler = StandardScaler()

# Fit only on training data
X_train_scaled = standard_scaler.fit_transform(X_train)

# Transform testing data using the same scaler
X_test_scaled = standard_scaler.transform(X_test)

knn_with = KNeighborsClassifier(n_neighbors=5)

knn_with.fit(X_train_scaled, y_train)

y_pred_with = knn_with.predict(X_test_scaled)

accuracy_with = accuracy_score(
    y_test, y_pred_with
)

print("\nKNN Accuracy Comparison:")
print("Without Scaling:", round(accuracy_without, 4))
print("With Scaling:", round(accuracy_with, 4))

# --------------------------------------------------
# 6. Decision Tree without scaling
# --------------------------------------------------

tree_without = DecisionTreeClassifier(random_state=42)

tree_without.fit(X_train, y_train)

tree_pred_without = tree_without.predict(X_test)

tree_accuracy_without = accuracy_score(
    y_test, tree_pred_without
)

# --------------------------------------------------
# 7. Decision Tree with scaling
# --------------------------------------------------

tree_with = DecisionTreeClassifier(random_state=42)

tree_with.fit(X_train_scaled, y_train)

tree_pred_with = tree_with.predict(X_test_scaled)

tree_accuracy_with = accuracy_score(
    y_test, tree_pred_with
)

print("\nDecision Tree Accuracy Comparison:")
print("Without Scaling:", round(tree_accuracy_without, 4))
print("With Scaling:", round(tree_accuracy_with, 4))

print("\nFinal Comparison:")
print("KNN without scaling:", round(accuracy_without, 4))
print("KNN with scaling:", round(accuracy_with, 4))
print("Decision Tree without scaling:",
      round(tree_accuracy_without, 4))
print("Decision Tree with scaling:",
      round(tree_accuracy_with, 4))
