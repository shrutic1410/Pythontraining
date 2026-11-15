import pandas as pd
import numpy as np

# 1. Create employees.csv and load it
csv_data = """id,name,department,salary,city
1,Arun,Sales,30000,Chennai
2,Priya,HR,45000,Chennai
3,Rahul,IT,60000,Bangalore
4,Divya,IT,75000,Chennai
5,Karthik,Finance,90000,Mumbai
6,Meena,Sales,52000,Bangalore
7,Suresh,IT,68000,Chennai
8,Anitha,HR,48000,Mumbai"""

with open("employees.csv", "w") as file:
  file.write(csv_data)

df = pd.read_csv("employees.csv")

# 2. Inspect the DataFrame
print("--- HEAD ---")
print(df.head()) 
# df.head() displays the first 5 rows of the dataset (from Arun to Karthik), allowing you to quickly verify column headers and sample data formatting.

print("\n--- INFO ---")
df.info() # df.info() 
# summarizes the DataFrame's structure, showing 8 total rows, 5 non-null columns (no missing values), and their data types (int64 for id and salary; object for text columns).

print("\n--- DESCRIBE ---")
print(df.describe())
# df.describe() computes summary statistics for numerical columns, revealing that the average (mean) salary  is 58,500, with a minimum of 30,000 and a maximum of 90,000.

# 3. Column selection
print("\n--- NAME COLUMN ---")
print(df["name"])

print("\n--- NAME AND SALARY ---")
print(df[["name", "salary"]])

# 4. Indexing with loc and iloc
chennai_employees = df.loc[df["city"] == "Chennai", "name"].tolist()
print("\n--- ILOC SLICE ---")
print(df.iloc[0:3, 1:3])
# Refer - https://www.datacamp.com/tutorial/loc-vs-iloc

# 5. Filtering and final formatted output
high_salary_df = df[df["salary"] > 50000]
it_employees = df[df["department"] == "IT"]["name"].tolist()

print("\n--- SUMMARY OUTPUT ---")
print(f"Chennai: {', '.join(chennai_employees)}")
print(f"Salary above 50000: {len(high_salary_df)} employees")
print(f"IT department: {', '.join(it_employees)}")
