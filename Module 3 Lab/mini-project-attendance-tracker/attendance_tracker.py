"""Track student attendance across multiple class dates."""

from datetime import date
from typing import TypeAlias

AttendanceRecord: TypeAlias = dict[str, str]
Student: TypeAlias = dict[str, str | list[AttendanceRecord]]


def read_date() -> str:
    """Read and validate a date in ISO format."""
    while True:
        value = input("Enter date (YYYY-MM-DD): ").strip()
        try:
            return date.fromisoformat(value).isoformat()
        except ValueError:
            print("Enter a valid date in YYYY-MM-DD format.")


def add_student(students: dict[str, Student]) -> None:
    """Add a student using a unique roll number."""
    roll_number = input("Enter roll number: ").strip()
    if not roll_number:
        print("Roll number cannot be empty.")
        return
    if roll_number in students:
        print("This roll number already exists.")
        return

    name = input("Enter student name: ").strip()
    if not name:
        print("Student name cannot be empty.")
        return

    students[roll_number] = {"name": name, "attendance": []}
    print("Student added successfully.")


def mark_attendance(students: dict[str, Student]) -> None:
    """Record attendance for every student on one date."""
    if not students:
        print("Add at least one student first.")
        return

    attendance_date = read_date()
    if any(
        any(record["date"] == attendance_date for record in student["attendance"])
        for student in students.values()
    ):
        print("Attendance has already been recorded for this date.")
        return

    for roll_number, student in sorted(students.items()):
        while True:
            status = input(
                f"{roll_number} - {student['name']} (P/A): "
            ).strip().upper()
            if status in {"P", "A"}:
                student["attendance"].append(
                    {"date": attendance_date, "status": status}
                )
                break
            print("Enter P for present or A for absent.")
    print("Attendance recorded successfully.")


def attendance_percentage(records: list[AttendanceRecord]) -> float:
    """Return the percentage of records marked present."""
    if not records:
        return 0.0
    present_count = sum(record["status"] == "P" for record in records)
    return present_count / len(records) * 100


def display_report(students: dict[str, Student]) -> None:
    """Display a summary report for all students."""
    if not students:
        print("No students have been added.")
        return

    print("\n================ ATTENDANCE REPORT ================")
    print(f"{'Roll No.':<12} {'Name':<22} {'Present':>7} {'Total':>7} {'Percent':>9}")
    print("-" * 61)
    for roll_number, student in sorted(students.items()):
        records = student["attendance"]
        present = sum(record["status"] == "P" for record in records)
        percentage = attendance_percentage(records)
        print(
            f"{roll_number:<12} {student['name']:<22} "
            f"{present:>7} {len(records):>7} {percentage:>8.2f}%"
        )


def display_student_history(students: dict[str, Student]) -> None:
    """Display the dated attendance history of one student."""
    roll_number = input("Enter roll number: ").strip()
    student = students.get(roll_number)
    if not student:
        print("Student not found.")
        return

    records = student["attendance"]
    print(f"\nAttendance history for {student['name']} ({roll_number})")
    if not records:
        print("No attendance has been recorded.")
        return
    for record in records:
        label = "Present" if record["status"] == "P" else "Absent"
        print(f"{record['date']}: {label}")


def main() -> None:
    """Run the attendance tracker menu."""
    students: dict[str, Student] = {}
    actions = {
        "1": add_student,
        "2": mark_attendance,
        "3": display_report,
        "4": display_student_history,
    }

    while True:
        print("\n========== ATTENDANCE TRACKER ==========")
        print("1. Add student")
        print("2. Mark attendance")
        print("3. Display class report")
        print("4. Display student history")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "5":
            print("Attendance tracker closed.")
            break
        action = actions.get(choice)
        if action:
            action(students)
        else:
            print("Invalid choice. Enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
