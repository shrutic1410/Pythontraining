"""
Task 1 - Charts with Matplotlib
Place employees.csv in the same folder as this script, then run:
    python charts.py

Creates four PNG files in the current folder.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = Path("employees.csv")
OUTPUT_DIR = Path("./week 1 - Day 4/Task_1_Charts_Matplotlib/charts_output")

def main():
    df = pd.read_csv(DATA_FILE)
    df.columns = [column.strip() for column in df.columns]

    required = {"id", "department", "salary"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    # 1. Bar chart: average salary per department
    avg_salary = df.groupby("department")["salary"].mean()
    ax = avg_salary.plot(kind="bar", figsize=(8, 5), title="Average Salary by Department")
    ax.set_xlabel("Department")
    ax.set_ylabel("Average Salary")
    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", padding=3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "1_average_salary_by_department.png", dpi=150)
    plt.close()

    # 2. Histogram: salary distribution with 5 bins
    plt.figure(figsize=(8, 5))
    plt.hist(df["salary"], bins=5, edgecolor="black")
    plt.title("Distribution of Employee Salaries")
    plt.xlabel("Salary")
    plt.ylabel("Number of Employees")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "2_salary_histogram.png", dpi=150)
    plt.close()

    # 3. Scatter plot: employee ID vs salary, colored by department
    plt.figure(figsize=(8, 5))
    for department, group in df.groupby("department"):
        plt.scatter(group["id"], group["salary"], label=department, s=85)
    plt.title("Employee ID vs Salary by Department")
    plt.xlabel("Employee ID")
    plt.ylabel("Salary")
    plt.legend(title="Department")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "3_id_vs_salary_scatter.png", dpi=150)
    plt.close()

    # 4. Line chart: monthly sales from January to June
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    sales = [12, 15, 14, 18, 22, 25]
    plt.figure(figsize=(8, 5))
    plt.plot(months, sales, marker="o", linewidth=2)
    plt.title("Monthly Sales (January to June)")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "4_monthly_sales_line.png", dpi=150)
    plt.close()

    print("All 4 charts saved as PNG files.")

if __name__ == "__main__":
    main()
