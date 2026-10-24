# Vexa — MVP 1: Healthcare operations CSV quality checker

A runnable Streamlit app for **synthetic, non-patient** service records. It identifies missing data, invalid dates, duplicate request IDs, unrecognized statuses, and illustrative overdue follow-ups. Python/pandas cleans and checks records; SQLite executes a real SQL status summary.

## Run locally

1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Run `pip install -r requirements.txt`.
4. Run `streamlit run app.py`.
5. Download the sample CSV from the app, or upload `sample_requests.csv` to test.

## Expected CSV columns
`request_id, service_type, status, assigned_team, last_updated`

`last_updated` should be an ISO date, e.g. `2026-10-20`. Recognized statuses: `Open`, `In Progress`, `Closed`. For the demo, open work untouched for **more than seven days** is flagged for review; this is only an illustrative business rule.

## What is real vs simulated?

- **Working:** CSV upload, pandas checks, SQLite SQL aggregation, flags, filters, downloads.
- **Not implemented yet:** AI explanations, approval workflow, persistent audit trail, integrations.
- **Synthetic data only:** no client/patient data and no claims about any named company’s actual operations.
- Date-sensitive flags are calculated relative to the day the app runs.

## First business question
Which operational records need manual review, and which types of issues appear most often?
