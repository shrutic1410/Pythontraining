import csv
import io
from functools import wraps

# Sample CSV data
csv_data = """name,department,salary
Arun,Sales,30000
Priya,HR,45000
Rahul,IT,60000
Divya,IT,75000
Karthik,Finance,90000"""


# 1. Decorator to log function calls
# Wraps Manager.get_details to intercept the call, print the method name via func.__name__, and execute the underlying method.  Using @functools.wraps(func) ensures func.__name__ and docstrings aren't overwritten by wrapper
# https://www.geeksforgeeks.org/python/args-kwargs-python/

def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs): # is the standard pattern used inside decorators to accept any arbitrary positional or keyword arguments passed to the wrapped function.
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


# 2. Function with default args, *args, and **kwargs
# Uses *extras as a tuple to sum additional amounts and checks the **options dictionary for a "cap" key to enforce a maximum limit.
def calculate_bonus(salary, rate=0.1, *extras, **options):
    bonus = (salary * rate) + sum(extras)
    if "cap" in options and bonus > options["cap"]:
        return options["cap"]
    return bonus


# 3. Base Employee class
# Exposes annual_salary as a computed attribute (accessible without parentheses via emp.annual_salary).
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = float(salary)

    @property
    def annual_salary(self):
        return self.salary * 12

    def get_details(self):
        return f"{self.name} - {int(self.salary)}"


# 4. Manager subclass inheriting from Employee
#  Inherits attributes from Employee via super().__init__() and extends get_details() rather than rewriting the base formatting.
class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    @log_call
    def get_details(self):
        base_details = super().get_details()
        return f"{base_details} - Team Size: {self.team_size}"


# 5. Parse CSV data and process salary categories
# Reads the CSV rows into Employee objects and classifies each salary using if / elif / else.
reader = csv.DictReader(io.StringIO(csv_data))
employees = []

for row in reader:
    emp = Employee(row["name"], row["salary"])
    employees.append(emp)

    if emp.salary < 50000:
        category = "Low Salary"
    elif emp.salary < 70000:
        category = "Medium Salary"
    else:
        category = "High Salary"

    print(f"{emp.name} - {category}")

# 6. Instantiate Manager and test decorated method
divya_manager = Manager("Divya", 75000, 5)
print(divya_manager.get_details())
