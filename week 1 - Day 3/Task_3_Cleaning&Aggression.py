import pandas as pd

# 1. Create orders.csv and load it
csv_data = """order_id,customer_id,amount
1,101,500
2,102,
3,101,700
3,101,700
4,103,300
5,104,900"""

with open("orders.csv", "w") as f:
    f.write(csv_data)

df = pd.read_csv("orders.csv")

# 2. Check for missing values and duplicates
# Identifies 1 missing value in amount (for order_id 2) and 1 duplicate row (order_id 3).
# In pandas, isna() is used to detect missing or null values (like NaN, None, or pd.NaT) in your data. It returns a boolean mask of the same shape as your object, where True indicates a missing value and False indicates valid data. https://pandas.pydata.org/docs/reference/api/pandas.isna.html & https://www.ionos.com/digitalguide/websites/web-development/python-pandas-dataframe-isna/

missing_amount = df.isna().sum()["amount"]
duplicates_count = df.duplicated().sum()
print(f"Missing: amount {missing_amount} | Duplicates: {duplicates_count}")

# 3. Remove duplicates and fill missing amount with the median
#  Removes the duplicate row first—which ensures the median isn't skewed by repeated entries—and computes a median of 600.0 (from [500, 700, 300, 900]). -> Arrange the dataset in ascending order: 300, 500, 700, 900 => (500 + 700) / 2 = 600 
df = df.drop_duplicates().copy()
df["amount"] = pd.to_numeric(df["amount"])
median_val = df["amount"].median()
print(f"Median used: {median_val}")

# 4. Ensure proper data types
# Fills the missing value with 600, converts amount to int, and casts order_id to str.
df["amount"] = df["amount"].fillna(median_val).astype(int)
df["order_id"] = df["order_id"].astype(str)

# 5. Group by customer_id and aggregate
# Groups by customer_id to calculate each customer's total spend (total) and unique order count (orders).

result = (
    df.groupby("customer_id")
    .agg(total=("amount", "sum"), orders=("order_id", "count"))
    .reset_index()
)

print(result.to_string(index=False))
