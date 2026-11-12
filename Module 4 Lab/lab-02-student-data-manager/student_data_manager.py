"""Manage student records stored in a tab-separated text file."""

from pathlib import Path
from typing import TypeAlias

Student: TypeAlias = dict[str, str]
DATA_FILE = Path(__file__).with_name("students.txt")


def load_students(file_path: Path = DATA_FILE) -> list[Student]:
    """Load valid student records from a text file."""
    if not file_path.exists():
        return []

    students: list[Student] = []
    for line in file_path.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) == 3:
            roll_number, name, course = parts
            students.append(
                {"roll_number": roll_number, "name": name, "course": course}
            )
    return students


def save_students(students: list[Student], file_path: Path = DATA_FILE) -> None:
    """Save records atomically to a tab-separated text file."""
    lines = [
        "\t".join((student["roll_number"], student["name"], student["course"]))
        for student in students
    ]
    temporary_file = file_path.with_suffix(file_path.suffix + ".tmp")
    temporary_file.write_text(
        "\n".join(lines) + ("\n" if lines else ""), encoding="utf-8"
    )
    temporary_file.replace(file_path)


def find_student(students: list[Student], roll_number: str) -> Student | None:
    """Return a student matching a roll number."""
    normalized_roll = roll_number.strip().casefold()
    return next(
        (
            student
            for student in students
            if student["roll_number"].casefold() == normalized_roll
        ),
        None,
    )


def read_field(prompt: str, current_value: str | None = None) -> str:
    """Read a non-empty field that does not contain a tab."""
    while True:
        suffix = f" [{current_value}]" if current_value is not None else ""
        value = input(f"{prompt}{suffix}: ").strip()
        if current_value is not None and not value:
            return current_value
        if value and "\t" not in value:
            return value
        print("Enter a non-empty value without tab characters.")


def add_student(students: list[Student]) -> bool:
    """Add a student and return whether data changed."""
    roll_number = read_field("Enter roll number")
    if find_student(students, roll_number):
        print("This roll number already exists.")
        return False
    students.append(
        {
            "roll_number": roll_number,
            "name": read_field("Enter student name"),
            "course": read_field("Enter course"),
        }
    )
    print("Student added successfully.")
    return True


def search_student(students: list[Student]) -> None:
    """Search for and display one student."""
    student = find_student(students, input("Enter roll number to search: "))
    if student:
        print(
            f"Roll Number: {student['roll_number']}\n"
            f"Name: {student['name']}\nCourse: {student['course']}"
        )
    else:
        print("Student not found.")


def update_student(students: list[Student]) -> bool:
    """Update a student and return whether data changed."""
    student = find_student(students, input("Enter roll number to update: "))
    if not student:
        print("Student not found.")
        return False
    student["name"] = read_field("Enter student name", student["name"])
    student["course"] = read_field("Enter course", student["course"])
    print("Student updated successfully.")
    return True


def delete_student(students: list[Student]) -> bool:
    """Delete a student and return whether data changed."""
    student = find_student(students, input("Enter roll number to delete: "))
    if not student:
        print("Student not found.")
        return False
    students.remove(student)
    print("Student deleted successfully.")
    return True


def display_students(students: list[Student]) -> None:
    """Display all student records."""
    if not students:
        print("No student records are available.")
        return
    print("\n================ STUDENT RECORDS ================")
    print(f"{'Roll Number':<16} {'Name':<25} Course")
    print("-" * 62)
    for student in sorted(students, key=lambda item: item["roll_number"].casefold()):
        print(
            f"{student['roll_number']:<16} {student['name']:<25} "
            f"{student['course']}"
        )


def main() -> None:
    """Run the student data manager menu."""
    try:
        students = load_students()
    except (PermissionError, UnicodeError, OSError) as error:
        print(f"Unable to load student data: {error}")
        return

    while True:
        print("\n========== STUDENT DATA MANAGER ==========")
        print("1. Add student")
        print("2. Search student")
        print("3. Update student")
        print("4. Delete student")
        print("5. Display all students")
        print("6. Exit")
        choice = input("Enter your choice: ").strip()

        changed = False
        if choice == "1":
            changed = add_student(students)
        elif choice == "2":
            search_student(students)
        elif choice == "3":
            changed = update_student(students)
        elif choice == "4":
            changed = delete_student(students)
        elif choice == "5":
            display_students(students)
        elif choice == "6":
            print("Student data manager closed.")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 6.")

        if changed:
            try:
                save_students(students)
            except (PermissionError, OSError) as error:
                print(f"Unable to save student data: {error}")


if __name__ == "__main__":
    main()
