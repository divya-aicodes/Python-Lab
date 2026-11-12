"""Read and summarize a UTF-8 text log file."""

from pathlib import Path


def read_log_file(file_path: Path) -> list[str]:
    """Return the log file's lines without trailing newline characters."""
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if not file_path.is_file():
        raise IsADirectoryError(f"Not a file: {file_path}")
    return file_path.read_text(encoding="utf-8").splitlines()


def summarize_log(lines: list[str]) -> dict[str, int]:
    """Return basic text and severity statistics for log lines."""
    uppercase_lines = [line.upper() for line in lines]
    return {
        "lines": len(lines),
        "words": sum(len(line.split()) for line in lines),
        "characters": sum(len(line) for line in lines),
        "warnings": sum("WARNING" in line or "WARN" in line for line in uppercase_lines),
        "errors": sum("ERROR" in line or "CRITICAL" in line for line in uppercase_lines),
    }


def main() -> None:
    """Read a path, display its log lines, and print a summary."""
    raw_path = input("Enter the log file path: ").strip().strip('"')
    if not raw_path:
        print("A file path is required.")
        return

    file_path = Path(raw_path).expanduser()
    try:
        lines = read_log_file(file_path)
    except (FileNotFoundError, IsADirectoryError, PermissionError, UnicodeError, OSError) as error:
        print(f"Unable to read log file: {error}")
        return

    print("\n================ LOG CONTENTS ================")
    if lines:
        for line_number, line in enumerate(lines, start=1):
            print(f"{line_number:>4}: {line}")
    else:
        print("The log file is empty.")

    summary = summarize_log(lines)
    print("\n================== SUMMARY ==================")
    for label, value in summary.items():
        print(f"{label.title():<12}: {value}")


if __name__ == "__main__":
    main()
