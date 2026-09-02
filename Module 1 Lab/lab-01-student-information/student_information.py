"""Display a student's personal details and three-subject marks summary."""


def main() -> None:
    """Collect student details and print the academic summary."""
    name = input("Enter Student Name: ").strip()
    usn = input("Enter USN: ").strip()
    branch = input("Enter Branch: ").strip()
    semester = int(input("Enter Semester: "))

    mark1 = float(input("Enter Marks in Subject 1: "))
    mark2 = float(input("Enter Marks in Subject 2: "))
    mark3 = float(input("Enter Marks in Subject 3: "))

    total = mark1 + mark2 + mark3
    average = total / 3

    print("\n========== STUDENT REPORT ==========")
    print(f"Name          : {name}")
    print(f"USN           : {usn}")
    print(f"Branch        : {branch}")
    print(f"Semester      : {semester}")
    print(f"Total Marks   : {total:.2f}")
    print(f"Average Marks : {average:.2f}")
    print("====================================")


if __name__ == "__main__":
    main()
