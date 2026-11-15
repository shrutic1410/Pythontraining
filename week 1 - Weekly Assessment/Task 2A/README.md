# Employee File Processing Assignment

## Project files

- `main.py` — reads the employee CSV, writes JSON and high-earner CSV files, creates and reads an Excel workbook, logs file errors, and optionally extracts PDF text.
- `employees.csv` — sample input with 5 employees; 3 earn more than 50,000.
- `requirements.txt` — packages requested in the assignment.

## 1. Create and activate a virtual environment

### Windows (PowerShell)
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:
```cmd
.venv\Scripts\activate.bat
```

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Run the program

Put `employees.csv` and `main.py` in the same folder, activate the virtual environment, then run:

```bash
python main.py
```

The program creates `employees.json`, `high_earners.csv`, and `salary.xlsx`.
It also deliberately tries to read `missing.txt` to demonstrate logged
`FileNotFoundError` handling.

## 4. PDF extraction

Put any PDF in the project folder and run `python main.py`, or provide a path:

```bash
python main.py --pdf sample.pdf
```

The program extracts page 1 and prints its first 100 characters. If no PDF is
provided or found, the PDF step is skipped with an explanatory message.

## Expected output with the supplied CSV (without a PDF)

```text
Rows read: 5 | High earners written: 3
salary.xlsx created and read back: 5 rows
ERROR - File not found: missing.txt
PDF skipped: place a PDF in this folder or run with --pdf filename.pdf
```

The exact order of the error line may appear before or after standard output
because logging writes to stderr while `print()` writes to stdout.

## Function/type-hint notes

- `read_employees(...) -> List[dict]`
- `read_file(...) -> Optional[Union[List[dict], dict]]`
- `find_employee(name: Union[int, str], employees: List[dict]) -> Optional[dict]`

`read_file` returns `None` and logs an error if the file is missing or contains
invalid JSON. It uses `logging`, not `print`, for those errors.
