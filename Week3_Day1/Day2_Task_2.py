
import pandas as pd

from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# Load Wine dataset
wine = load_wine()
X, y = wine.data, wine.target


X_train, X_test, y_train, y_test = train_test_split(X, y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

rf = RandomForestClassifier(
    n_estimators=200,
    oob_score=True,
    random_state=42)

rf.fit(X_train, y_train)

rf_pred = rf.predict(X_test)
rf_accuracy = accuracy_score(y_test, rf_pred)

# Step 5: Print accuracy comparison
#print("Single Tree Test Accuracy:", round(dt_accuracy, 2))
#print("Single Tree Test Accuracy:", round(dt_accuracy, 2))

print("Random Forest Test Accuracy:", round(rf_accuracy, 2))
print("OOB Score:", round(rf.oob_score_, 2))

# Step 6: Try different numbers of estimators
estimators = [10, 50, 100, 300]
accuracies = []

for n in estimators:

    model = RandomForestClassifier(
        n_estimators=n,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    accuracies.append(accuracy)

    print(f"Number of Trees: {n}, Accuracy: {accuracy:.2f}")
