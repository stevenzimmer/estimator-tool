# Estimator Agent Workflow

Use this workflow when preparing a construction bid or large project estimate from a new bid package.

## Operating Rules

- Treat historical bids as references, not truth. Always distinguish extracted facts, inferred assumptions, and estimator judgment.
- Do not fill missing quantities or rates silently. Create explicit open questions or assumptions.
- Prefer comparable completed bids from the same project type, scope type, delivery model, geography, and document maturity.
- Keep estimate outputs auditable. Every major number should tie back to source documents, historical comps, rate sheets, or stated assumptions.
- Preserve source files. Put derived notes, takeoffs, and draft outputs in the bid workspace.

## Bid Intake

For each new bid, identify:

- Project name, owner/client, location, and bid due date.
- Delivery model and contract type if available.
- Drawing/specification maturity, such as conceptual, IFC, addendum, or revision number.
- Major scopes included and excluded.
- Required alternates, allowances, contingencies, bonds, taxes, escalation, and markups.
- Schedule milestones and constraints.
- Site, geotech, environmental, access, laydown, weather, and permitting risks.

## Estimating Passes

1. Intake pass: inventory documents, missing files, due dates, and critical risks.
2. Scope pass: split the work into bid packages, inclusions, exclusions, and assumptions.
3. Quantity pass: extract or estimate quantities, then mark confidence by source quality.
4. Rate pass: apply labor, equipment, material, subcontractor, indirect, and escalation rates.
5. Comparison pass: compare against similar completed bids and explain deltas.
6. Risk pass: identify uncertainty, contingency drivers, long-lead items, and commercial exposure.
7. Output pass: prepare estimate summary, backup, bid letter notes, and review checklist.

## Standard Output

Each new bid workspace should contain:

- `working/estimate-brief.md`: primary agent-readable estimate summary.
- `working/open-questions.md`: missing inputs and clarifications.
- `working/assumptions.md`: explicit assumptions used in the estimate.
- `working/risk-register.md`: commercial, scope, site, schedule, and production risks.
- `outputs/`: final bid summaries, exports, and client-facing deliverables.

