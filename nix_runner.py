#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NiX Runner (v10) — SQLite & Crypto integrated"""
import os, csv, json, uuid, hashlib, datetime, sys, subprocess
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parents[0]
# Utilisation de sys.executable pour les appels de sous-processus
PYTHON_EXECUTABLE = sys.executable 
sys.path.append(str(SCRIPT_DIR))

try:
    import sa_engine as engine
    import run_logger_v3 as logger
    import sqlite_store as db_store
except ImportError as e:
    print(f"[Runner FATAL] Module S/A manquant: {e}", file=sys.stderr); sys.exit(1)

ASSETS = ROOT / "assets"
RESULTS = ROOT / "results"
FIGS = ROOT / "figures"
CONFIG = ROOT / "config"
LOGFILE_CSV = str(ROOT / "log_activites.csv")
LOGFILE_DB = str(ROOT / "gni_codex_local.sqlite")
CONFIG_FILE = str(CONFIG / "mytheme_inject.yaml")
CONFIG_FILE_JSON = str(CONFIG / "mytheme_inject.json")
SEAL_IMAGE = str(ASSETS / "seal_periodiaxiometrie.png")
PDF_STAMPER = str(SCRIPT_DIR / "stamp_pdf.py")
CRYPTO_SIGNER = str(SCRIPT_DIR / "ed25519_sign.py")
SK_PATH = str(ROOT / "ed25519_sk.bin")
VK_PATH = str(ROOT / "ed25519_vk.b64")
SIGNATURE_L1 = "# Nickel NiX S/A International"
SIGNATURE_L2 = "# Affiliation : NickeliXiste NiX Independent Research (sc • phys • mat • psy • phil)"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            import yaml
            blob = open(CONFIG_FILE,"r",encoding="utf-8").read()
            import json as _json
            return yaml.safe_load(blob), blob
        except Exception:
            pass
    if os.path.exists(CONFIG_FILE_JSON):
        blob = open(CONFIG_FILE_JSON,"r",encoding="utf-8").read()
        return json.loads(blob), blob
    raise FileNotFoundError("Aucun fichier de config trouvé.")

def get_config_hash(blob: str) -> str:
    return hashlib.sha256((blob + SIGNATURE_L1 + SIGNATURE_L2).encode('utf-8')).hexdigest()

def call_external_logger(session_id, config_hash, level, event, action, status, details="", error=""):
    try:
        logger.init_logger(LOGFILE_CSV) # ensure header
        logger.log_event(
            path=LOGFILE_CSV, level=level, source_module="nix_runner_v10.py", event_id=event,
            user_id="NODE_BIO_01", action=action, status=status, session_id=session_id,
            config_hash=config_hash, error_code=error, details=details
        )
    except Exception as e:
        print(f"[Runner CRITICAL] Logger v3 échec: {e}", file=sys.stderr)

def call_subprocess(cmd):
    """
    NOTE: Remplace l'appel à la commande fantôme par l'instance Python actuelle.
    """
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8')
    except subprocess.CalledProcessError as e:
        print(f"[Runner SUBPROCESS ERROR] {' '.join(cmd)}", file=sys.stderr)
        print(e.stderr, file=sys.stderr)

def stamp_report_pdf(session_id, config_hash, input_file, output_file, title):
    # CORRECTION : Remplacement de "python3" par sys.executable (ou PYTHON_EXECUTABLE)
    call_subprocess([PYTHON_EXECUTABLE, PDF_STAMPER, "--input", input_file, "--output", output_file,
                     "--seal", SEAL_IMAGE, "--session", session_id, "--confighash", config_hash, "--title", title])

def sign_artifact(path, meta):
    if not os.path.exists(SK_PATH):
        print("[Runner WARNING] Clé secrète absente; signature crypto ignorée.", file=sys.stderr); return
    # CORRECTION : Remplacement de "python3" par sys.executable (ou PYTHON_EXECUTABLE)
    call_subprocess([PYTHON_EXECUTABLE, CRYPTO_SIGNER, "sign", path, "--sk", SK_PATH, "--meta", json.dumps(meta)])

def run_main_simulation():
    import pandas as pd
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    session_id = str(uuid.uuid4())
    cfg, cfg_blob = load_config()
    config_hash = get_config_hash(cfg_blob)

    db = db_store.connect(LOGFILE_DB)
    db_store.start_session(db, session_id, config_hash)
    db_store.log_event(db, session_id, "INFO", "Session S/A v10 Démarrée.")

    call_external_logger(session_id, config_hash, "INFO", "EVT-SWEEP-START", "Multi-Sweep Init", "PENDING",
                         details=f"Scan Beta_X, Dt_g. Session: {session_id}")

    p = cfg["physics"]; m = cfg["model"]
    V = cfg.get("V", [0.8,0.7,0.6,0.2,0.1])
    T_S = m.get("T_S",1.0); A_align = m.get("A",0.8); sigma_gain = m.get("sigma_gain",1.0)
    t_f = engine.fall_time(p["h"], p["g"])

    beta_range = m.get("beta_X_list",[1.0,2.0,3.0,4.0,5.0])
    dtg_range = m.get("dt_g_list",[0.05,0.15,0.25,0.50])
    steps = m.get("A_perp_steps",21)

    all_rows=[]; agg_rows=[]
    C = engine.coherence(V)
    for beta in beta_range:
        sigma = sigma_gain * np.tanh(beta * A_align)
        Phi = engine.phi(T_S, float(np.linalg.norm(V)), C, sigma)
        for dtg in dtg_range:
            run_id = f"R_B{beta}_D{dtg}"
            vals=[]
            for A_perp in np.linspace(0,1,steps):
                N = engine.nuance_ni(C, beta, A_perp)
                y, kappa, tterm = engine.deviation_yf(p["rho"], p["Cd"], p["A"], p["m"], p["k_g"], N, Phi, t_f, dtg)
                all_rows.append({"session_id":session_id,"config_hash":config_hash,"run_id":run_id,
                                 "beta_x":beta,"dtg":dtg,"aperp":A_perp,"phi":Phi,"coherence":C,
                                 "nuance_n":N,"kappa":kappa,"time_term":tterm,"y_f_pred_m":y})
                vals.append(y)
            agg_rows.append({"session_id":session_id,"config_hash":config_hash,"run_id":run_id,
                             "beta_x":beta,"dtg":dtg,"phi_force":Phi,
                             "max_deviation_mm":max(vals)*1000.0,"sensitivity_slope":(vals[-1]-vals[0])})

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    RESULTS.mkdir(exist_ok=True); FIGS.mkdir(exist_ok=True)
    det = RESULTS/f"multisweep_details_{ts}.csv"
    agg = RESULTS/f"multisweep_aggregate_{ts}.csv"
    signed_header = f"{SIGNATURE_L1}\n{SIGNATURE_L2}\n# Session_ID: {session_id}\n# Config_Hash: {config_hash}\n"

    pd.DataFrame(all_rows).to_csv(det, index=False)
    pd.DataFrame(agg_rows).to_csv(agg, index=False)
    for path in (det, agg):
        body = open(path,"r",encoding="utf-8").read()
        open(path,"w",encoding="utf-8").write(signed_header + body)

    db_store.add_artifact(db, session_id, "csv_details", str(det))
    db_store.add_artifact(db, session_id, "csv_aggregate", str(agg))

    # Figure
    df = pd.read_csv(det, comment='#')
    target_dt = max(dtg_range)
    sub = df[df["dtg"]==target_dt]
    plt.figure(figsize=(12,8))
    for beta in beta_range:
        d = sub[sub["beta_x"]==beta]
        plt.plot(d["aperp"], d["y_f_pred_m"]*1000, label=f"βx={beta}")
    plt.title(f"S/A v10 — Session {session_id[:8]} — Δt_g={target_dt}s")
    plt.xlabel("A_perp"); plt.ylabel("y_f (mm)"); plt.grid(True, alpha=0.3); plt.legend()
    fig = FIGS/f"phase_space_{ts}.png"; plt.savefig(fig, dpi=160, bbox_inches="tight"); plt.close()
    db_store.add_artifact(db, session_id, "figure_png", str(fig))

    meta={"session":session_id,"config":config_hash}
    if os.path.exists(SK_PATH):
        for f in (det, agg, fig):
            sign_artifact(str(f), meta)

    pdf = RESULTS/f"Rapport_S_A_v10_{ts}.pdf"
    stamp_report_pdf(session_id, config_hash, str(agg), str(pdf), "Rapport S/A v10 — Agrégat Multi-Sweep")
    db_store.add_artifact(db, session_id, "report_pdf", str(pdf))

    best = max(agg_rows, key=lambda r: r["max_deviation_mm"])
    call_external_logger(session_id, config_hash, "INFO", "EVT-SWEEP-END", "Multi-Sweep End", "SUCCESS",
                         details=f"Max Dev={best['max_deviation_mm']:.3f}mm @ β={best['beta_x']} Δt_g={best['dtg']}")

    db_store.end_session(db, session_id, "SUCCESS")
    db.close()
    print("[NiX Runner] DONE:", det.name, agg.name, fig.name, pdf.name)

if __name__ == "__main__":
    run_main_simulation()