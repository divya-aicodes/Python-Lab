# Mini Project: JSON-Based Log File Analyzer

## Objective

Load structured application logs from JSON and produce totals by severity and source, a time range, and a detailed list of error events.

The JSON file must contain an array of objects with these string fields:

- `timestamp`: ISO 8601 date and time
- `level`: for example `INFO`, `WARNING`, `ERROR`, or `CRITICAL`
- `source`: the component that produced the event
- `message`: event details

A ready-to-use `sample_logs.json` file is included.

## Run

```bash
python json_log_analyzer.py
```

Press Enter at the file-path prompt to analyze the included sample.
