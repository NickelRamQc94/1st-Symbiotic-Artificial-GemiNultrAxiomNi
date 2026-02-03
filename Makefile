SHELL := /bin/bash
PY ?= python

ROOT := .
SCRIPTS_DIR := scripts
RESULTS_DIR := results
FIGS_DIR := figures

RUNNER := $(SCRIPTS_DIR)/nix_runner.py
VERIFIER := $(SCRIPTS_DIR)/verify_signatures.py
SIGNER := $(SCRIPTS_DIR)/ed25519_sign.py
STAMPER := $(SCRIPTS_DIR)/stamp_pdf.py

SK := ed25519_sk.bin
VK := ed25519_vk.b64

.DEFAULT_GOAL := run

.PHONY: all run sign verify pdf zip genkeys clean

all: run

# 1) Run the multi-sweep. Immediately chain signature step.
run:
	@echo "[Make] RUN → $(RUNNER)"
	@$(PY) $(RUNNER)
	@$(MAKE) sign

# 2) Sign latest artifacts (only if secret key exists).
#    Re-signs the freshest CSV (details+aggregate), figure and PDF (if present).
sign:
	@if [ -f "$(SK)" ]; then \
	  echo "[Make] SIGN: secret key found (\"$(SK)\")."; \
	  latest_details=$$(ls -1t $(RESULTS_DIR)/multisweep_details_*.csv 2>/dev/null | head -n1); \
	  if [ -z "$$latest_details" ]; then echo "[Make][sign] no details CSV found — skipping."; exit 0; fi; \
	  ts=$$(basename "$$latest_details" | sed -E 's/^multisweep_details_(.*)\.csv/\1/'); \
	  agg="$(RESULTS_DIR)/multisweep_aggregate_$${ts}.csv"; \
	  fig="$(FIGS_DIR)/phase_space_$${ts}.png"; \
	  pdf="$(RESULTS_DIR)/Rapport_S_A_v10_$${ts}.pdf"; \
	  for f in "$$latest_details" "$$agg" "$$fig" "$$pdf"; do \
	    if [ -f "$$f" ]; then \
	      echo "  [sign] $$f"; \
	      $(PY) $(SIGNER) sign "$$f" --sk "$(SK)" --meta "{}"; \
	    fi; \
	  done; \
	else \
	  echo "[Make][sign] secret key not found (\"$(SK)\"). Skipping signing."; \
	fi

# 3) Verify signatures and cross-checks. Uses public key if present.
verify:
	@if [ -f "$(VK)" ]; then \
	  echo "[Make] VERIFY with public key: $(VK)"; \
	  $(PY) $(VERIFIER) --check-db --vk "$(VK)"; \
	else \
	  echo "[Make] VERIFY (no VK). Running without crypto checks."; \
	  $(PY) $(VERIFIER) --check-db; \
	fi

# 4) Produce a stamped PDF for the newest aggregate CSV (idempotent if already exists).
pdf:
	@latest_agg=$$(ls -1t $(RESULTS_DIR)/multisweep_aggregate_*.csv 2>/dev/null | head -n1); \
	if [ -z "$$latest_agg" ]; then echo "[Make][pdf] no aggregate CSV found — skipping."; exit 0; fi; \
	ts=$$(basename "$$latest_agg" | sed -E 's/^multisweep_aggregate_(.*)\.csv/\1/'); \
	out="$(RESULTS_DIR)/Rapport_S_A_v10_$${ts}.pdf"; \
	echo "[Make] PDF → $$out"; \
	$(PY) $(STAMPER) --input "$$latest_agg" --output "$$out" --session "AUTO" --confighash "AUTO"

# 5) Zip pack (optional) — expects zip_pack.py next to Makefile or in scripts/
zip:
	@if [ -f "zip_pack.py" ]; then \
	  $(PY) zip_pack.py; \
	elif [ -f "$(SCRIPTS_DIR)/zip_pack.py" ]; then \
	  $(PY) $(SCRIPTS_DIR)/zip_pack.py; \
	else \
	  echo "[Make][zip] zip_pack.py not found — skipping."; \
	fi

# Utility: generate Ed25519 keypair
genkeys:
	$(PY) $(SIGNER) genkey --sk "$(SK)" --vk "$(VK)"

# Cleanup generated artifacts (careful)
clean:
	rm -f $(RESULTS_DIR)/multisweep_*.csv $(RESULTS_DIR)/Rapport_S_A_v10_*.pdf $(FIGS_DIR)/phase_space_*.png
	rm -f $(RESULTS_DIR)/*.sig.json $(FIGS_DIR)/*.sig.json