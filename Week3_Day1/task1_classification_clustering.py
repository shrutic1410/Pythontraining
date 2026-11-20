
# Task 1: Classification and Clustering

# Import required libraries
import numpy as np
import pandas as pd

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from sklearn.cluster import KMeans

# -------------------------------------------------
# STEP 1: Load the Iris Dataset
# -------------------------------------------------

iris = load_iris()

X = iris.data
y = iris.target

print("Dataset loaded successfully!")
print("Features:", iris.feature_names)
print("Target classes:", iris.target_names)
print("Dataset shape:", X.shape)

# -------------------------------------------------
# STEP 2: Split Dataset into 80% Training and 20% Testing
# -------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining data size:", X_train.shape)
print("Testing data size:", X_test.shape)

# -------------------------------------------------
# STEP 3: Train Logistic Regression (Supervised)
# -------------------------------------------------

model = LogisticRegression(max_iter=200)

model.fit(X_train, y_train)

# Predict test data
y_pred = model.predict(X_test)

# Calculate accuracy and F1 score
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average="macro")

print("\n--- Logistic Regression Results ---")
print("Accuracy:", round(accuracy, 2))
print("F1 Score (macro):", round(f1, 2))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:")
print(cm)

# -------------------------------------------------
# STEP 4: KMeans Clustering (Unsupervised)
# -------------------------------------------------

kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

# Use features only, without labels
clusters = kmeans.fit_predict(X)

# Print cluster sizes
cluster_sizes = np.bincount(clusters)

print("\n--- KMeans Clustering Results ---")
print("Cluster sizes:", cluster_sizes)

# -------------------------------------------------
# STEP 5: Compare Clusters with Real Species
# -------------------------------------------------

comparison = pd.crosstab(
    pd.Series(clusters, name="KMeans Cluster"),
    pd.Series(
        iris.target_names[y],
        name="Actual Species"
    )
)

print("\n--- Cluster vs Actual Species ---")
print(comparison)

print("\n--- Observations ---")
print("1. KMeans groups flowers based on similarities in their features.")
print("2. Some clusters correspond closely to actual Iris species.")
print("3. Some overlap occurs because different species can have similar measurements.")

# -------------------------------------------------
# STEP 6: Supervised vs Unsupervised Learning
# -------------------------------------------------

print("\n--- Supervised vs Unsupervised Learning ---")
print("1. Logistic Regression requires labelled data to learn the relationship")
print("   between flower features and their species.")
print("2. KMeans does not require labelled data because it groups similar")
print("   data points based on their features.")
