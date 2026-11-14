import csv
import json
import logging
from pathlib import Path
from typing import List, Optional, Union
import fitz
import openpyxl
import pymupdf

# Configure logging (no print statements for errors)
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def process_employees(
    input_path: Path, json_output_path: Path, high_earners_path: Path
) -> List[dict]:
    """Reads employees.csv, writes employees.json, and filters high earners."""
    employees: List[dict] = []

    with input_path.open(mode="r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            # Convert salary to int for accurate numeric comparison
            row["salary"] = int(row["salary"])
            employees.append(row)

    # Write all employees to JSON
    with json_output_path.open(mode="w", encoding="utf-8") as json_file:
        json.dump(employees, json_file, indent=4)

    # Filter high earners (salary > 50000) and write to CSV
    high_earners = [emp for emp in employees if emp["salary"] > 50000]
    if high_earners:
        fieldnames = list(high_earners[0].keys())
        with high_earners_path.open(mode="w", encoding="utf-8", newline="") as out_csv:
            writer = csv.DictWriter(out_csv, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(high_earners)

    print(f"Rows read: {len(employees)} | High earners written: {len(high_earners)}")
    return employees


def handle_excel(employees: List[dict], excel_path: Path) -> int:
    """Creates salary.xlsx using openpyxl and reads it back."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Salaries"

    if employees:
        headers = list(employees[0].keys())
        ws.append(headers)
        for emp in employees:
            ws.append(list(emp.values()))

    wb.save(excel_path)

    # Read it back (excluding header row)
    wb_read = openpyxl.load_workbook(excel_path)
    ws_read = wb_read.active
    data_rows = list(ws_read.iter_rows(min_row=2, values_only=True))
    
    print(f"{excel_path.name} created and read back: {len(data_rows)} rows")
    return len(data_rows)


def extract_pdf_preview(pdf_path: Path) -> Optional[str]:
    """Extracts text from page 1 of a PDF using PyMuPDF and prints first 100 chars."""
    if not pdf_path.exists():
        logger.warning(f"PDF file not found for preview: {pdf_path.name}")
        return None

    with fitz.open(pdf_path) as doc:
        if len(doc) > 0:
            page_text = doc[0].get_text()
            preview = page_text[:100].replace("\n", " ")
            print(f"PDF Page 1 Preview: {preview}")
            return preview
    return None


def read_file(path: Union[str, Path]) -> Optional[Union[dict, list, str]]:
    """Safely reads a file with error logging for missing files or invalid JSON."""
    file_path = Path(path)
    try:
        content = file_path.read_text(encoding="utf-8")
        if file_path.suffix == ".json":
            return json.loads(content)
        return content
    except FileNotFoundError:
        logger.error(f"File not found: {file_path.name}")
        return None
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON format in: {file_path.name}")
        return None


def find_employee(name: str, employees: List[dict]) -> Optional[dict]:
    """Searches for an employee by name (case-insensitive) and returns their record."""
    for emp in employees:
        if emp.get("name", "").lower() == name.lower():
            return emp
    return None


def main() -> None:
    base_dir = Path(".")
    csv_input = base_dir / "employees.csv"
    json_output = base_dir / "employees.json"
    high_earners_csv = base_dir / "high_earners.csv"
    excel_output = base_dir / "salary.xlsx"
    sample_pdf = base_dir / "sample.pdf"

    # 1. Process CSV & JSON
    employees_data = process_employees(csv_input, json_output, high_earners_csv)

    # 2. Process Excel
    handle_excel(employees_data, excel_output)

    # 3. Extract PDF text (runs if sample.pdf is present)
    extract_pdf_preview(sample_pdf)

    # 4. Trigger FileNotFoundError to match Expected Output
    read_file("missing.txt")

    # 5. Demonstrate find_employee
    _ = find_employee("Alice", employees_data)


if __name__ == "__main__":
    main()
