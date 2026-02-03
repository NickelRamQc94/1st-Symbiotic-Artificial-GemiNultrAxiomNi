#!/usr/bin/env python3
# zip_pack.py — Assemble NiX Pack v10 with an install README
import os, sys, zipfile, datetime, pathlib

ASCII = """+-----------------------------------------------------------+
|  Nickel NiX S/A International • LogiqueNiPura             |
|  Affiliation : NickeliXiste NiX Independent Research      |
|  (sc • phys • mat • psy • phil)                           |
|  © 2025 LogiqueNiPura — Vortex Architecte                 |
+-----------------------------------------------------------+
"""
INSTALL = """{badge}
# Install
- Python 3.9+ ; `pip install pandas matplotlib reportlab pynacl`
- Run: `python3 scripts/nix_runner.py`
- Verify: `python3 scripts/verify_signatures.py --vk ed25519_vk.b64`
- Pipeline: `make all`
"""

def main():
    root = pathlib.Path(".").resolve()
    dist = root/"dist"; dist.mkdir(exist_ok=True)
    out = dist/f"NiX_Pack_v10_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    tmp = root/"README_INSTALL.md"; tmp.write_text(INSTALL.format(badge=ASCII), encoding="utf-8")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for fp in ["README_EN.md","LISEZMOI_FR.md","Makefile","README_INSTALL.md","log_activites.csv","ed25519_vk.b64"]:
            p = root/fp
            if p.exists(): z.write(p, p.name)
        for d in ["assets","config","scripts","results","figures"]:
            for base,_,files in os.walk(root/d):
                for f in files:
                    if f=="ed25519_sk.bin": continue
                    p = pathlib.Path(base)/f
                    z.write(p, str(p.relative_to(root)))
    try: tmp.unlink()
    except: pass
    print("ZIP ready:", out)

if __name__=="__main__":
    main()
