# AATMF Tooling

Standard-library Python (3.10+) — no dependencies, runs on a bare CI image.

| Script | Purpose |
|:---|:---|
| `aatmf_taxonomy.py` | Shared parser. Reads the tactic chapters + README into a structured taxonomy. |
| `build_export.py` | Writes the machine-readable export to [`../data/`](../data/). |
| `validate.py` | Framework integrity checks (run in CI by [`.github/workflows/integrity.yml`](../.github/workflows/integrity.yml)). |

## Usage

```bash
python scripts/build_export.py   # regenerate data/aatmf.json + data/aatmf-techniques.csv
python scripts/validate.py       # run integrity checks (exit 1 on failure)
```

## What `validate.py` enforces

**Errors** (block the build):
- Duplicate technique IDs
- Duplicate attack-procedure IDs (now namespaced `TX-AP-NNNl`)
- Per-tactic technique counts that disagree across the overview table, the
  technique cards, the chapter subtitle, and the README
- Risk badges that don't match the AATMF-R scale (250+ CRITICAL · 200–249 HIGH ·
  150–199 MEDIUM · 100–149 LOW · 0–99 INFO)
- Overview/card risk-score drift
- Broken relative links
- Undefined inline technique references (`TX-AT-NNN` with no matching card)
- Unbalanced code fences
- A stale `data/` export

**Warnings** (surfaced, non-blocking):
- Technique headings that omit the `` ### `TX-AT-NNN` `` backtick convention

## Regenerating the export

`data/aatmf.json` and `data/aatmf-techniques.csv` are generated artifacts. After
editing any tactic chapter, run `python scripts/build_export.py` and commit the
updated files — CI verifies they are current.
