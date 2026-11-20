import pandas as pd
from sklearn.datasets import load_diabetes
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split

# 1. Load dataset and split 80/20
diabetes = load_diabetes()
X_train, X_test, y_train, y_test = train_test_split(
    diabetes.data, diabetes.target, test_size=0.2, random_state=42
)

# 2. Train LinearRegression and evaluate on the test set
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
y_pred_lr = lr_model.predict(X_test)

lr_mae = mean_absolute_error(y_test, y_pred_lr)
lr_rmse = root_mean_squared_error(y_test, y_pred_lr)
lr_r2 = r2_score(y_test, y_pred_lr)

print(
    f"Linear Regression -> MAE: {lr_mae:.2f}, RMSE: {lr_rmse:.2f}, R2:"
    f" {lr_r2:.2f}"
)

# 3. Build a mean-predicting baseline and evaluate on the test set
baseline_model = DummyRegressor(strategy="mean")
baseline_model.fit(X_train, y_train)
y_pred_base = baseline_model.predict(X_test)

base_mae = mean_absolute_error(y_test, y_pred_base)
base_rmse = root_mean_squared_error(y_test, y_pred_base)
base_r2 = r2_score(y_test, y_pred_base)

print(
    f"Baseline (Mean)   -> MAE: {base_mae:.2f}, RMSE: {base_rmse:.2f}, R2:"
    f" {base_r2:.2f}"
)

# 4. Generate the submission metrics table
results_df = pd.DataFrame({
    "Model": ["Baseline (Mean)", "Linear Regression"],
    "MAE": [round(base_mae, 2), round(lr_mae, 2)],
    "RMSE": [round(base_rmse, 2), round(lr_rmse, 2)],
    "R2": [round(base_r2, 2), round(lr_r2, 2)],
})

print("\nSubmission Metrics Table:")
print(results_df.to_markdown(index=False))
