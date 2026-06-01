"""AATMF taxonomy parser — the single source of truth for repository tooling.

Parses the Markdown tactic chapters and README into a structured taxonomy and
exposes the helpers used by:

  * build_export.py  — emits the machine-readable export under data/
  * validate.py      — runs the CI integrity checks

Standard library only, so it runs on a bare CI image with no pip install.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS = REPO_ROOT / "docs"
README = REPO_ROOT / "README.md"

# Risk scale: (inclusive minimum score, rating, emoji). Highest band first.
RISK_SCALE = [
    (250, "CRITICAL", "🔴"),
    (200, "HIGH", "🟠"),
    (150, "MEDIUM", "🟡"),
    (100, "LOW", "🔵"),
    (0, "INFO", "⚪"),
]


def rating_for(score: int) -> str:
    """Return the canonical rating word for a numeric risk score."""
    for low, name, _ in RISK_SCALE:
        if score >= low:
            return name
    return "INFO"


# --- Markdown patterns -------------------------------------------------------

_TACTIC_FILE_RE = re.compile(r"(\d+)-t(\d+)-[a-z0-9-]+\.md$")
_H1_RE = re.compile(r"^#\s+(T\d+)\s+[—-]\s+(.+?)\s*$", re.M)
_SUBTITLE_RE = re.compile(
    r">\s*\*\*(\d+)\s+Techniques\*\*\s*·\s*\*\*(\d+)\s+Attack Procedures\*\*"
    r"\s*·\s*Risk Range:\s*(\d+)\s*[–-]\s*(\d+)"
)
# Overview table row, e.g.  | `T1-AT-001` | Dialogue Hijacking | 190 | 🟡 MEDIUM | 10 |
_OVERVIEW_ROW_RE = re.compile(
    r"^\|\s*`?(T\d+-AT-\d+)`?\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|",
    re.M,
)
# Technique card heading, with or without backticks around the id.
_CARD_HEAD_RE = re.compile(r"^###\s+(`?)(T\d+-AT-\d+)`?\s+[—-]\s+(.+?)\s*$", re.M)
_RISK_LINE_RE = re.compile(r"\*\*Risk Score:\*\*\s*(\d+)\s*\S*\s*([A-Z]+)")
_OWASP_LLM_RE = re.compile(r"\*\*OWASP LLM:\*\*\s*([^\n|]+)")
_OWASP_ASI_RE = re.compile(r"\*\*OWASP ASI:\*\*\s*([^\n|]+)")
_ATLAS_RE = re.compile(r"\*\*MITRE ATLAS:\*\*\s*([^\n]+)")

_TOKEN_LLM = re.compile(r"LLM\d{2}")
_TOKEN_ASI = re.compile(r"ASI\d{2}")
_TOKEN_ATLAS = re.compile(r"AML\.T\d+(?:\.\d+)?")

# README tactic-table row and headline totals.
_README_ROW_RE = re.compile(r"<code>(T\d+)</code>.*?<b>(.*?)</b></td><td>(\d+)</td>", re.S)
_README_TOTALS_RE = re.compile(
    r"(\d+)\s+Tactics\s*·\s*(\d+)\s+Techniques\s*·\s*([\d,]+)\+?\s+Attack Procedures"
)


def _rating_word(cell: str) -> str:
    match = re.search(r"[A-Z]{3,}", cell)
    return match.group(0) if match else cell.strip()


def _unescape(text: str) -> str:
    return text.replace("&amp;", "&").strip()


def tactic_files() -> dict[int, Path]:
    """Map tactic number -> chapter file, ordered by tactic number."""
    out: dict[int, Path] = {}
    for path in DOCS.glob("vol-*/*.md"):
        match = _TACTIC_FILE_RE.search(path.name)
        if match:
            out[int(match.group(2))] = path
    return dict(sorted(out.items()))


def parse_chapter(path: Path) -> dict:
    """Parse a single tactic chapter into its structural pieces."""
    text = path.read_text(encoding="utf-8")

    h1 = _H1_RE.search(text)
    code = h1.group(1) if h1 else None
    name = h1.group(2).strip() if h1 else None

    sub = _SUBTITLE_RE.search(text)
    subtitle = None
    if sub:
        subtitle = {
            "techniques": int(sub.group(1)),
            "procedures": int(sub.group(2)),
            "risk_min": int(sub.group(3)),
            "risk_max": int(sub.group(4)),
        }

    overview = []
    for m in _OVERVIEW_ROW_RE.finditer(text):
        tid, title, score, rating, procs = m.groups()
        digits = re.search(r"\d+", procs)
        overview.append(
            {
                "id": tid,
                "title": title.strip(),
                "risk_score": int(score),
                "rating": _rating_word(rating),
                "procedures": int(digits.group(0)) if digits else None,
            }
        )

    cards: dict[str, dict] = {}
    heads = list(_CARD_HEAD_RE.finditer(text))
    for i, m in enumerate(heads):
        tid = m.group(2)
        start = m.end()
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        nxt_section = text.find("\n## ", start)
        if nxt_section != -1 and nxt_section < end:
            end = nxt_section
        body = text[start:end]

        risk = _RISK_LINE_RE.search(body)
        mappings = {"owasp_llm": [], "owasp_asi": [], "mitre_atlas": []}
        if (ml := _OWASP_LLM_RE.search(body)):
            mappings["owasp_llm"] = sorted(set(_TOKEN_LLM.findall(ml.group(1))))
        if (ma := _OWASP_ASI_RE.search(body)):
            mappings["owasp_asi"] = sorted(set(_TOKEN_ASI.findall(ma.group(1))))
        if (mt := _ATLAS_RE.search(body)):
            mappings["mitre_atlas"] = sorted(set(_TOKEN_ATLAS.findall(mt.group(1))))

        cards[tid] = {
            "title": m.group(3).strip(),
            "risk_score": int(risk.group(1)) if risk else None,
            "rating": risk.group(2) if risk else None,
            "mappings": mappings,
            "backticked": m.group(1) == "`",
        }

    return {
        "code": code,
        "number": int(code[1:]) if code else None,
        "name": name,
        "file": str(path.relative_to(REPO_ROOT)),
        "volume": path.parent.name,
        "subtitle": subtitle,
        "overview": overview,
        "cards": cards,
    }


def build_taxonomy() -> dict:
    """Merge every chapter's overview + cards into the full taxonomy object."""
    tactics = []
    for _, path in tactic_files().items():
        ch = parse_chapter(path)
        techniques = []
        for row in ch["overview"]:
            card = ch["cards"].get(row["id"], {})
            techniques.append(
                {
                    "id": row["id"],
                    "title": row["title"],
                    "risk_score": row["risk_score"],
                    "rating": row["rating"],
                    "procedures": row["procedures"],
                    "mappings": card.get(
                        "mappings",
                        {"owasp_llm": [], "owasp_asi": [], "mitre_atlas": []},
                    ),
                }
            )
        tactics.append(
            {
                "id": ch["code"],
                "number": ch["number"],
                "name": ch["name"],
                "volume": ch["volume"],
                "file": ch["file"],
                "technique_count": len(techniques),
                "techniques": techniques,
            }
        )

    total_t = sum(t["technique_count"] for t in tactics)
    total_p = sum((x["procedures"] or 0) for t in tactics for x in t["techniques"])
    return {
        "framework": "AATMF",
        "name": "Adversarial AI Threat Modeling Framework",
        "version": "3",
        "source": "generated from docs/ by scripts/build_export.py — do not edit by hand",
        "risk_scale": [{"min": lo, "rating": r, "emoji": e} for lo, r, e in RISK_SCALE],
        "counts": {"tactics": len(tactics), "techniques": total_t, "procedures": total_p},
        "tactics": tactics,
    }


def serialize_json(taxonomy: dict) -> str:
    """Canonical JSON serialization shared by the exporter and the validator."""
    return json.dumps(taxonomy, ensure_ascii=False, indent=2) + "\n"


def parse_readme() -> dict:
    text = README.read_text(encoding="utf-8")
    tactics = {
        m.group(1): {"name": _unescape(m.group(2)), "count": int(m.group(3))}
        for m in _README_ROW_RE.finditer(text)
    }
    totals = None
    if (tot := _README_TOTALS_RE.search(text)):
        totals = {
            "tactics": int(tot.group(1)),
            "techniques": int(tot.group(2)),
            "procedures": int(tot.group(3).replace(",", "")),
        }
    return {"tactics": tactics, "totals": totals}


_LINK_RE = re.compile(r"\]\(([^)]+)\)")
_HREF_RE = re.compile(r'(?:href|src)="([^"]+)"')


def local_links(path: Path):
    """Yield the relative (non-external, non-anchor) link targets in a file."""
    text = Path(path).read_text(encoding="utf-8")
    for link in set(_LINK_RE.findall(text)) | set(_HREF_RE.findall(text)):
        if link.startswith(("http://", "https://", "#", "mailto:")):
            continue
        yield link
