# Mini Project: Retail Sales Dashboard

## Objective

Read retail transactions from CSV, aggregate sales without pandas, and generate a four-panel Matplotlib dashboard showing:

- Monthly revenue
- Revenue by category
- Units sold by product
- Revenue share by sales channel

A ready-to-use `sample_sales.csv` file is included.

## Install

From the `Module 5 Lab` folder:

```bash
pip install -r requirements.txt
```

## Run

```bash
python retail_sales_dashboard.py
```

Press Enter at both prompts to use the sample CSV and create `retail_sales_dashboard.png` beside the program.

## CSV columns

`date`, `product`, `category`, `quantity`, `unit_price`, and `channel` are required.
