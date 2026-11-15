# FastAPI Employee Service

A beginner-friendly FastAPI project implementing health, employee listing,
employee lookup, and employee creation endpoints.

## 1. Setup

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

Copy `.env.example` to `.env` if you need local configuration. `.env` is ignored
by Git and must not be committed.

## 2. Run the API

```bash
uvicorn app.main:app --reload --app-dir src
```

Open <http://127.0.0.1:8000/docs> for Swagger UI.

## 3. Run tests and coverage

```bash
pytest --cov=app --cov-report=term-missing
```

The coverage threshold is configured as 80%.

## 4. Format, lint, and install Git hooks

```bash
black .
ruff check . --fix
ruff format .
pre-commit install
pre-commit run --all-files
```

Run `pre-commit run --all-files` before committing. If a hook changes files,
stage the changes and run it again.

## 5. Git feature branch and pull request

Create the requested branch and make small, descriptive commits:

```bash
git init
git switch -c feature/employee-service
git add .
git commit -m "chore: create FastAPI employee service structure"
git add src/app/main.py src/app/data/employees.json
git commit -m "feat: add employee API endpoints"
git add tests/
git commit -m "test: cover employee API validation and responses"
git add .pre-commit-config.yaml pyproject.toml README.md
git commit -m "chore: configure coverage and pre-commit hooks"
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
git push -u origin feature/employee-service
```

Then open GitHub and create a Pull Request from `feature/employee-service`
into your default branch. A remote repository and GitHub credentials are
required to push and open the PR.
