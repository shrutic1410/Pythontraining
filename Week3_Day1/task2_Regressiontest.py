# Install and import libraries

import numpy as np
import pandas as pd

from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 2. Load the diabetes dataset and split into 80/20
# Load diabetes dataset
diabetes = load_diabetes()

X = diabetes.data
y = diabetes.target

# Split dataset into 80% training and 20% testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Training data size:", X_train.shape)
print("Testing data size:", X_test.shape)


#3. Train Linear Regression model

# Create Linear Regression model
model = LinearRegression()

# Train model
model.fit(X_train, y_train)

# Predict test data
y_pred = model.predict(X_test)

print("Linear Regression Model Trained Successfully")


#4. Calculate MAE, RMSE and R-Squared
# Calculate regression metrics
mae = mean_absolute_error(y_test, y_pred)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))

r2 = r2_score(y_test, y_pred)

print("Linear Regression Metrics")
print("-------------------------")
print("MAE:", mae)
print("RMSE:", rmse)
print("R-Squared:", r2)

# 5. Build baseline model
#The baseline model always predicts the mean of the training target values.
# Calculate mean of training target
mean_value = np.mean(y_train)

# Predict the same mean value for every test sample
baseline_pred = np.full(len(y_test), mean_value)

# Calculate baseline metrics
baseline_mae = mean_absolute_error(y_test, baseline_pred)

baseline_rmse = np.sqrt(
    mean_squared_error(y_test, baseline_pred)
)

baseline_r2 = r2_score(y_test, baseline_pred)

print("Baseline Model Metrics")
print("-----------------------")
print("MAE:", baseline_mae)
print("RMSE:", baseline_rmse)
print("R-Squared:", baseline_r2)


#6. Compare both models using a metrics table
# Create comparison table
results = pd.DataFrame({
    "Model": ["Baseline", "Linear Regression"],
    "MAE": [baseline_mae, mae],
    "RMSE": [baseline_rmse, rmse],
    "R2": [baseline_r2, r2]
})

print(results.to_string(index=False))