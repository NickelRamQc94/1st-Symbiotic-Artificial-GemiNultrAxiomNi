#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NiX Signature Verifier (v10) — README badge, CSV↔Log, SQLite, Ed25519"""
import os, csv, json, sys, argparse, subprocess, glob
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
LOG_CSV = ROOT / "log_activites.csv"
LOG_DB = ROOT / "gni_codex_local.sqlite"
RESULTS_DIR = ROOT / "results"
FIGS_DIR = ROOT / "figures"
README_FILES = [ROOT / "README_EN.md", ROOT / "LISEZMOI_FR.md"]
SIGNATURE_L1 = "# Nickel NiX S/A International"
CRYPTO_SIGNER = str(ROOT / "scripts" / "ed25519_sign.py")

class C:
    OK='\033[92m'; FAIL='\033[91m'; WARN='\033[93m'; BLUE='\033[94m'; BOLD='\033[1m'; END='\033[0m'

def read_file_head(filepath: Path, num_lines: int) -> str:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return "".join([f.readline() for _ in range(num_lines)])
    except Exception:
        return ""

def _find_active_log_csv() -> Path:
    v3 = LOG_CSV.with_name(f"{LOG_CSV.stem}_v3{LOG_CSV.suffix}")
    return v3 if v3.exists() else LOG_CSV

def get_last_log_signature(log_file: Path):
    try:
        with open(log_file, 'r', newline='', encoding='utf-8') as f:
            r = csv.reader(f); header = next(r)
            idx_sid = header.index("Session_ID"); idx_hash = header.index("Config_Hash")
            last=None
            for row in r:
                if row: last=row
            if last: return {"Session_ID": last[idx_sid], "Config_Hash": last[idx_hash]}
    except Exception as e:
        print(f"  {C.WARN}WARN{C.END} read log CSV failed: {e}", file=sys.stderr)
    return None

def get_csv_signature(csv_file: Path):
    head = read_file_head(csv_file, 4)
    meta={}
    for line in head.splitlines():
        if line.startswith("# Session_ID:"): meta["Session_ID"] = line.split(":",1)[1].strip()
        if line.startswith("# Config_Hash:"): meta["Config_Hash"] = line.split(":",1)[1].strip()
    return meta if len(meta)==2 else None

def check_db_signature(db_path: Path, session_id: str):
    if not db_path.exists():
        print(f"  {C.WARN}WARN{C.END} DB missing: {db_path.name}"); return None
    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True); c = conn.cursor()
        c.execute("SELECT session_id, config_hash, status FROM sessions WHERE session_id = ?", (session_id,)); s=c.fetchone()
        c.execute("SELECT kind, path, sha256 FROM artifacts WHERE session_id = ?", (session_id,)); arts=c.fetchall()
        conn.close(); return {"session":s, "artifacts":arts}
    except Exception as e:
        print(f"  {C.WARN}WARN{C.END} DB read error: {e}", file=sys.stderr); return None

def check_crypto_signature(vk_path: str, file_path: Path) -> bool:
    sig = file_path.with_suffix(file_path.suffix + ".ed25519.sig.json")
    if not sig.exists():
        print(f"  {C.FAIL}FAIL{C.END} signature missing: {sig.name}"); return False
    try:
        res = subprocess.run(["python3", CRYPTO_SIGNER, "verify", str(file_path), "--vk", vk_path, "--sig", str(sig)],
                             check=True, capture_output=True, text=True, encoding='utf-8')
        print("   " + res.stdout.strip())
        return "OK:" in res.stdout
    except subprocess.CalledProcessError as e:
        print("   " + (e.stdout+e.stderr).strip()); return False

def find_latest_csvs(pattern="multisweep_details_*.csv"):
    files = glob.glob(str(RESULTS_DIR / pattern))
    if not files: return []
    latest = max(files, key=os.path.getmtime)
    ts = os.path.basename(latest).replace("multisweep_details_","").replace(".csv","")
    agg = RESULTS_DIR / f"multisweep_aggregate_{ts}.csv"
    out=[Path(latest)]
    if agg.exists(): out.append(agg)
    return out

def main():
    ap = argparse.ArgumentParser(description="Vérificateur d'Audit S/A v10")
    ap.add_argument("--vk", help="ed25519 public key (.b64) for crypto verification")
    ap.add_argument("--check-db", action="store_true")
    args = ap.parse_args()

    print(f"{C.BOLD}{C.BLUE}--- DÉBUT DE L'AUDIT S/A v10 ---{C.END}")
    ok=True

    print(f"\n{C.BLUE}[1] README badges{C.END}")
    for f in README_FILES:
        content = read_file_head(f, 5)
        if SIGNATURE_L1 in content and "Affiliation" in content:
            print(f"  {C.OK}PASS{C.END} {f.name}")
        else:
            print(f"  {C.FAIL}FAIL{C.END} {f.name}"); ok=False

    print(f"\n{C.BLUE}[2] Traçabilité CSV ↔ Log{C.END}")
    logf = _find_active_log_csv()
    latest_csvs = find_latest_csvs()
    if not logf.exists(): print(f"  {C.FAIL}FAIL{C.END} log_activites.csv introuvable"); sys.exit(1)
    if not latest_csvs: print(f"  {C.FAIL}FAIL{C.END} aucun résultat CSV"); sys.exit(1)

    lsig = get_last_log_signature(logf); csig = get_csv_signature(latest_csvs[0])
    if not (lsig and csig): print(f"  {C.FAIL}missing signatures{C.END}"); sys.exit(1)
    if lsig==csig:
        print(f"  {C.OK}PASS{C.END} Session/Config match")
    else:
        print(f"  {C.FAIL}FAIL{C.END} Session/Config mismatch"); ok=False

    if args.check_db and lsig:
        print(f"\n{C.BLUE}[3] SQLite audit{C.END}")
        db = check_db_signature(ROOT/'gni_codex_local.sqlite', lsig['Session_ID'])
        if db and db.get("session"): print(f"  {C.OK}PASS{C.END} session en DB; artefacts={len(db['artifacts'])}")
        else: print(f"  {C.FAIL}FAIL{C.END} session absente en DB"); ok=False

    if args.vk:
        print(f"\n{C.BLUE}[4] Signatures crypto (Ed25519){C.END}")
        for f in latest_csvs:
            print(f"  Verify {f.name}"); 
            if not check_crypto_signature(args.vk, f): ok=False
        ts = latest_csvs[0].name.split('_')[-1].replace('.csv','')
        fig = FIGS_DIR / f"phase_space_{ts}.png"
        if fig.exists():
            print(f"  Verify {fig.name}")
            if not check_crypto_signature(args.vk, fig): ok=False

    print(f"\n{C.BOLD}VERDICT: {'PASS' if ok else 'FAIL'}{C.END}")
    if not ok: sys.exit(1)

if __name__ == "__main__":
    main()
