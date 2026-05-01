#!/usr/bin/env python3
"""Local scaffolding for a construction estimate agent workspace.

The script intentionally uses only Python's standard library so it can run
before the project chooses an app framework, database, or LLM provider.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PAST_BIDS = ROOT / "past-bids"
NEW_BIDS = ROOT / "new-bids"
KNOWLEDGE_BASE = ROOT / "knowledge-base"
INDEX_PATH = KNOWLEDGE_BASE / "past-bids-index.json"

DOC_TYPE_RULES: list[tuple[str, str]] = [
    ("base_bid", r"\bbase\b.*\bbid\b|\bbid\b.*\bbase\b"),
    ("scope_of_work", r"\bscope\b|\bsow\b"),
    ("civil_drawings", r"\bcivil\b|\b_ifc\b|\bifc\b"),
    ("schedule", r"\bschedule\b|\bbaseline\b"),
    ("geotech", r"\bgeotech\b|\bgeotechnical\b"),
    ("grading", r"\bgrading\b"),
    ("structural", r"\bstructural\b"),
    ("environmental", r"\benvironmental\b|\beis\b"),
    ("labor_rates", r"\blabor\b|\bhourly\b|\brates?\b.*\bt&m\b"),
    ("equipment_material_rates", r"\bequipment\b|\bmaterial\b"),
]

SUPPORTED_EXTENSIONS = {".docx", ".xlsx", ".pdf"}


@dataclass(frozen=True)
class FileSummary:
    path: str
    name: str
    extension: str
    document_type: str
    size_bytes: int
    extracted: dict[str, Any]


def classify_document(path: Path) -> str:
    normalized = path.stem.lower().replace("_", " ")
    for doc_type, pattern in DOC_TYPE_RULES:
        if re.search(pattern, normalized):
            return doc_type
    return "unclassified"


def clean_text(value: str) -> str:
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def extract_docx(path: Path, max_chars: int = 12_000) -> dict[str, Any]:
    try:
        with zipfile.ZipFile(path) as archive:
            xml = archive.read("word/document.xml")
    except (KeyError, zipfile.BadZipFile, OSError) as exc:
        return {"status": "error", "error": str(exc)}

    root = ET.fromstring(xml)
    paragraphs: list[str] = []

    for paragraph in root.iter(
        "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"
    ):
        parts = [
            node.text or ""
            for node in paragraph.iter(
                "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"
            )
        ]
        text = clean_text("".join(parts))
        if text:
            paragraphs.append(text)

    joined = "\n".join(paragraphs)
    return {
        "status": "ok",
        "paragraph_count": len(paragraphs),
        "text_preview": joined[:max_chars],
    }


def xlsx_shared_strings(archive: zipfile.ZipFile, limit: int = 50_000) -> list[str]:
    try:
        with archive.open("xl/sharedStrings.xml") as handle:
            strings: list[str] = []
            for _, elem in ET.iterparse(handle, events=("end",)):
                if elem.tag.endswith("}si"):
                    text = "".join(node.text or "" for node in elem.iter() if node.text)
                    strings.append(clean_text(text))
                    elem.clear()
                    if len(strings) >= limit:
                        break
            return strings
    except KeyError:
        return []


def workbook_sheet_paths(archive: zipfile.ZipFile) -> list[tuple[str, str]]:
    namespaces = {
        "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
        "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
        "office_rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    }

    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))

    rel_by_id = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in rels.findall("rel:Relationship", namespaces)
    }

    sheets: list[tuple[str, str]] = []
    for sheet in workbook.findall("main:sheets/main:sheet", namespaces):
        name = sheet.attrib.get("name", "Unnamed sheet")
        rel_id = sheet.attrib.get(
            "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
        )
        target = rel_by_id.get(rel_id or "")
        if not target:
            continue
        sheet_path = "xl/" + target.lstrip("/")
        sheets.append((name, sheet_path))
    return sheets


def xlsx_cell_value(cell: ET.Element, shared_strings: list[str]) -> str:
    cell_type = cell.attrib.get("t")
    value_node = None
    for child in cell:
        if child.tag.endswith("}v"):
            value_node = child
            break

    if value_node is None or value_node.text is None:
        inline_text = "".join(node.text or "" for node in cell.iter() if node.text)
        return clean_text(inline_text)

    raw_value = value_node.text
    if cell_type == "s":
        try:
            return shared_strings[int(raw_value)]
        except (ValueError, IndexError):
            return raw_value
    return raw_value


def extract_xlsx(path: Path, max_sheets: int = 40, max_rows: int = 12) -> dict[str, Any]:
    try:
        with zipfile.ZipFile(path) as archive:
            shared_strings = xlsx_shared_strings(archive)
            sheets = workbook_sheet_paths(archive)
            summaries: list[dict[str, Any]] = []

            for sheet_name, sheet_path in sheets[:max_sheets]:
                sample_rows: list[list[str]] = []
                non_empty_cells = 0

                try:
                    with archive.open(sheet_path) as handle:
                        for _, row in ET.iterparse(handle, events=("end",)):
                            if not row.tag.endswith("}row"):
                                continue
                            values = [
                                xlsx_cell_value(cell, shared_strings)
                                for cell in row
                                if cell.tag.endswith("}c")
                            ]
                            values = [value for value in values if value != ""]
                            non_empty_cells += len(values)
                            if values and len(sample_rows) < max_rows:
                                sample_rows.append(values[:12])
                            row.clear()
                except KeyError:
                    sample_rows.append(["Could not read sheet XML"])

                summaries.append(
                    {
                        "name": sheet_name,
                        "non_empty_cells_sampled": non_empty_cells,
                        "sample_rows": sample_rows,
                    }
                )

            return {
                "status": "ok",
                "sheet_count": len(sheets),
                "sheets": summaries,
                "shared_strings_indexed": len(shared_strings),
            }
    except (KeyError, zipfile.BadZipFile, OSError, ET.ParseError) as exc:
        return {"status": "error", "error": str(exc)}


def summarize_pdf(path: Path) -> dict[str, Any]:
    return {
        "status": "metadata_only",
        "note": "PDF text extraction is not configured yet.",
        "file_size_mb": round(path.stat().st_size / 1_000_000, 2),
    }


def summarize_file(path: Path) -> FileSummary:
    extension = path.suffix.lower()
    extracted: dict[str, Any]

    if extension == ".docx":
        extracted = extract_docx(path)
    elif extension == ".xlsx":
        extracted = extract_xlsx(path)
    elif extension == ".pdf":
        extracted = summarize_pdf(path)
    else:
        extracted = {"status": "skipped", "note": "Unsupported extension"}

    return FileSummary(
        path=str(path.relative_to(ROOT)),
        name=path.name,
        extension=extension,
        document_type=classify_document(path),
        size_bytes=path.stat().st_size,
        extracted=extracted,
    )


def index_past_bids() -> dict[str, Any]:
    KNOWLEDGE_BASE.mkdir(exist_ok=True)
    projects: list[dict[str, Any]] = []

    if not PAST_BIDS.exists():
        PAST_BIDS.mkdir()

    for project_dir in sorted(path for path in PAST_BIDS.iterdir() if path.is_dir()):
        files = [
            summarize_file(path)
            for path in sorted(project_dir.iterdir())
            if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
        ]
        projects.append(
            {
                "name": project_dir.name,
                "path": str(project_dir.relative_to(ROOT)),
                "file_count": len(files),
                "document_types": sorted({file.document_type for file in files}),
                "files": [file.__dict__ for file in files],
            }
        )

    index = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "root": str(ROOT),
        "project_count": len(projects),
        "projects": projects,
    }

    INDEX_PATH.write_text(json.dumps(index, indent=2), encoding="utf-8")
    return index


def safe_project_name(name: str) -> str:
    normalized = re.sub(r"[^\w\s.-]", "", name).strip()
    normalized = re.sub(r"\s+", " ", normalized)
    if not normalized:
        raise ValueError("Project name must contain at least one letter or number.")
    return normalized


def create_new_bid(name: str) -> Path:
    project_name = safe_project_name(name)
    project_dir = NEW_BIDS / project_name
    for child in ("source-files", "working", "outputs"):
        (project_dir / child).mkdir(parents=True, exist_ok=True)

    intake_path = project_dir / "working" / "intake.md"
    if not intake_path.exists():
        intake_path.write_text(
            f"""# {project_name} Intake

## Known Facts

- Project:
- Client/owner:
- Location:
- Bid due date:
- Delivery model:
- Drawing/spec maturity:

## Source Files

Place incoming documents in `../source-files/`.

## Missing Inputs

- 

""",
            encoding="utf-8",
        )
    return project_dir


def load_index() -> dict[str, Any]:
    if not INDEX_PATH.exists():
        return index_past_bids()
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))


def comparable_bid_summary(index: dict[str, Any]) -> str:
    if not index.get("projects"):
        return "No historical bids have been indexed yet."

    lines: list[str] = []
    for project in index["projects"]:
        doc_types = ", ".join(project.get("document_types", [])) or "none"
        lines.append(
            f"- {project['name']}: {project['file_count']} indexed files; "
            f"document types: {doc_types}"
        )
    return "\n".join(lines)


def source_file_inventory(project_dir: Path) -> str:
    source_dir = project_dir / "source-files"
    files = sorted(path for path in source_dir.iterdir() if path.is_file())
    if not files:
        return "- No source files added yet."
    return "\n".join(
        f"- {path.name} ({path.suffix.lower() or 'no extension'}, "
        f"{round(path.stat().st_size / 1_000_000, 2)} MB)"
        for path in files
    )


def draft_estimate(name: str) -> Path:
    project_dir = create_new_bid(name)
    index = load_index()
    brief_path = project_dir / "working" / "estimate-brief.md"
    questions_path = project_dir / "working" / "open-questions.md"
    assumptions_path = project_dir / "working" / "assumptions.md"
    risk_path = project_dir / "working" / "risk-register.md"

    brief_path.write_text(
        f"""# {project_dir.name} Estimate Brief

Generated: {dt.datetime.now().isoformat(timespec="seconds")}

## Source File Inventory

{source_file_inventory(project_dir)}

## Historical Bid Context

{comparable_bid_summary(index)}

## Estimate Build Plan

1. Confirm bid due date, client instructions, commercial terms, and deliverables.
2. Inventory drawings, specifications, addenda, schedule, geotech, environmental, and scope documents.
3. Build the work breakdown structure and map source documents to each scope.
4. Extract quantities and tag each quantity as source-backed, calculated, historical-comparable, or assumed.
5. Apply labor, equipment, material, subcontract, indirect, escalation, contingency, and markup rates.
6. Compare totals and production assumptions against historical completed bids.
7. Resolve open questions or carry explicit qualifications into the bid.

## Work Breakdown Starter

| Scope | Quantity Source | Rate Source | Confidence | Notes |
| --- | --- | --- | --- | --- |
| Civil / sitework | TBD | TBD | Low | Review civil drawings and grading workflow. |
| Structural / foundations | TBD | TBD | Low | Review structural report and install assumptions. |
| Electrical / collection | TBD | TBD | Low | Add when electrical drawings are available. |
| Labor | TBD | Historical labor rates | Low | Normalize crew makeup, shifts, overtime, and per diem. |
| Equipment | TBD | Historical equipment rates | Low | Confirm owned vs rented and utilization assumptions. |
| Indirects / general conditions | TBD | Historical bid backup | Low | Tie to schedule duration and staffing plan. |

## Required Outputs

- Estimate summary.
- Detailed estimate backup.
- Inclusions, exclusions, and qualifications.
- Open questions log.
- Risk and contingency register.
- Historical comparison notes.

""",
        encoding="utf-8",
    )

    if not questions_path.exists():
        questions_path.write_text(
            """# Open Questions

- What is the bid due date and required submission format?
- Are there addenda, alternates, allowances, or owner-furnished items?
- Which scopes are in contract and which are excluded?
- What labor agreement, wage determination, per diem, shift, and overtime assumptions apply?
- What schedule milestones constrain production, staffing, or equipment utilization?

""",
            encoding="utf-8",
        )

    if not assumptions_path.exists():
        assumptions_path.write_text(
            """# Assumptions

- Quantities are not final until tied to source drawings, specs, or takeoff backup.
- Historical rates require normalization for date, location, labor terms, and scope differences.
- Missing documents are treated as estimate risk, not zero cost.

""",
            encoding="utf-8",
        )

    if not risk_path.exists():
        risk_path.write_text(
            """# Risk Register

| Risk | Category | Impact | Mitigation / Bid Qualification |
| --- | --- | --- | --- |
| Missing or incomplete bid documents | Scope | TBD | Carry open question or qualify exclusion. |
| Geotechnical uncertainty | Site | TBD | Review geotech report and foundation assumptions. |
| Schedule compression | Schedule | TBD | Compare required milestones against production plan. |
| Environmental constraints | Permitting | TBD | Review EIS and permit obligations. |

""",
            encoding="utf-8",
        )

    return brief_path


def print_index_summary(index: dict[str, Any]) -> None:
    print(f"Indexed {index['project_count']} historical bid project(s).")
    print(f"Wrote {INDEX_PATH.relative_to(ROOT)}")
    for project in index["projects"]:
        print(
            f"- {project['name']}: {project['file_count']} files "
            f"({', '.join(project['document_types'])})"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Local tools for construction bid estimation workspaces."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("index", help="Index completed bids in past-bids/.")

    new_bid = subparsers.add_parser("new-bid", help="Create a new bid workspace.")
    new_bid.add_argument("name", help="Project name for the new bid.")

    draft = subparsers.add_parser("draft", help="Draft an estimate workspace.")
    draft.add_argument("name", help="Project name in new-bids/.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "index":
            print_index_summary(index_past_bids())
            return 0

        if args.command == "new-bid":
            project_dir = create_new_bid(args.name)
            print(f"Created {project_dir.relative_to(ROOT)}")
            return 0

        if args.command == "draft":
            brief_path = draft_estimate(args.name)
            print(f"Wrote {brief_path.relative_to(ROOT)}")
            return 0
    except ValueError as exc:
        parser.error(str(exc))

    return 1


if __name__ == "__main__":
    sys.exit(main())
