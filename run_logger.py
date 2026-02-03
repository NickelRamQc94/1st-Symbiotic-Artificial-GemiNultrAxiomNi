
#!/usr/bin/env python3
"""
run_logger.py — Extended CSV logger for structured event recording.

- Creates the CSV with header if missing.
- Appends rows safely with proper quoting (UTF-8).
- Auto-generates UTC timestamps in ISO 8601 with milliseconds.
- CLI-friendly (argparse) and import-friendly (functions).

Default CSV header (strict order):
  Timestamp_UTC, Log_Level, Source_Module, Event_ID, User_ID,
  Action_Performed, Status, Error_Code, Details
"""

from __future__ import annotations
import csv
import sys
import os
from pathlib import Path
from datetime import datetime, timezone
import argparse
from typing import Optional, Sequence, Mapping

DEFAULT_HEADER: Sequence[str] = (
    "Timestamp_UTC",
    "Log_Level",
    "Source_Module",
    "Event_ID",
    "User_ID",
    "Action_Performed",
    "Status",
    "Error_Code",
    "Details",
)

def iso_utc_now_ms() -> str:
    """Return timezone-aware ISO 8601 UTC with milliseconds."""
    now = datetime.now(timezone.utc)
    # Ensure milliseconds precision; keep timezone offset +00:00
    return now.isoformat(timespec="milliseconds")

def initialize_logger(filepath: os.PathLike | str, delimiter: str = ",") -> Path:
    """
    Ensure the CSV file exists with the correct header in the correct order.
    If it doesn't exist or is empty, create it and write ONLY the header.
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.stat().st_size == 0:
        try:
            with path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(DEFAULT_HEADER)
        except Exception as e:
            print(f"[run_logger] ERROR: cannot initialize CSV at {path}: {e}", file=sys.stderr)
            raise
    return path

def log_event(
    filepath: os.PathLike | str,
    log_level: str,
    source_module: str,
    event_id: str,
    user_id: str,
    action_performed: str,
    status: str,
    error_code: str = "",
    details: str = "",
    delimiter: str = ",",
) -> None:
    """
    Append a single, structured log row to the CSV.

    Args are written in strict header order. Timestamp_UTC is auto-filled.
    """
    path = initialize_logger(filepath, delimiter=delimiter)
    row = {
        "Timestamp_UTC": iso_utc_now_ms(),  # auto UTC timestamp
        "Log_Level": str(log_level),
        "Source_Module": str(source_module),
        "Event_ID": str(event_id),
        "User_ID": str(user_id),
        "Action_Performed": str(action_performed),
        "Status": str(status),
        "Error_Code": str(error_code),
        "Details": str(details),
    }
    try:
        with path.open("a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=DEFAULT_HEADER,
                delimiter=delimiter,
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
                extrasaction="ignore",
            )
            writer.writerow(row)
    except Exception as e:
        print(f"[run_logger] ERROR: cannot write log row: {e}", file=sys.stderr)
        raise

def build_cli() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Append structured events to a UTF-8 CSV log (with auto UTC timestamps)."
    )
    p.add_argument("--file", "-f", required=True, help="Path to CSV log file (will be created if missing).")
    p.add_argument("--delimiter", "-d", default=",", help="CSV delimiter (default ',').")
    p.add_argument("--level", required=True, help="Log level: INFO|WARNING|ERROR|DEBUG|CRITICAL")
    p.add_argument("--source", required=True, help="Source module, e.g., main.py or pkg.mod:func")
    p.add_argument("--event", required=True, help="Event ID, e.g., EVT-0001")
    p.add_argument("--user", default="", help="User ID, e.g., user-42 (optional)")
    p.add_argument("--action", required=True, help="Short verb phrase, e.g., 'Start Run'")
    p.add_argument("--status", required=True, help="Status: SUCCESS|FAILURE|PENDING")
    p.add_argument("--error", default="", help="Error code if applicable (optional)")
    p.add_argument("--details", default="", help="Free text details (quoted automatically).")
    return p

def main(argv=None) -> int:
    args = build_cli().parse_args(argv)
    try:
        log_event(
            filepath=args.file,
            log_level=args.level,
            source_module=args.source,
            event_id=args.event,
            user_id=args.user,
            action_performed=args.action,
            status=args.status,
            error_code=args.error,
            details=args.details,
            delimiter=args.delimiter,
        )
        return 0
    except Exception:
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
