# Lab 4: Electricity Bill Generator

## Objective

Create a formatted residential electricity bill from consumer details and meter readings.

## Calculations

- Units consumed = current reading - previous reading
- Energy charge = units consumed x cost per unit
- Electricity duty = 5% of energy charge
- Fixed meter charge = INR 100
- Net bill = energy charge + electricity duty + fixed meter charge

The current meter reading must not be lower than the previous reading.

## Run

```bash
python electricity_bill.py
```
