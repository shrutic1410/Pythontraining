
import pandas as pd

# --------------------------------
# 1. Create customers.csv
# --------------------------------

customers = pd.DataFrame({
    "customer_id": [101, 102, 103, 105],
    "name": ["Arun", "Priya", "Rahul", "Divya"],
    "city": ["Chennai", "Mumbai", "Chennai", "Bangalore"]
})

customers.to_csv("customers.csv", index=False)

print("Customers CSV created successfully!")

# --------------------------------
# 2. Read cleaned orders
# --------------------------------

orders = pd.read_csv("cleaned_orders.csv")
customers = pd.read_csv("customers.csv")

print("\nCleaned Orders:")
print(orders)

print("\nCustomers:")
print(customers)

# --------------------------------
# 3. INNER JOIN
# --------------------------------

inner_join = pd.merge(
    orders,
    customers,
    on="customer_id",
    how="inner"
)

print("\n--- INNER JOIN ---")
print(inner_join)

print("Inner join rows:", len(inner_join))

# --------------------------------
# 4. LEFT JOIN
# Find customers with no orders
# --------------------------------

left_join = pd.merge(
    customers,
    orders,
    on="customer_id",
    how="left",
    indicator=True
)

no_orders = left_join[left_join["_merge"] == "left_only"]

print("\n--- CUSTOMERS WITH NO ORDERS ---")
print(no_orders[["customer_id", "name_y", "city_y"]])

# --------------------------------
# 5. OUTER JOIN
# Find orders without customers
# --------------------------------

outer_join = pd.merge(
    customers,
    orders,
    on="customer_id",
    how="outer",
    indicator=True
)

unmatched_orders = outer_join[
    outer_join["_merge"] == "right_only"
]

print("\n--- ORDERS WITHOUT CUSTOMER RECORD ---")
print(unmatched_orders)

# --------------------------------
# 6. Summary
# --------------------------------

print("\n--- SUMMARY ---")
print("Inner join rows:", len(inner_join))
print("Customers without orders:", len(no_orders))
print("Orders without customers:", len(unmatched_orders))
