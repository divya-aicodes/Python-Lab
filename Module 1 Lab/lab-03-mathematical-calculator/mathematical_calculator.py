"""Demonstrate operators, built-in functions, and the math module."""

import math


def main() -> None:
    """Read a floating-point number and display mathematical results."""
    number = float(input("Enter a number: "))

    print("\n========== MATHEMATICAL OPERATIONS ==========")
    print(f"Number         : {number}")
    print(f"Square         : {number ** 2}")
    print(f"Cube           : {number ** 3}")

    if number < 0:
        print("Square Root    : Undefined for negative real numbers")
    else:
        print(f"Square Root    : {math.sqrt(number)}")

    print(f"Ceiling Value  : {math.ceil(number)}")
    print(f"Floor Value    : {math.floor(number)}")
    print(f"Absolute Value : {abs(number)}")
    print(f"Type           : {type(number)}")
    print(f"Memory Address : {id(number)}")
    print("=============================================")


if __name__ == "__main__":
    main()
