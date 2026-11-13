"""Simulate dice rolls using Python's random module."""

import random
from collections import Counter


def roll_dice(
    dice_count: int, sides: int, random_generator: random.Random | None = None
) -> list[int]:
    """Roll dice and return each individual result."""
    if dice_count <= 0:
        raise ValueError("Number of dice must be positive.")
    if sides < 2:
        raise ValueError("Each die must have at least two sides.")
    generator = random_generator or random
    return [generator.randint(1, sides) for _ in range(dice_count)]


def simulate_rolls(
    dice_count: int,
    sides: int,
    simulation_count: int,
    random_generator: random.Random | None = None,
) -> list[int]:
    """Return the total from each simulated roll."""
    if simulation_count <= 0:
        raise ValueError("Number of simulations must be positive.")
    return [
        sum(roll_dice(dice_count, sides, random_generator))
        for _ in range(simulation_count)
    ]


def read_integer(prompt: str, minimum: int) -> int:
    """Read an integer greater than or equal to a minimum."""
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")
            continue
        if value >= minimum:
            return value
        print(f"Enter a value of at least {minimum}.")


def main() -> None:
    """Collect simulation settings and display results."""
    print("========== DICE SIMULATOR ==========")
    dice_count = read_integer("Enter number of dice: ", 1)
    sides = read_integer("Enter sides per die: ", 2)
    simulation_count = read_integer("Enter number of simulations: ", 1)
    totals = simulate_rolls(dice_count, sides, simulation_count)

    if simulation_count <= 20:
        print("\nRoll totals:", ", ".join(map(str, totals)))
    frequencies = Counter(totals)
    print("\n========== FREQUENCY SUMMARY ==========")
    print(f"{'Total':<10} Frequency")
    print("-" * 22)
    for total in range(dice_count, dice_count * sides + 1):
        print(f"{total:<10} {frequencies.get(total, 0)}")


if __name__ == "__main__":
    main()
