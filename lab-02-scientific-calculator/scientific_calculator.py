"""Perform arithmetic operations on two user-provided numbers."""


def main() -> None:
    """Read two numbers and display the calculator results."""
    num1 = float(input("Enter First Number: "))
    num2 = float(input("Enter Second Number: "))

    print("\n========== CALCULATOR ==========")
    print(f"Addition       : {num1 + num2}")
    print(f"Subtraction    : {num1 - num2}")
    print(f"Multiplication : {num1 * num2}")

    if num2 == 0:
        print("Division       : Undefined (division by zero)")
        print("Floor Division : Undefined (division by zero)")
        print("Modulus        : Undefined (division by zero)")
    else:
        print(f"Division       : {num1 / num2}")
        print(f"Floor Division : {num1 // num2}")
        print(f"Modulus        : {num1 % num2}")

    print(f"Power          : {num1 ** num2}")
    print("================================")


if __name__ == "__main__":
    main()
