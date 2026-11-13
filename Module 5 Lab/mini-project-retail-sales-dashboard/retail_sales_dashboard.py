"""Generate a retail sales dashboard from CSV data."""

import csv
from collections import defaultdict
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import TypeAlias

Sale: TypeAlias = dict[str, object]
SAMPLE_FILE = Path(__file__).with_name("sample_sales.csv")
DEFAULT_OUTPUT = Path(__file__).with_name("retail_sales_dashboard.png")
REQUIRED_FIELDS = {"date", "product", "category", "quantity", "unit_price", "channel"}


def load_sales(file_path: Path) -> list[Sale]:
    """Load and validate sales records from a CSV file."""
    sales: list[Sale] = []
    with file_path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        if not reader.fieldnames or not REQUIRED_FIELDS.issubset(reader.fieldnames):
            raise ValueError("CSV file is missing one or more required columns.")

        for row_number, row in enumerate(reader, start=2):
            try:
                sale_date = date.fromisoformat(row["date"].strip())
                quantity = int(row["quantity"])
                unit_price = Decimal(row["unit_price"])
            except (ValueError, InvalidOperation, AttributeError) as error:
                raise ValueError(f"Invalid data on CSV row {row_number}.") from error
            product = row["product"].strip()
            category = row["category"].strip()
            channel = row["channel"].strip()
            if quantity <= 0 or unit_price < 0 or not unit_price.is_finite():
                raise ValueError(f"Invalid quantity or price on CSV row {row_number}.")
            if not product or not category or not channel:
                raise ValueError(f"Blank text field on CSV row {row_number}.")
            sales.append(
                {
                    "date": sale_date,
                    "product": product,
                    "category": category,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "channel": channel,
                }
            )
    if not sales:
        raise ValueError("The CSV file contains no sales records.")
    return sales


def aggregate_sales(sales: list[Sale]) -> dict[str, dict[str, Decimal | int]]:
    """Aggregate revenue and quantities for dashboard charts."""
    monthly_revenue: defaultdict[str, Decimal] = defaultdict(Decimal)
    category_revenue: defaultdict[str, Decimal] = defaultdict(Decimal)
    product_quantity: defaultdict[str, int] = defaultdict(int)
    channel_revenue: defaultdict[str, Decimal] = defaultdict(Decimal)

    for sale in sales:
        sale_date = sale["date"]
        quantity = sale["quantity"]
        revenue = sale["unit_price"] * quantity
        month = sale_date.strftime("%Y-%m")
        monthly_revenue[month] += revenue
        category_revenue[sale["category"]] += revenue
        product_quantity[sale["product"]] += quantity
        channel_revenue[sale["channel"]] += revenue

    return {
        "monthly_revenue": dict(sorted(monthly_revenue.items())),
        "category_revenue": dict(
            sorted(category_revenue.items(), key=lambda item: item[1], reverse=True)
        ),
        "product_quantity": dict(
            sorted(product_quantity.items(), key=lambda item: item[1], reverse=True)
        ),
        "channel_revenue": dict(
            sorted(channel_revenue.items(), key=lambda item: item[1], reverse=True)
        ),
    }


def create_dashboard(
    aggregates: dict[str, dict[str, Decimal | int]], output_path: Path
) -> None:
    """Create and save a four-panel Matplotlib dashboard."""
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as error:
        raise RuntimeError(
            'Matplotlib is required. Run: pip install -r "Module 5 Lab/requirements.txt"'
        ) from error

    figure, axes = plt.subplots(2, 2, figsize=(14, 9))
    figure.suptitle("Retail Sales Dashboard", fontsize=18, fontweight="bold")

    months = list(aggregates["monthly_revenue"])
    monthly_values = [float(value) for value in aggregates["monthly_revenue"].values()]
    axes[0, 0].plot(months, monthly_values, marker="o", color="#2563eb", linewidth=2)
    axes[0, 0].set_title("Monthly Revenue")
    axes[0, 0].set_ylabel("Revenue")
    axes[0, 0].grid(alpha=0.25)

    categories = list(aggregates["category_revenue"])
    category_values = [float(value) for value in aggregates["category_revenue"].values()]
    axes[0, 1].bar(categories, category_values, color="#0f766e")
    axes[0, 1].set_title("Revenue by Category")
    axes[0, 1].set_ylabel("Revenue")

    products = list(aggregates["product_quantity"])
    product_values = list(aggregates["product_quantity"].values())
    axes[1, 0].barh(products[::-1], product_values[::-1], color="#d97706")
    axes[1, 0].set_title("Units Sold by Product")
    axes[1, 0].set_xlabel("Units")

    channels = list(aggregates["channel_revenue"])
    channel_values = [float(value) for value in aggregates["channel_revenue"].values()]
    axes[1, 1].pie(
        channel_values,
        labels=channels,
        autopct="%1.1f%%",
        startangle=90,
        colors=["#7c3aed", "#db2777", "#0891b2", "#65a30d"],
    )
    axes[1, 1].set_title("Revenue by Sales Channel")

    figure.tight_layout(rect=(0, 0, 1, 0.96))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close(figure)


def main() -> None:
    """Read input and output paths, then generate the dashboard."""
    raw_input = input(
        f"Enter sales CSV path or press Enter for {SAMPLE_FILE.name}: "
    ).strip().strip('"')
    raw_output = input(
        f"Enter output image path or press Enter for {DEFAULT_OUTPUT.name}: "
    ).strip().strip('"')
    input_path = Path(raw_input).expanduser() if raw_input else SAMPLE_FILE
    output_path = Path(raw_output).expanduser() if raw_output else DEFAULT_OUTPUT

    try:
        sales = load_sales(input_path)
        aggregates = aggregate_sales(sales)
        create_dashboard(aggregates, output_path)
    except FileNotFoundError:
        print(f"Sales file not found: {input_path}")
        return
    except (ValueError, PermissionError, UnicodeError, OSError, RuntimeError) as error:
        print(f"Unable to create dashboard: {error}")
        return
    print(f"Dashboard created successfully: {output_path.resolve()}")


if __name__ == "__main__":
    main()
