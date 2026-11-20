
# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt

from xgboost import XGBClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

# Load Breast Cancer Dataset
data = load_breast_cancer()

X = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target

# Split dataset into training and testing sets
X_train_full, X_test, y_train_full, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Split training data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(
    X_train_full,
    y_train_full,
    test_size=0.2,
    random_state=42,
    stratify=y_train_full
)

# Different learning rates and number of trees
experiments = [
    (0.3, 100),
    (0.1, 200),
    (0.03, 500)
]

results = []
models = {}

# Train XGBoost models
for learning_rate, n_estimators in experiments:

    print("\nLearning Rate:", learning_rate)

    model = XGBClassifier(
        n_estimators=n_estimators,
        learning_rate=learning_rate,
        max_depth=3,
        random_state=42,
        eval_metric="logloss",
        early_stopping_rounds=20
    )

    # Train with validation set
    model.fit(
        X_train,
        y_train,
        eval_set=[(X_val, y_val)],
        verbose=False
    )

    # Predict test data
    y_pred = model.predict(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)

    # Best iteration
    best_iteration = model.best_iteration

    results.append({
        "Learning Rate": learning_rate,
        "Best Iteration": best_iteration,
        "Test Accuracy": accuracy
    })

    models[learning_rate] = model

    print("Best Iteration:", best_iteration)
    print("Test Accuracy:", accuracy)

# Display comparison table
results_df = pd.DataFrame(results)

print("\nXGBoost Model Comparison")
print(results_df.to_string(index=False))

# Find best model based on test accuracy
best_result = results_df.loc[results_df["Test Accuracy"].idxmax()]
best_lr = best_result["Learning Rate"]

best_model = models[best_lr]

print("\nBest Learning Rate:", best_lr)
print("Best Iteration:", best_result["Best Iteration"])
print("Best Test Accuracy:", best_result["Test Accuracy"])

# Feature Importance
importance = pd.Series(
    best_model.feature_importances_,
    index=X.columns
).sort_values(ascending=False)

print("\nTop 10 Important Features:")
print(importance.head(10))

# Plot Feature Importance
plt.figure(figsize=(10, 6))

importance.head(10).sort_values().plot(
    kind="barh"
)

plt.title("XGBoost Feature Importance")
plt.xlabel("Importance Score")
plt.ylabel("Features")
plt.tight_layout()
plt.show()

# Compare with Random Forest
rf_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

rf_model.fit(X_train_full, y_train_full)

rf_pred = rf_model.predict(X_test)

rf_accuracy = accuracy_score(y_test, rf_pred)

print("\nRandom Forest Accuracy:", rf_accuracy)
print("Best XGBoost Accuracy:", best_result["Test Accuracy"])
