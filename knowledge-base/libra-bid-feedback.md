# Libra Past Bid Feedback

Generated for future estimating context. This review is based on the indexed files in `past-bids/Libra/`, with detailed extraction available for the DOCX and XLSX files. PDF files were reviewed by filename/metadata only because local PDF text extraction is not currently configured.

## Package Reviewed

| Document Type | File | Observed Value |
| --- | --- | --- |
| Base estimate workbook | `BASE BID - SGC 25-143 Libra Solar IFC Rev 3 RZ DP.xlsx` | Major estimate model with 360 sheets covering production, equipment, labor, materials, scope activities, conversions, and summary tabs. |
| Scope of work | `SCOPE OF WORK - 2. WO - Scope Attachment_Stockbridge_Libra 02.12.2026.docx` | Strong scope narrative for earthwork, site rules, work hours, SWPPP, water, surveying, safety, QA/QC, and exclusions. |
| Labor rates | `LABOR RATES - Hourly Rates T&M (SOLV).xlsx` | Straight time, time-and-a-half, and double-time labor rates by role. |
| Equipment/material rates | `EQUIPMENT & MATERIAL RATES.xlsx` | T&M rates for equipment, fuel assumptions, non-union manpower, and material unit pricing. |
| Civil drawings | `CIVIL - 2025.12.19_SBLIBRA_HV_C_IFC.pdf` | Required for quantity validation and scope interpretation. |
| Geotech report | `GEOTECH REPORT - 4.3 Libra Solar_Geotech Report.pdf` | Required for rock, excavation, compaction, subgrade, and soil-condition assumptions. |
| Structural report | `STRUCTURAL REPORT - AWM Structural Report, Libra, NS Runs, 500-600lb Install Tension, 12-19-2025.pdf` | Required for foundation / pile installation assumptions and constructability risk. |
| Environmental impact statement | `ENVIRONMENTAL IMPACT STATEMENT - 7.4.8 Libra Solar Project Final EIS 508_MXF (1).pdf` | Required for environmental restrictions, mitigation, access, and compliance risks. |
| Grading workflow | `GRADING - Libra Solar - Grading Workflow.pdf` | Important for sequencing, production logic, and equipment planning. |
| Schedule | `SCHEDULE - 25446017 Libra PV - B12G - (DD 12.29.25) - EPC BASELINE 20251230 7pm.pdf` | Required for crew loading, indirects, escalation, and schedule-risk review. |

## Overall Assessment

The Libra package is useful as an internal estimating reference because it includes estimate backup, rate sheets, scope language, and major technical inputs. It is less complete as a final customer-facing bid record because it does not clearly show the final submitted proposal, final price summary, revision history, decision log, or a direct trace from customer requirements to priced scope.

The strongest artifacts are the base bid workbook and scope attachment. The base bid workbook appears to include detailed production templates for civil/sitework activities such as rock removal, rip rap, trenching/backfill, concrete canvas, mobilization, SWPPP, water hauling, clearing, grading, and site management. The scope attachment clearly defines earthwork responsibilities, site procedures, exclusions, schedule/work-hour assumptions, safety requirements, QA/QC expectations, water hauling, SWPPP responsibilities, and environmental compliance obligations.

## What Could Be Improved

- Add a final customer-facing bid summary that states the final price, bid version, bid date, scope included, major exclusions, alternates, and commercial assumptions.
- Add a revision log tying documents, addenda, drawing revisions, and workbook versions to the submitted estimate.
- Add a scope-to-cost matrix showing which workbook tabs support each priced scope line.
- Add a quantity takeoff register with source sheet/page references, takeoff method, units, and confidence level.
- Add an assumptions and qualifications register separate from the subcontract scope language.
- Add a risk and contingency register explaining how geotech, environmental, schedule, rock, water, dewatering, and access risks were priced or excluded.
- Add a bid review / approval record showing estimator, reviewer, approver, date, and major review comments.
- Clean workbook sheet naming and duplicate tabs where possible. Repeated sheets such as multiple `Pond Side Rip Rap` and `Trench-Backfill DC` versions make it harder to identify which tab drove the final number.
- Clarify whether the workbook is budgetary or final. The extracted summary language includes budgetary caveats, which would conflict with use as a final bid unless updated.

## Information Most Important To The Final Bid

- Final bid amount and pricing breakdown by major scope.
- Basis of estimate, including drawing set, specifications, addenda, scope documents, schedule, and reports used.
- Inclusions and exclusions, especially SWPPP, survey/staking, inspection fees, hazardous material handling, dewatering, soil stabilization, design, environmental mitigation, and construction water.
- Quantity takeoffs and production assumptions for roads, grading, trenching/backfill, rip rap, rock removal, SWPPP, mobilization, laydown, and water hauling.
- Labor basis, including crew makeup, wage/rate source, overtime, per diem/subsistence, shift schedule, and work calendar.
- Equipment basis, including owned/rented assumptions, monthly rates, fuel cost, utilization, and standby/move-in assumptions.
- Schedule basis, including milestones, work hours, calendar assumptions, weather/non-work days, and sequence constraints.
- Geotechnical basis, especially rock, compaction, excavation conditions, subgrade treatment, and unsuitable material assumptions.
- Environmental and permitting obligations that affect access, sequencing, mitigation, restoration, and productivity.
- Commercial terms, including taxes, bonds, insurance, escalation, contingency, overhead, profit, retainage, payment terms, and change-order / T&M rates.

## Missing Or Helpful Additions For Customer Understanding

- Final proposal letter or submitted bid form.
- Executive summary explaining what the customer is buying in plain language.
- Customer-facing price summary by scope area rather than only internal workbook detail.
- Alternates, allowances, unit prices, and deduct/add options.
- Addenda log and document-control register.
- Clear statement of bid validity period and escalation assumptions.
- Clarification of responsibilities between contractor, subcontractor, owner, surveyor, inspector, SWPPP designer, and utility providers.
- Schedule narrative explaining how the bid supports the baseline schedule.
- Explicit statement of open items, unresolved RFIs, and assumptions carried into price.
- Vendor/subcontractor quote log for major materials, hauling, disposal, specialty scopes, or rental equipment.
- Contingency explanation showing what risks are covered versus excluded.
- Customer-ready qualifications for high-risk exclusions such as dewatering, hazardous materials, unsuitable soils, rock, environmental mitigation, and water availability.

## Guidance For Future Bids

Use the Libra package as a strong internal estimating template for civil/sitework production buildup, labor/equipment rate logic, and scope language. Do not use it alone as a model for final customer deliverables. Future bid packages should include both the internal estimate backup and a clean customer-facing output using `final_estimate_template.md`.

For future estimate automation, extract and preserve these fields from every completed bid:

- Final submitted price and pricing date.
- Estimate version and source document revisions.
- Scope line items and final cost by scope.
- Quantity, unit, source document, and confidence level.
- Labor/equipment/material/subcontractor rate source.
- Inclusions, exclusions, assumptions, and qualifications.
- Schedule duration, crew plan, and productivity assumptions.
- Risk register and contingency basis.
- Bid review notes and final approval.
