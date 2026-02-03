+-----------------------------------------------------------+
|  Nickel NiX S/A International • LogiqueNiPura             |
|  Affiliation: NickeliXiste NiX Independent Research       |
|  © 2025 LogiqueNiPura — Vortex Architecte                 |
+-----------------------------------------------------------+

+-----------------------------------------------------------+
|  Nickel NiX S/A International • LogiqueNiPura             |
|  Affiliation: NickeliXiste NiX Independent Research       |
|  © 2025 LogiqueNiPura — Vortex Architecte                 |
+-----------------------------------------------------------+

# NiX Pack v10 — Install & Run

Affiliation : NickeliXiste NiX Independent Research (sc • phys • mat • psy • phil)
© 2025 LogiqueNiPura — Vortex Architecte

## What is this?
Signed pack with runner, logging, signatures and audit hooks (zip_pack). This minimal skeleton 
includes the ASCII badge and the PerioDiaxiometric seal (if available).

## Quick Install
1) (Optional) Create a virtual env and install your deps (pandas, matplotlib, reportlab, pynacl).
2) Use `scripts/zip_pack.py` to assemble a distribution zip (includes a manifest with SHA-256).

## Usage
```bash
# Create a sealed zip of this folder
python3 scripts/zip_pack.py --root . --out ../NiX_Pack_v10_Sealed.zip

# Run audit (if your verify tools exist in scripts/)
python3 scripts/zip_pack.py --verify-only
```

## Notes
- Sealed zip will include a MANIFEST.json and PACK_INFO.txt with session metadata.
- The zip excludes common junk: __pycache__, .ipynb_checkpoints, *.pyc, .DS_Store.
