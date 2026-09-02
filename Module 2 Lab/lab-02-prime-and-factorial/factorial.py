"""Calculate the factorial of a non-negative integer."""


def factorial(number: int) -> int:
    """Return number factorial, raising ValueError for negative input."""
    if number < 0:
        raise ValueError("Factorial is not defined for negative integers.")

    result = 1
    for value in range(2, number + 1):
        result *= value
    return result


def main() -> None:
    """Read a non-negative integer and display its factorial."""
    number = int(input("Enter a non-negative integer: "))

    if number < 0:
        print("Factorial is not defined for negative integers.")
        return

    print(f"Factorial of {number} is {factorial(number)}.")


if __name__ == "__main__":
    main()
