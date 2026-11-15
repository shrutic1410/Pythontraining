from __future__ import annotations

import argparse
import csv
import json
import logging
from pathlib import Path
from typing import List, Optional, Union

import fitz  # PyMuPDF
from openpyxl import Workbook, load_workbook

# Log errors to the console. The requested missing-file example will therefore
# produce a line such as: ERROR - File not found: missing.txt
logging.basicConfig(level=logging.ERROR, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

Employee = dict


def read_employees(path: Union[str, Path]) -> List[dict]:
    """Read employee records from a CSV file."""
    employees: List[dict] = []

    with Path(path).open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            # Convert salary to a number so comparisons and Excel values work.
            row["salary"] = float(row["salary"])
            employees.append(row)

    return employees


def write_employee_json(employees: List[dict], path: Union[str, Path]) -> None:
    """Write all employee records to a JSON file."""
    with Path(path).open("w", encoding="utf-8") as json_file:
        json.dump(employees, json_file, indent=4)


def write_high_earners(
    employees: List[dict], path: Union[str, Path], threshold: int = 50000
) -> List[dict]:
    """Write employees whose salary is above the threshold to a CSV file."""
    high_earners = [
        employee for employee in employees if employee["salary"] > threshold
    ]

    if high_earners:
        with Path(path).open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=list(high_earners[0].keys()))
            writer.writeheader()
            writer.writerows(high_earners)
    else:
        # Still create a valid empty file with the employee column headings.
        with Path(path).open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(
                csv_file, fieldnames=list(employees[0].keys()) if employees else []
            )
            if employees:
                writer.writeheader()

    return high_earners


def create_and_read_excel(employees: List[dict], path: Union[str, Path]) -> int:
    """Create salary.xlsx, then reopen it and return its employee row count."""
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Salaries"

    headers = list(employees[0].keys()) if employees else ["id", "name", "department", "salary"]
    sheet.append(headers)

    for employee in employees:
        sheet.append([employee.get(header) for header in headers])

    workbook.save(path)

    # Read the workbook back, as required by the assignment.
    read_workbook = load_workbook(path, data_only=True)
    read_sheet = read_workbook["Salaries"]
    row_count = max(read_sheet.max_row - 1, 0)  # Exclude the header row.
    read_workbook.close()

    return row_count


def extract_first_page_text(pdf_path: Union[str, Path]) -> str:
    """Extract and return the text from page 1 of a PDF."""
    with fitz.open(pdf_path) as pdf_document:
        if pdf_document.page_count == 0:
            return ""
        first_page = pdf_document.load_page(0)
        return first_page.get_text()


def read_file(path: Union[str, Path]) -> Optional[Union[List[dict], dict]]:
    """
    Read JSON data from a file.

    FileNotFoundError and JSONDecodeError are logged rather than printed.
    Returns None when either error occurs.
    """
    try:
        with Path(path).open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error("File not found: %s", path)
    except json.JSONDecodeError as error:
        logger.error("Invalid JSON in %s: %s", path, error)

    return None


def find_employee(name: Union[int, str], employees: List[dict]) -> Optional[dict]:
    """Find an employee by name (case-insensitive); return None if not found."""
    search_name = str(name).casefold()
    for employee in employees:
        if employee.get("name", "").casefold() == search_name:
            return employee
    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Process employee CSV, JSON, Excel, and optional PDF files."
    )
    parser.add_argument(
        "--pdf",
        type=str,
        default=None,
        help="Optional PDF file; its first page's first 100 characters are printed.",
    )
    args = parser.parse_args()

    employees = read_employees("employees.csv")
    write_employee_json(employees, "employees.json")
    high_earners = write_high_earners(employees, "high_earners.csv", 50000)
    excel_rows = create_and_read_excel(employees, "salary.xlsx")

    print(f"Rows read: {len(employees)} | High earners written: {len(high_earners)}")
    print(f"salary.xlsx created and read back: {excel_rows} rows")

    # Demonstrate the required FileNotFoundError logging behaviour.
    read_file("missing.txt")

    # Extract PDF page 1 if a PDF was supplied or one exists in this folder.
    pdf_path = Path(args.pdf) if args.pdf else next(Path(".").glob("*.pdf"), None)
    if pdf_path is not None:
        try:
            page_text = extract_first_page_text(pdf_path)
            print(f"PDF first 100 characters: {page_text[:100]}")
        except FileNotFoundError:
            logger.error("PDF file not found: %s", pdf_path)
        except (fitz.FileDataError, RuntimeError) as error:
            logger.error("Could not read PDF %s: %s", pdf_path, error)
    else:
        print("PDF skipped: place a PDF in this folder or run with --pdf filename.pdf")


if __name__ == "__main__":
    main()
