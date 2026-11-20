import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from sklearn.cluster import KMeans

# 1. Load dataset and split 80/20
iris = load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Supervised Learning: Logistic Regression
clf = LogisticRegression(max_iter=200)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

print("--- Logistic Regression Results ---")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print(f"F1 Score (Macro): {f1_score(y_test, y_pred, average='macro'):.4f}")
print("Confusion Matrix 3*3 with almost all the values on the diagonal:\n", confusion_matrix(y_test, y_pred))

# 3. Unsupervised Learning: K-Means Clustering
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X)
unique, counts = np.unique(clusters, return_counts=True)

print("\n--- K-Means Clustering Results ---")
print("Cluster sizes:", dict(zip(unique, counts)))

# Compare clusters against actual species
comparison = pd.crosstab(
    pd.Series(y, name='Actual Species').map(dict(enumerate(iris.target_names))),
    pd.Series(clusters, name='Cluster')
)
print("\nCluster vs. Real Species:\n", comparison)
