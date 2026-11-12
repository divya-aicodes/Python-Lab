"""Analyze structured application logs stored in a JSON file."""

import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import TypeAlias

LogEntry: TypeAlias = dict[str, str]
SAMPLE_FILE = Path(__file__).with_name("sample_logs.json")
REQUIRED_FIELDS = {"timestamp", "level", "source", "message"}


def parse_timestamp(value: str) -> datetime:
    """Parse an ISO 8601 timestamp, including timestamps ending in Z."""
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_logs(file_path: Path) -> list[LogEntry]:
    """Load and validate log entries from a JSON array."""
    with file_path.open("r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    if not isinstance(data, list):
        raise ValueError("The JSON root must be an array of log entries.")

    logs: list[LogEntry] = []
    for index, entry in enumerate(data, start=1):
        if not isinstance(entry, dict) or not REQUIRED_FIELDS.issubset(entry):
            raise ValueError(f"Log entry {index} is missing required fields.")
        if not all(isinstance(entry[field], str) for field in REQUIRED_FIELDS):
            raise ValueError(f"Log entry {index} fields must contain strings.")
        parse_timestamp(entry["timestamp"])
        logs.append({field: entry[field] for field in REQUIRED_FIELDS})
    return logs


def analyze_logs(logs: list[LogEntry]) -> dict[str, object]:
    """Calculate severity, source, time-range, and error summaries."""
    levels = Counter(entry["level"].upper() for entry in logs)
    sources = Counter(entry["source"] for entry in logs)
    timestamps = [parse_timestamp(entry["timestamp"]) for entry in logs]
    errors = [
        entry for entry in logs if entry["level"].upper() in {"ERROR", "CRITICAL"}
    ]
    return {
        "total": len(logs),
        "levels": dict(sorted(levels.items())),
        "sources": dict(sorted(sources.items())),
        "start": min(timestamps).isoformat() if timestamps else None,
        "end": max(timestamps).isoformat() if timestamps else None,
        "errors": errors,
    }


def display_analysis(analysis: dict[str, object]) -> None:
    """Display a formatted log analysis report."""
    print("\n================ JSON LOG ANALYSIS ================")
    print(f"Total entries: {analysis['total']}")
    print(f"Time range: {analysis['start'] or 'N/A'} to {analysis['end'] or 'N/A'}")

    print("\nEntries by level:")
    levels = analysis["levels"]
    for level, count in levels.items():
        print(f"  {level:<10} {count}")

    print("\nEntries by source:")
    sources = analysis["sources"]
    for source, count in sources.items():
        print(f"  {source:<15} {count}")

    errors = analysis["errors"]
    print(f"\nError and critical events ({len(errors)}):")
    if not errors:
        print("  None")
    for entry in errors:
        print(
            f"  [{entry['timestamp']}] {entry['level'].upper()} "
            f"{entry['source']}: {entry['message']}"
        )


def main() -> None:
    """Read a JSON log path and display its analysis."""
    raw_path = input(
        f"Enter JSON log path or press Enter for {SAMPLE_FILE.name}: "
    ).strip().strip('"')
    file_path = Path(raw_path).expanduser() if raw_path else SAMPLE_FILE
    try:
        logs = load_logs(file_path)
        analysis = analyze_logs(logs)
    except FileNotFoundError:
        print(f"Log file not found: {file_path}")
        return
    except (json.JSONDecodeError, ValueError, PermissionError, UnicodeError, OSError) as error:
        print(f"Unable to analyze log file: {error}")
        return
    display_analysis(analysis)


if __name__ == "__main__":
    main()
