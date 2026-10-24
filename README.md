# Vexa — Data Operations Intelligence

**AI-Powered Data Reconciliation, Investigation & Audit Platform**

Vexa is an interactive data operations platform built with Python, Streamlit, SQLite, and Groq LLM. It helps analysts compare reports, identify data quality issues, investigate discrepancies, document decisions, and apply verified corrections.

## Key Features

- **Data Reconciliation:** Compare CSV and Excel reports using matching record identifiers.
- **Data Quality Detection:** Identify missing records, duplicate identifiers, and mismatched values.
- **Investigation Workflow:** Record reviewer decisions, verification notes, and supporting evidence.
- **AI Investigation Assistant:** Use Groq LLM to explore potential causes, business impacts, and recommended validation steps.
- **Human-Approved Corrections:** Apply verified value corrections and duplicate-row deletions to working copies.
- **Audit History:** SQLite-backed audit history for local use and isolated session history for the public demo.
- **Data Export:** Download original reports, corrected reports, difference reports, change logs, and review history.

## Technology Stack

Python · Streamlit · Pandas · SQLite · Groq LLM · OpenPyXL · GitHub

## Data Privacy

Vexa is designed for demonstration using fictional, non-sensitive information. Do not upload real patient records or confidential organizational data.

The public demo uses session-based audit history, while the local version supports persistent SQLite audit records.

## Getting Started

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure your Groq API key privately in Streamlit secrets, then launch:

```bash
streamlit run app.py
```

## Project Purpose

Vexa demonstrates practical skills in data analytics, data quality management, workflow automation, AI-assisted investigation, and human-in-the-loop decision support.
