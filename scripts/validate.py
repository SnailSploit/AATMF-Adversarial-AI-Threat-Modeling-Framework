#!/usr/bin/env python3
"""AATMF framework integrity checks.

Fails (exit 1) on structural defects that should never reach main:
  * duplicate technique IDs
  * per-tactic counts that disagree across docs, overview tables, and the README
  * risk badges that don't match the AATMF-R scale
  * overview/card risk-score drift
  * broken relative links
  * unbalanced code fences
  * a stale data/ export

Warnings (non-fatal) flag style drift worth cleaning up.

Run from anywhere:  python scripts/validate.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import aatmf_taxonomy as A  # noqa: E402

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def check_ids_and_counts(taxonomy, readme):
    seen: dict[str, list[str]] = {}
    for tactic in taxonomy["tactics"]:
        for tech in tactic["techniques"]:
            seen.setdefault(tech["id"], []).append(tactic["id"])
    for tid, locs in seen.items():
        if len(locs) > 1:
            err(f"duplicate technique id {tid} appears in {locs}")

    for tactic in taxonomy["tactics"]:
        ch = A.parse_chapter(A.REPO_ROOT / tactic["file"])
        n_over, n_card = len(ch["overview"]), len(ch["cards"])
        declared = readme["tactics"].get(tactic["id"], {}).get("count")
        if n_over != n_card:
            err(f"{tactic['id']}: {n_over} overview rows but {n_card} technique cards")
        if declared is not None and n_over != declared:
            err(f"{tactic['id']}: docs list {n_over} techniques, README says {declared}")
        if ch["subtitle"] and ch["subtitle"]["techniques"] != n_over:
            err(
                f"{tactic['id']}: subtitle claims {ch['subtitle']['techniques']} "
                f"techniques, found {n_over}"
            )
        styles = {c["backticked"] for c in ch["cards"].values()}
        if styles == {False}:
            warn(
                f"{tactic['id']}: technique headings omit the backtick convention "
                f"(### `{tactic['id']}-AT-NNN`)"
            )
        elif len(styles) > 1:
            err(f"{tactic['id']}: mixed technique-heading styles (backticked and not)")

    totals = readme["totals"]
    if totals:
        if totals["techniques"] != taxonomy["counts"]["techniques"]:
            err(
                f"README headline says {totals['techniques']} techniques, "
                f"docs contain {taxonomy['counts']['techniques']}"
            )
        table_sum = sum(v["count"] for v in readme["tactics"].values())
        if table_sum != totals["techniques"]:
            err(
                f"README tactic-table sums to {table_sum}, "
                f"headline says {totals['techniques']}"
            )


def check_risk_badges(taxonomy):
    for tactic in taxonomy["tactics"]:
        ch = A.parse_chapter(A.REPO_ROOT / tactic["file"])
        overview_by_id = {r["id"]: r for r in ch["overview"]}
        for row in ch["overview"]:
            expected = A.rating_for(row["risk_score"])
            if row["rating"] != expected:
                err(
                    f"{row['id']}: overview rating {row['rating']} should be "
                    f"{expected} for score {row['risk_score']}"
                )
        for tid, card in ch["cards"].items():
            if card["risk_score"] is not None and card["rating"]:
                expected = A.rating_for(card["risk_score"])
                if card["rating"] != expected:
                    err(
                        f"{tid}: card rating {card['rating']} should be "
                        f"{expected} for score {card['risk_score']}"
                    )
            ov = overview_by_id.get(tid)
            if ov and card["risk_score"] is not None and ov["risk_score"] != card["risk_score"]:
                err(
                    f"{tid}: overview score {ov['risk_score']} disagrees with "
                    f"card score {card['risk_score']}"
                )


def check_links():
    for path in [A.README, *sorted(A.DOCS.glob("**/*.md"))]:
        for link in A.local_links(path):
            target = link.split("#", 1)[0]
            if not target:
                continue
            if not (path.parent / target).resolve().exists():
                err(f"broken link in {path.relative_to(A.REPO_ROOT)} -> {link}")


def check_fences():
    for path in [A.README, *sorted(A.DOCS.glob("**/*.md"))]:
        fences = sum(
            1 for line in path.read_text(encoding="utf-8").splitlines()
            if line.startswith("```")
        )
        if fences % 2:
            err(f"unbalanced code fences in {path.relative_to(A.REPO_ROOT)} ({fences})")


def check_export_fresh(taxonomy):
    current = A.REPO_ROOT / "data" / "aatmf.json"
    if not current.exists():
        warn("data/aatmf.json missing — run scripts/build_export.py")
        return
    if current.read_text(encoding="utf-8") != A.serialize_json(taxonomy):
        err("data/aatmf.json is stale — run scripts/build_export.py and commit the result")


def check_inline_refs(taxonomy):
    """Flag inline TX-AT-NNN references that don't resolve to a defined technique."""
    import re

    defined = set()
    for tactic in taxonomy["tactics"]:
        for tech in tactic["techniques"]:
            m = re.match(r"T(\d+)-AT-(\d+)", tech["id"])
            defined.add((int(m.group(1)), int(m.group(2))))

    seen: dict[str, set] = {}
    for path in [A.README, *sorted(A.DOCS.glob("**/*.md"))]:
        for m in re.finditer(r"\bT(\d+)-AT-(\d+)\b", path.read_text(encoding="utf-8")):
            key = (int(m.group(1)), int(m.group(2)))
            if key not in defined:
                rid = f"T{m.group(1)}-AT-{m.group(2)}"
                seen.setdefault(rid, set()).add(str(path.relative_to(A.REPO_ROOT)))
    for rid, locs in sorted(seen.items()):
        err(f"reference to undefined technique {rid} in {sorted(locs)}")


def check_ap_ids():
    """Flag duplicate attack-procedure ID definitions (must be globally unique)."""
    import re

    seen: dict[str, list] = {}
    for path in sorted(A.DOCS.glob("**/*.md")):
        for m in re.finditer(r"^\*\*`(T\d+-AP-\d+[A-Z])`", path.read_text(encoding="utf-8"), re.M):
            seen.setdefault(m.group(1), []).append(str(path.relative_to(A.REPO_ROOT)))
    for ap, locs in sorted(seen.items()):
        if len(locs) > 1:
            err(f"duplicate attack-procedure id {ap} defined in {locs}")


def main() -> None:
    taxonomy = A.build_taxonomy()
    readme = A.parse_readme()

    check_ids_and_counts(taxonomy, readme)
    check_risk_badges(taxonomy)
    check_links()
    check_fences()
    check_inline_refs(taxonomy)
    check_ap_ids()
    check_export_fresh(taxonomy)

    counts = taxonomy["counts"]
    print("AATMF integrity check")
    print(
        f"  {counts['tactics']} tactics · {counts['techniques']} techniques · "
        f"{counts['procedures']} procedures"
    )
    for w in warnings:
        print(f"  WARN  {w}")
    for e in errors:
        print(f"  ERROR {e}")

    if errors:
        print(f"\nFAILED — {len(errors)} error(s), {len(warnings)} warning(s).")
        sys.exit(1)
    print(f"\nPASSED — 0 errors, {len(warnings)} warning(s).")


if __name__ == "__main__":
    main()
