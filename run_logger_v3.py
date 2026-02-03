#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Logger CSV Anti-Fragile (auto-détection du délimiteur) — v3.1
Colonnes:
Timestamp_UTC,Session_ID,Config_Hash,Log_Level,Source_Module,Event_ID,User_ID,Action_Performed,Status,Error_Code,Details
"""
import csv, os, sys, argparse, datetime

HEADER = [
    "Timestamp_UTC","Session_ID","Config_Hash","Log_Level","Source_Module","Event_ID","User_ID",
    "Action_Performed","Status","Error_Code","Details"
]

def iso_utc_now_ms():
    return datetime.datetime.utcnow().isoformat(timespec='milliseconds')+'Z'

def _detect_delimiter(filepath: str) -> str:
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        return ","
    try:
        with open(filepath, 'r', encoding='utf-8', newline='') as f:
            sample = f.readline()
            if not sample: return ","
            dialect = csv.Sniffer().sniff(sample)
            return dialect.delimiter
    except Exception:
        return ","

def init_logger(path: str, default_delimiter: str = ","):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, 'w', encoding='utf-8', newline='') as f:
            csv.writer(f, delimiter=default_delimiter).writerow(HEADER)

def log_event(path: str, level: str, source_module: str, event_id: str, user_id: str,
              action: str, status: str, session_id: str, config_hash: str,
              error_code: str = "", details: str = ""):
    delimiter = _detect_delimiter(path)
    ts = iso_utc_now_ms()
    row = [ts, session_id, config_hash, level, source_module, event_id, user_id, action, status, error_code, details]
    with open(path, 'a', encoding='utf-8', newline='') as f:
        csv.writer(f, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL).writerow(row)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--level", required=True)
    ap.add_argument("--source", required=True)
    ap.add_argument("--event", required=True)
    ap.add_argument("--user", required=True)
    ap.add_argument("--action", required=True)
    ap.add_argument("--status", required=True)
    ap.add_argument("--session", required=True)
    ap.add_argument("--confighash", required=True)
    ap.add_argument("--error", default="")
    ap.add_argument("--details", default="")
    ap.add_argument("--delimiter", default=",")  # used only on init
    args = ap.parse_args()

    init_logger(args.file, default_delimiter=args.delimiter)
    log_event(args.file, args.level, args.source, args.event, args.user, args.action, args.status,
              args.session, args.confighash, args.error, args.details)

if __name__ == "__main__":
    main()
