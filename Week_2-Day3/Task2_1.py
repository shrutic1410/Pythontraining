from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score
#load dataset
iris = load_iris()
X, y = iris.data, iris.target

#split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42,stratify=y)

#train decision tree classifier
tree = DecisionTreeClassifier(criterion="gini", max_depth=3, random_state=42)
tree.fit(X_train, y_train)
y_pred = tree.predict(X_test)

#predict and evaluate accuracy
y_pred = tree.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

#display the learned rules
print(export_text(tree, feature_names=iris.feature_names))
#
# feature importance = collection of techniques used in ml to quantify the 
#contribution of each feature to the model's predictions. It helps identify which features are most influential in making accurate predictions, allowing for better understanding and interpretation of the model's behavior.

for name, importance in zip(iris.feature_names, tree.feature_importances_):
    print(f"{name}: {importance:.3f}")