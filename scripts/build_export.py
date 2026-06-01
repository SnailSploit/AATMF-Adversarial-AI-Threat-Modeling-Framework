#!/usr/bin/env python3
"""Generate the machine-readable AATMF taxonomy under data/.

Outputs:
  data/aatmf.json            — full nested taxonomy (tactics -> techniques -> mappings)
  data/aatmf-techniques.csv  — flat technique table (spreadsheet / Navigator friendly)

Run from anywhere:  python scripts/build_export.py
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import aatmf_taxonomy as A  # noqa: E402


def main() -> None:
    taxonomy = A.build_taxonomy()
    data_dir = A.REPO_ROOT / "data"
    data_dir.mkdir(exist_ok=True)

    (data_dir / "aatmf.json").write_text(A.serialize_json(taxonomy), encoding="utf-8")

    with open(data_dir / "aatmf-techniques.csv", "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                "tactic_id", "tactic", "technique_id", "title",
                "risk_score", "rating", "procedures", "owasp_llm", "mitre_atlas",
            ]
        )
        for tactic in taxonomy["tactics"]:
            for tech in tactic["techniques"]:
                writer.writerow(
                    [
                        tactic["id"], tactic["name"], tech["id"], tech["title"],
                        tech["risk_score"], tech["rating"], tech["procedures"],
                        ";".join(tech["mappings"]["owasp_llm"]),
                        ";".join(tech["mappings"]["mitre_atlas"]),
                    ]
                )

    counts = taxonomy["counts"]
    print(
        f"Wrote data/aatmf.json and data/aatmf-techniques.csv "
        f"({counts['tactics']} tactics, {counts['techniques']} techniques, "
        f"{counts['procedures']} procedures)."
    )


if __name__ == "__main__":
    main()
