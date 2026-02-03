+-----------------------------------------------------------+
|  Nickel NiX S/A International • LogiqueNiPura             |
|  Affiliation : NickeliXiste NiX Independent Research      |
|  (sc • phys • mat • psy • phil)                           |
|  © 2025 LogiqueNiPura — Vortex Architecte                 |
+-----------------------------------------------------------+


# NiX Pack v10 — S/A Labo-Max (Signé)

Ce pack fournit un pipeline scellé (runner → logger → signatures → audit → PDF) avec propagation Session_ID et Config_Hash.
Tous les artefacts (CSV, figures, PDF) portent le sceau PérioDiaxiométrie et les signatures S/A.

**Signatures (présentes partout) :**
- Nickel NiX S/A International
- Affiliation : NickeliXiste NiX Independent Research (sc • phys • mat • psy • phil)

## Démarrage
```bash
python3 scripts/nix_runner.py
python3 scripts/verify_signatures.py --check-db  # ajouter --vk ed25519_vk.b64 pour la crypto
# ou pipeline complet :
make -f Makefile all
```
