"""Manage employee payroll records in a CSV file."""

import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import TypeAlias

Employee: TypeAlias = dict[str, str]
DATA_FILE = Path(__file__).with_name("payroll.csv")
FIELDNAMES = [
    "employee_id",
    "name",
    "basic_salary",
    "allowance_percent",
    "deduction_percent",
]


def load_employees(file_path: Path = DATA_FILE) -> list[Employee]:
    """Load employee records from a CSV file."""
    if not file_path.exists():
        return []
    with file_path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames != FIELDNAMES:
            raise ValueError("The payroll CSV header is invalid.")
        return [{field: row[field] for field in FIELDNAMES} for row in reader]


def save_employees(employees: list[Employee], file_path: Path = DATA_FILE) -> None:
    """Save payroll records atomically to CSV."""
    temporary_file = file_path.with_suffix(file_path.suffix + ".tmp")
    with temporary_file.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(employees)
    temporary_file.replace(file_path)


def read_nonnegative_decimal(prompt: str) -> Decimal:
    """Read a non-negative decimal number."""
    while True:
        try:
            value = Decimal(input(prompt).strip())
        except InvalidOperation:
            print("Please enter a valid number.")
            continue
        if value.is_finite() and value >= 0:
            return value
        print("Enter a non-negative finite number.")


def calculate_pay(employee: Employee) -> tuple[Decimal, Decimal, Decimal]:
    """Return gross pay, deduction, and net pay."""
    basic_salary = Decimal(employee["basic_salary"])
    allowance = basic_salary * Decimal(employee["allowance_percent"]) / 100
    gross_pay = basic_salary + allowance
    deduction = gross_pay * Decimal(employee["deduction_percent"]) / 100
    return gross_pay, deduction, gross_pay - deduction


def add_employee(employees: list[Employee]) -> bool:
    """Add an employee and return whether data changed."""
    employee_id = input("Enter employee ID: ").strip()
    if not employee_id:
        print("Employee ID cannot be empty.")
        return False
    if any(item["employee_id"].casefold() == employee_id.casefold() for item in employees):
        print("This employee ID already exists.")
        return False

    name = input("Enter employee name: ").strip()
    if not name:
        print("Employee name cannot be empty.")
        return False
    basic_salary = read_nonnegative_decimal("Enter basic salary: ")
    allowance_percent = read_nonnegative_decimal("Enter allowance percentage: ")
    deduction_percent = read_nonnegative_decimal("Enter deduction percentage: ")
    if deduction_percent > 100:
        print("Deduction percentage cannot exceed 100.")
        return False

    employees.append(
        {
            "employee_id": employee_id,
            "name": name,
            "basic_salary": str(basic_salary),
            "allowance_percent": str(allowance_percent),
            "deduction_percent": str(deduction_percent),
        }
    )
    print("Employee added successfully.")
    return True


def delete_employee(employees: list[Employee]) -> bool:
    """Delete an employee and return whether data changed."""
    employee_id = input("Enter employee ID to delete: ").strip().casefold()
    employee = next(
        (item for item in employees if item["employee_id"].casefold() == employee_id),
        None,
    )
    if not employee:
        print("Employee not found.")
        return False
    employees.remove(employee)
    print("Employee deleted successfully.")
    return True


def display_payroll(employees: list[Employee]) -> None:
    """Display the calculated payroll report."""
    if not employees:
        print("No employee records are available.")
        return
    print("\n========================== PAYROLL REPORT ==========================")
    print(
        f"{'ID':<10} {'Name':<20} {'Basic':>11} {'Gross':>11} "
        f"{'Deduction':>11} {'Net Pay':>11}"
    )
    print("-" * 80)
    for employee in sorted(employees, key=lambda item: item["employee_id"].casefold()):
        gross, deduction, net_pay = calculate_pay(employee)
        basic = Decimal(employee["basic_salary"])
        print(
            f"{employee['employee_id']:<10} {employee['name']:<20} "
            f"{basic:>11.2f} {gross:>11.2f} {deduction:>11.2f} {net_pay:>11.2f}"
        )


def main() -> None:
    """Run the payroll management menu."""
    try:
        employees = load_employees()
    except (ValueError, PermissionError, UnicodeError, OSError) as error:
        print(f"Unable to load payroll data: {error}")
        return

    while True:
        print("\n========== PAYROLL MANAGEMENT ==========")
        print("1. Add employee")
        print("2. Delete employee")
        print("3. Display payroll report")
        print("4. Exit")
        choice = input("Enter your choice: ").strip()

        changed = False
        if choice == "1":
            changed = add_employee(employees)
        elif choice == "2":
            changed = delete_employee(employees)
        elif choice == "3":
            display_payroll(employees)
        elif choice == "4":
            print("Payroll management system closed.")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 4.")

        if changed:
            try:
                save_employees(employees)
            except (PermissionError, OSError) as error:
                print(f"Unable to save payroll data: {error}")


if __name__ == "__main__":
    main()
