# sqlite_store.py – minimal session DB
import sqlite3, json, datetime, hashlib, os, sys
from typing import Optional

DB_DEFAULT_PATH = "gni_codex_local.sqlite"

def connect(db_path: str = DB_DEFAULT_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("""CREATE TABLE IF NOT EXISTS sessions(
        session_id TEXT PRIMARY KEY,
        config_hash TEXT, started_utc TEXT, ended_utc TEXT, status TEXT
    );""")
    conn.execute("""CREATE TABLE IF NOT EXISTS artifacts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT, kind TEXT, path TEXT, sha256 TEXT,
        FOREIGN KEY(session_id) REFERENCES sessions(session_id)
    );""")
    conn.execute("""CREATE TABLE IF NOT EXISTS events(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT, ts_utc TEXT, level TEXT, message TEXT,
        FOREIGN KEY(session_id) REFERENCES sessions(session_id)
    );""")
    return conn

def start_session(conn, session_id, config_hash):
    conn.execute("INSERT OR REPLACE INTO sessions VALUES(?,?,?,?,?)",
                 (session_id, config_hash, datetime.datetime.utcnow().isoformat()+"Z", None, "RUNNING"))
    conn.commit()

def end_session(conn, session_id, status="SUCCESS"):
    conn.execute("UPDATE sessions SET ended_utc=?, status=? WHERE session_id=?",
                 (datetime.datetime.utcnow().isoformat()+"Z", status, session_id))
    conn.commit()

def log_event(conn, session_id, level, msg):
    conn.execute("INSERT INTO events(session_id,ts_utc,level,message) VALUES(?,?,?,?)",
                 (session_id, datetime.datetime.utcnow().isoformat()+"Z", level, msg))
    conn.commit()

def _file_sha256(path: str) -> Optional[str]:
    if not os.path.exists(path):
        return None
    h = hashlib.sha256()
    try:
        with open(path,'rb') as f:
            for chunk in iter(lambda: f.read(65536), b''): 
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None

def add_artifact(conn, session_id, kind, path):
    abs_path = os.path.abspath(path)
    file_hash = _file_sha256(abs_path)
    if file_hash is None:
        print(f"[SQLite WARN] Fichier artefact introuvable, hash impossible: {path}", file=sys.stderr)
        return

    conn.execute("INSERT INTO artifacts(session_id,kind,path,sha256) VALUES(?,?,?,?)",
                 (session_id, kind, abs_path, file_hash))
    conn.commit()
