---
title: "Appendix B: Analytical Pipeline"
---

# Appendix B — Analytical Pipeline

This appendix documents the script sequence and reproducibility instructions for the data analysis pipeline used in this thesis.

---

## Overview

The thesis uses three generations of analysis scripts, progressively refined. The canonical (latest) pipeline is in `analytics_new/`.

---

## Latest Analysis Pipeline (`analytics_new/`)

### Script Sequence

| Step | Script | Purpose |
|------|--------|---------|
| 1 | `01_prepare_cohorts.py` | Load raw dataset, apply eligibility filters, construct loose/strict samples, define cohorts |
| 2 | `02_ecosystem_analysis.py` | Governance distribution, ownership structure, decentralisation scoring |
| 3 | `03_dapp_level_analysis.py` | Market structure (concentration, Gini), sector performance, chain deployment |
| 4 | `04_thesis_report.py` | Generate all thesis output documents (methodology, results, insights, anomalies, brief) |

### Shared Libraries (`analytics_new/lib/`)
Reusable modules for data loading, statistical utilities, and output formatting.

### Configuration (`analytics_new/config.py`)
Paths, constants, ENUM definitions, and sampling parameters.

---

## Merged Analysis Pipeline (`analytics_merged/`)

### Script Sequence

| Step | Script | Purpose |
|------|--------|---------|
| 1 | `01_prepare.py` | Data loading and preprocessing |
| 2 | `02_governance.py` | Governance and decentralisation analysis |
| 3 | `03_market.py` | Market structure analysis |
| 4 | `04_chains.py` | Blockchain deployment analysis |
| 5 | `05_performance.py` | Sector performance metrics |
| 6 | `06_concept_synthesis.py` | Cross-variable synthesis and clustering |
| 7 | `07_thesis_docs.py` | Generate output documents |

---

## Original Analysis Pipeline (`analytics/`)

A 13-script pipeline covering data preparation through ecosystem overview:

| Step | Script | Focus |
|------|--------|-------|
| 01 | `01_data_preparation.py` | Raw data ingestion |
| 02 | `02_governance_analysis.py` | Governance coding |
| 03 | `03_ecosystem_analysis.py` | Ecosystem overview |
| 04 | `04_market_analysis.py` | Market metrics |
| 05 | `05_adoption_analysis.py` | Adoption patterns |
| 06 | `06_performance_analysis.py` | Performance benchmarks |
| 07 | `07_funding_analysis.py` | Funding structure |
| 08 | `08_category_comparison.py` | Cross-category comparison |
| 09 | `09_key_insights.py` | Key insight extraction |
| 10 | `10_token_type_analysis.py` | Token type analysis |
| 11 | `11_sector_deep_dive.py` | Sector deep dive |
| 12 | `12_anomaly_analysis.py` | Anomaly detection |
| 13 | `13_ecosystem_overview.py` | Full ecosystem summary |

---

## Reproducibility Instructions

### Environment Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Key libraries used:
# pandas, numpy, scipy, scikit-learn, matplotlib, seaborn, openpyxl
```

### Running the Latest Pipeline

```bash
cd analytics_new/

# Step 1: Prepare cohorts
python 01_prepare_cohorts.py

# Step 2: Ecosystem analysis
python 02_ecosystem_analysis.py

# Step 3: DApp-level analysis
python 03_dapp_level_analysis.py

# Step 4: Generate thesis report
python 04_thesis_report.py
```

### Source Data

Primary input: `DAPP_Dataset_Nov_2025 - Final.csv` (repo root)  
This CSV is the canonical source for all pipeline scripts.

---

## Output Files

All analysis outputs are generated in `analytics_new/outputs/`:

- `METHODOLOGY.md` — Analysis methodology documentation
- `RESULTS_AND_DISCUSSION.md` — Full results narrative
- `KEY_INSIGHTS.md` — Summary of key research insights
- `ANOMALIES.md` — Detected anomalies and notable patterns
- `THESIS_BRIEF.md` — Condensed thesis brief

All figure files (`.png`) are generated in the `outputs/` directory and referenced in the thesis chapters.

---

## Key Methodological Choices

| Choice | Rationale |
|--------|-----------|
| K-means clustering (k=3) | Identifies primary, secondary, and tertiary DApp cohorts without prior cluster definition |
| PCA for dimensionality reduction | Reduces 48 variables to meaningful composite dimensions for visualisation |
| Gini coefficient | Standard measure of concentration; comparable to income inequality literature |
| Composite governance score | Aggregates governance_type, ownership_status, and decentralisation_level into a 0–1 scale |
| Loose/strict sample split | Preserves full-universe statistics while enabling deeper analysis on complete-data subset |
