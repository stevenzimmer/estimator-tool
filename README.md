# Construction Estimator Agent

This folder is an offline-first workspace for building construction bids and large project estimates from historical bid packages.

The intended workflow is:

1. Put completed bid packages in `past-bids/<project-name>/`.
2. Run the indexer so the agent can learn what documents and estimate workbooks exist.
3. Put incoming bid packages in `new-bids/<project-name>/source-files/`.
4. Generate a working estimate folder with checklists, assumptions, risk notes, and historical reference context.
5. Refine the workflow as more completed bids are added.

## Current Structure

```text
past-bids/              Completed bids and source artifacts.
new-bids/               New opportunities being estimated.
knowledge-base/         Generated historical bid index.
tools/                  Local command-line tooling.
workflows/              Agent instructions and estimating workflow.
```

## Quick Start

Index historical bids:

```bash
python3 tools/estimator_agent.py index
```

Create a new bid workspace:

```bash
python3 tools/estimator_agent.py new-bid "Project Name"
```

After adding source files to `new-bids/Project Name/source-files/`, draft the estimate workspace:

```bash
python3 tools/estimator_agent.py draft "Project Name"
```

## What The Tool Does Today

- Scans completed bids in `past-bids/`.
- Classifies documents by filename, such as base bid, scope, civil, schedule, geotech, structural, environmental, labor rates, and equipment rates.
- Extracts basic text from DOCX files.
- Extracts workbook structure and sample rows from XLSX files without requiring external Python packages.
- Creates repeatable new-bid folder structures.
- Generates a Markdown estimating brief for a new bid.

## Known Limits

- PDF text is not extracted yet unless a PDF parser is added later. PDFs are still indexed by filename, size, and document type.
- Cost normalization, quantity takeoff, production rates, and schedule logic are placeholders until more historical bids are added.
- The tool does not call an LLM yet. It creates structured context that an agent can use reliably.

