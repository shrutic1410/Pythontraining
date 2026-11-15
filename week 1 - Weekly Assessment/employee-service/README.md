# Employee Service

A small FastAPI CRUD-style service backed by `employees.json`.

## Setup

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
```

## Run the API

```bash
uvicorn src.main:app --reload
```

Open the interactive API docs at http://127.0.0.1:8000/docs.

## Endpoints

- `GET /health` -> `{"status": "ok"}`
- `GET /employees` -> list of employees
- `GET /employees/{name}` -> employee, or 404 when missing
- `POST /employees` -> create employee; `name` must not be blank and `salary` must be greater than zero

Example POST body:

```json
{"name": "Ravi", "salary": 70000}
```

## Tests and coverage

```bash
pytest -q --cov=src --cov-report=term-missing
```

The project is configured to fail coverage below 80%.

## Pre-commit

```bash
pre-commit install
pre-commit run --all-files
```

## Suggested Git workflow

Run these commands from the project directory. Replace the remote URL with your own GitHub repository URL.

```bash
git init
git switch -c feature/employee-service
git add .gitignore requirements.txt pyproject.toml README.md employees.json
git commit -m "chore: initialize employee service project"

git add src/
git commit -m "feat: add employee API endpoints and validation"

git add tests/
git commit -m "test: add employee API coverage"

git add .pre-commit-config.yaml
git commit -m "chore: configure black and ruff pre-commit hooks"

pre-commit install
pre-commit run --all-files
pytest -q --cov=src --cov-report=term-missing

git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin feature/employee-service
```

Then open GitHub, select **Compare & pull request**, set the base branch to `main`,
and create the PR titled `Add FastAPI employee service`.
