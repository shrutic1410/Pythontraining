import json
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, ConfigDict

DATA_FILE = Path(__file__).parent / "data" / "employees.json"

app = FastAPI(title="Employee Service", version="1.0.0")


class EmployeeCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1)
    salary: float = Field(gt=0)


def load_employees() -> list[dict]:
    """Load employee records from the JSON data file."""
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_employees(employees: list[dict]) -> None:
    """Persist employee records to the JSON data file."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(employees, file, indent=2)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/employees")
def get_employees() -> list[dict]:
    return load_employees()


@app.get("/employees/{name}")
def get_employee(name: str) -> dict:
    for employee in load_employees():
        if employee["name"].casefold() == name.casefold():
            return employee
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Employee not found",
    )


@app.post("/employees", status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate) -> dict:
    employees = load_employees()
    if any(item["name"].casefold() == employee.name.casefold() for item in employees):
        raise HTTPException(status_code=409, detail="Employee already exists")

    new_employee = {
        "id": max((item.get("id", 0) for item in employees), default=0) + 1,
        "name": employee.name,
        "salary": employee.salary,
    }
    employees.append(new_employee)
    save_employees(employees)
    return new_employee
