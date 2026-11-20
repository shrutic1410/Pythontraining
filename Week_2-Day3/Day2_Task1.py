
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score

# 1. Load Wine dataset
wine = load_wine()
X = pd.DataFrame(wine.data, columns=wine.feature_names)
y = wine.target

# 2. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# 3. Hyperparameter tuning
param_grid = {
    "max_depth": [2, 3, 4, 5, None],
    "min_samples_leaf": [1, 2, 4, 6, 8]
}

results = []
models = {}

for criterion in ["gini", "entropy"]:

    grid = GridSearchCV(
        DecisionTreeClassifier(
            criterion=criterion,
            random_state=42
        ),
        param_grid,
        cv=5,
        scoring="accuracy",
        n_jobs=-1
    )

    grid.fit(X_train, y_train)

    best_model = grid.best_estimator_
    models[criterion] = best_model

    y_pred = best_model.predict(X_test)

    results.append({
        "criterion": criterion,
        "max_depth": best_model.max_depth,
        "min_samples_leaf": best_model.min_samples_leaf,
        "CV Accuracy": grid.best_score_,
        "Test Accuracy": accuracy_score(y_test, y_pred)
    })

# 4. Compare models
comparison = pd.DataFrame(results)

print("\nModel Comparison:")
print(comparison)

# 5. Select best model
best_criterion = (
    comparison.sort_values(
        "CV Accuracy",
        ascending=False
    ).iloc[0]["criterion"]
)

best_model = models[best_criterion]

print("\nBest Model:", best_criterion)
print("Best Parameters:", {
    "max_depth": best_model.max_depth,
    "min_samples_leaf": best_model.min_samples_leaf
})

y_pred = best_model.predict(X_test)

print("Test Accuracy:",
      accuracy_score(y_test, y_pred))

# 6. Plot decision tree
plt.figure(figsize=(22, 12))

plot_tree(
    best_model,
    feature_names=wine.feature_names,
    class_names=wine.target_names,
    filled=True,
    rounded=True,
    max_depth=3,
    fontsize=8
)

plt.title("Wine Decision Tree Classification")
plt.savefig(
    "wine_decision_tree.png",
    dpi=200,
    bbox_inches="tight"
)
plt.show()

# 7. Explain first two levels of splits
tree = best_model.tree_

def show_split(node, description):
    feature = tree.feature[node]

    if feature >= 0:
        print(
            description,
            wine.feature_names[feature],
            "<=",
            round(tree.threshold[node], 3)
        )
    else:
        print(description, "Leaf node")

print("\nFirst Splits:")

show_split(0, "Root split:")

show_split(
    tree.children_left[0],
    "Left branch split:"
)

show_split(
    tree.children_right[0],
    "Right branch split:"
)

# 8. Feature importance
importance = pd.DataFrame({
    "Feature": wine.feature_names,
    "Importance": best_model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\nTop 5 Important Features:")
print(importance.head(5).to_string(index=False))

importance.head(5).to_csv(
    "top_5_feature_importances.csv",
    index=False
)
