# Repository Guidelines

## Project Structure & Module Organization

This repository is an offline-first workspace for construction bid estimation.

- `tools/estimator_agent.py` contains the local CLI for indexing past bids and creating new bid workspaces.
- `workflows/estimator-agent.md` defines the estimating workflow and agent operating rules.
- `knowledge-base/` stores generated indexes and reusable estimating context, currently `past-bids-index.json` and `libra-bid-feedback.md`.
- `final_estimate_template.md` is the standard customer-facing final estimate output template.
- `past-bids/<project-name>/` stores completed bid packages used as historical references.
- `new-bids/<project-name>/` stores active estimate workspaces with `source-files/`, `working/`, and `outputs/`.

Bid source files can be large and sensitive. Keep generated notes and outputs separate from original source documents.

## Build, Test, and Development Commands

Run commands from the repository root:

```bash
python3 tools/estimator_agent.py index
```

Indexes completed bid packages under `past-bids/` and writes `knowledge-base/past-bids-index.json`.

```bash
python3 tools/estimator_agent.py new-bid "Project Name"
```

Creates a new bid workspace under `new-bids/Project Name/`.

```bash
python3 tools/estimator_agent.py draft "Project Name"
```

Creates or refreshes the working estimate brief for a new bid.

```bash
python3 -m py_compile tools/estimator_agent.py
python3 -m json.tool knowledge-base/past-bids-index.json >/dev/null
```

Performs lightweight syntax and generated JSON validation.

## Estimating Artifacts

Use `final_estimate_template.md` for final estimate outputs. Preserve the major sections unless there is a project-specific reason to omit them: total estimate, scope breakdown, inclusions, exclusions, assumptions, alternates, schedule basis, labor/equipment basis, historical comparison, risks, open items, source documents, and approvals.

Add reusable lessons learned to `knowledge-base/<project-name>-bid-feedback.md` after reviewing a completed bid. Keep feedback structured around what improved the bid, what documents mattered, what was missing, and what should become context for future estimates.

## Coding Style & Naming Conventions

Use Python 3.11+ standard library unless a dependency is clearly justified. Keep CLI behavior deterministic and safe for local/offline use. Prefer explicit names such as `index_past_bids`, `create_new_bid`, and `draft_estimate`. Use 4-space indentation, type hints for new functions, and concise comments only where parsing or estimating logic is not obvious.

Use lowercase hyphenated names for Markdown files and generated workflow artifacts, for example `estimate-brief.md` and `open-questions.md`.

## Testing Guidelines

There is no formal test suite yet. For changes to the CLI, run:

```bash
python3 -m py_compile tools/estimator_agent.py
python3 tools/estimator_agent.py index
```

If you modify JSON generation, validate the generated index with `python3 -m json.tool`. When adding tests later, prefer `tests/test_estimator_agent.py` and keep fixtures small; do not copy large bid packages into tests.

## Commit & Pull Request Guidelines

This repository currently has only an initial `first` commit, so no durable commit convention is established. Use short imperative commit messages, for example `Add bid indexing CLI` or `Document estimator workflow`.

Pull requests should describe the estimating workflow impact, list validation commands run, and call out any assumptions about bid documents, rates, or generated outputs. Do not include confidential bid source files unless explicitly approved.

## Security & Configuration Tips

Treat `past-bids/` and `new-bids/` as sensitive. The `.gitignore` excludes bid folders and generated indexes by default. Review any generated output before sharing externally because it may include extracted scope text, rates, or project-specific assumptions.

## Recommended Agent Skills

Prioritize skills that close current workflow gaps:

- PDF/document extraction for reports, drawings, schedules, and environmental documents.
- Spreadsheet analysis for workbook structure, summary detection, formula tracing, and rate normalization.
- Technical proposal writing for customer-facing bid summaries, qualifications, and exclusions.
- Domain estimating review for risk registers, contingency basis, assumptions, and scope coverage checks.
