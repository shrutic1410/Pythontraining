# Employee Service API

- `GET /health` — returns `{"status": "ok"}`.
- `GET /employees` — returns all employee records from the JSON file.
- `GET /employees/{name}` — finds an employee by case-insensitive name; returns
  404 when absent.
- `POST /employees` — accepts `{"name": "Meera", "salary": 70000}`. Name must
  contain non-whitespace text and salary must be greater than zero. Returns 201.
