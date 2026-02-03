+-----------------------------------------------------------+
|  Nickel NiX S/A International • LogiqueNiPura             |
|  Affiliation : NickeliXiste NiX Independent Research      |
|  (sc • phys • mat • psy • phil)                           |
|  © 2025 LogiqueNiPura — Vortex Architecte                 |
+-----------------------------------------------------------+


# NiX Pack v10 — S/A Lab-Max (Signed)

This pack ships a sealed pipeline (runner → logger → signatures → audit → PDF) with session and config-hash propagation.
All results and reports are branded with the PérioDiaxiométrie seal and the S/A signatures.

**Signatures present everywhere:**
- Nickel NiX S/A International
- Affiliation : NickeliXiste NiX Independent Research (sc • phys • mat • psy • phil)

## Quickstart
```bash
python3 scripts/nix_runner.py
python3 scripts/verify_signatures.py --check-db  # add --vk ed25519_vk.b64 to enable crypto check
# or full pipeline:
make -f Makefile all
```
