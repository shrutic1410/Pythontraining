import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

BASE_DIR = Path(__file__).resolve().parent.parent
EMPLOYEES_FILE = BASE_DIR / "employees.json"

app = FastAPI(title="Employee Service", version="1.0.0")


class EmployeeCreate(BaseModel):
    name: str = Field(min_length=1)
    salary: float = Field(gt=0)

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("name must not be empty")
        return value


def read_employees() -> list[dict]:
    if not EMPLOYEES_FILE.exists():
        return []
    with EMPLOYEES_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def write_employees(employees: list[dict]) -> None:
    with EMPLOYEES_FILE.open("w", encoding="utf-8") as file:
        json.dump(employees, file, indent=2)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/employees")
def get_employees() -> list[dict]:
    return read_employees()


@app.get("/employees/{name}")
def get_employee(name: str) -> dict:
    for employee in read_employees():
        if employee["name"].casefold() == name.casefold():
            return employee
    raise HTTPException(status_code=404, detail="Employee not found")


@app.post("/employees", status_code=201)
def create_employee(employee: EmployeeCreate) -> dict:
    employees = read_employees()
    if any(item["name"].casefold() == employee.name.casefold() for item in employees):
        raise HTTPException(status_code=409, detail="Employee already exists")
    new_employee = employee.model_dump()
    employees.append(new_employee)
    write_employees(employees)
    return new_employee
