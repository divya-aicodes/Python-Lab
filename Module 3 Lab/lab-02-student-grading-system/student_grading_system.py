"""Create a student grade report using a dictionary of subject marks."""

PASS_MARK = 40.0


def grade_for_average(average: float) -> str:
    """Return a letter grade for an average mark."""
    if average >= 90:
        return "A+"
    if average >= 80:
        return "A"
    if average >= 70:
        return "B"
    if average >= 60:
        return "C"
    if average >= 50:
        return "D"
    return "F"


def read_positive_integer(prompt: str) -> int:
    """Read a positive integer."""
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")
            continue
        if value > 0:
            return value
        print("The value must be positive.")


def read_mark(subject: str) -> float:
    """Read a mark in the inclusive range 0 to 100."""
    while True:
        try:
            mark = float(input(f"Enter marks for {subject}: "))
        except ValueError:
            print("Please enter a valid number.")
            continue
        if 0 <= mark <= 100:
            return mark
        print("Marks must be between 0 and 100.")


def calculate_report(marks: dict[str, float]) -> dict[str, float | str]:
    """Calculate summary values for a non-empty subject-marks dictionary."""
    if not marks:
        raise ValueError("At least one subject is required.")

    total = sum(marks.values())
    average = total / len(marks)
    passed = all(mark >= PASS_MARK for mark in marks.values())
    return {
        "total": total,
        "average": average,
        "result": "PASS" if passed else "FAIL",
        "grade": grade_for_average(average) if passed else "F",
    }


def main() -> None:
    """Collect student marks and display the grade report."""
    print("========== STUDENT GRADING SYSTEM ==========")
    student_name = input("Enter student name: ").strip() or "Student"
    subject_count = read_positive_integer("Enter number of subjects: ")
    marks: dict[str, float] = {}

    while len(marks) < subject_count:
        subject = input(f"Enter subject {len(marks) + 1} name: ").strip()
        if not subject:
            print("Subject name cannot be empty.")
            continue
        if subject.casefold() in (name.casefold() for name in marks):
            print("This subject has already been entered.")
            continue
        marks[subject] = read_mark(subject)

    report = calculate_report(marks)
    print("\n================ GRADE REPORT ================")
    print(f"Student: {student_name}")
    for subject, mark in marks.items():
        print(f"{subject:<20} {mark:>6.2f}")
    print("----------------------------------------------")
    print(f"Total:   {report['total']:.2f} / {subject_count * 100}")
    print(f"Average: {report['average']:.2f}")
    print(f"Result:  {report['result']}")
    print(f"Grade:   {report['grade']}")
    print("==============================================")


if __name__ == "__main__":
    main()
