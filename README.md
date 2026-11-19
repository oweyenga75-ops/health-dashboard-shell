# MedPulse Health Systems — Executive Clinical & M&E Analytics Portal

An interactive Streamlit executive analytics platform designed to monitor multi-facility clinical service volumes, maternal and neonatal outcomes, quality-of-care audits, financial solvency, patient satisfaction, and staff mentorship across a network of 38 healthcare facilities.

> **Disclaimer:** All facility names, regional labels, staff records, and clinical/financial figures in this repository are **100% synthetic mock data** generated via `generate_mock_data.py` for portfolio demonstration purposes.

## Demo Access
- **Portal Passkey:** `Demo2026!`

## Key Modules
- **Executive Summary & DDIU Brief:** High-level KPI scorecards, period-over-period comparisons, and automated PDF executive report generation.
- **Clinical & Volume Analytics (OPD, ANC, Deliveries):** Outpatient workload trends, antenatal care retention, and maternal/neonatal indicator tracking.
- **Facility 360° Deep-Dive:** Single-facility diagnostic scorecard combining clinical volume, quality compliance, and patient satisfaction.
- **Quality & Standards Compliance (QSC):** Baseline-to-endline module tracking across medical and management cohorts with statistical significance testing.
- **Financial Solvency & Sustainability:** Facility revenue vs. expense tracking, operating margin analysis, and cost-recovery monitoring.
- **Patient Satisfaction Survey (PSS):** Rolling 12-month exit-interview satisfaction trajectories against an 80% target benchmark.
- **Mentee & Capacity Building Tracker:** Session delivery modes, cadre reach, and facility mentorship coverage matrix.

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 generate_mock_data.py
streamlit run app.py
