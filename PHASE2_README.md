# Phase 2 Kit — Lebanon Property Tax Database II

**Date:** 2025-09-06

This kit delivers five concrete pieces for the next phase:

1. **Finalize Column Maps** — `scripts/finalize_column_maps.ps1`
2. **Validation Rules (and Runner)** — templates + `scripts/apply_validation_rules.ps1`
3. **Join Keys & Uniqueness Checks** — template + `scripts/qc_join_keys.ps1`
4. **Data Explorer UX Tweaks** — `scripts/patch_site_add_filters_and_totals.ps1` + JS
5. **Intake Checklist** — `docs/site/Intake_Checklist.pdf` (also included at kit root)

All files are UTF-8 (no BOM) and Windows-first (PowerShell). No cloud resources required.

---

## Quick Start (Clerk mode)

> Evidence: canonical repo layout with `outputs/normalized_csvs` and `outputs/alignment_report` directory exists.

1. Unzip this kit at your **repo root** (the folder that contains `scripts/` and `outputs/`).  
2. Run each step from **PowerShell** launched at the repo root (or inside `scripts/`).

### 1) Finalize Column Maps
```pwsh
pwsh ./scripts/finalize_column_maps.ps1
```
- Writes `outputs/alignment_report/column_maps/column_map_YYYY-MM-DD.csv`
- Identity mapping only (no schema guessing). Edit this CSV to refine requirements later.

### 2) Validation Rules
Copy the template to working rules:
```pwsh
Copy-Item outputs/alignment_report/templates/validation_rules_template.csv outputs/alignment_report/validation_rules.csv -Force
pwsh ./scripts/apply_validation_rules.ps1
```
- Writes `outputs/alignment_report/validation_report_YYYY-MM-DD.csv`
- Supported rules: REQUIRED, UNIQUE, DTYPE, MIN, MAX, REGEX, ALLOWED_VALUES, ROWCOUNT_MIN

### 3) Join Keys & Uniqueness
Create a `join_keys.csv` (from template) if you have known pairs:
```pwsh
Copy-Item outputs/alignment_report/templates/join_keys_template.csv outputs/alignment_report/join_keys.csv -Force
pwsh ./scripts/qc_join_keys.ps1
```
- Always writes `join_key_profile_YYYY-MM-DD.csv` (nulls, distincts, uniqueness ratio)  
- If `join_keys.csv` exists, also writes `join_checks_YYYY-MM-DD.csv` with orphans & duplicates.

### 4) Data Explorer UX Tweaks
```pwsh
pwsh ./scripts/patch_site_add_filters_and_totals.ps1
```
- Injects `js/data_explorer_enhancements.js` into `docs/site/*.html` (idempotent).
- Adds per-column filters and a numeric totals row (Σ) to tables.

### 5) Intake Checklist (PDF)
The checklist PDF is in:
- `docs/site/Intake_Checklist.pdf` (ready to publish) and also at the kit root for convenience.

---

## Notes
- All scripts automatically discover the repo root and write to `outputs/alignment_report`.
- CSV writing is **UTF-8, no BOM** to play nice with GitHub Pages and the site fetcher.
- These tools do **not** assume column names, file names, or external dependencies.
