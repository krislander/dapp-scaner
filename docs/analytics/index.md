---
title: Analytics Overview
---

# Analytics Overview

This section documents all data analysis pipelines used in the thesis. Three generations of analysis were conducted, each refining the methodology and dataset.

---

## Analysis Pipelines

### Original Analysis (`analytics/`)
The first generation of analysis scripts. Produced summary statistics, completion reports, and initial presentation materials.

- [Analysis Summary](/analytics/original/summary)
- [Completion Report](/analytics/original/completion)
- [Presentation](/analytics/original/presentation)

**Scripts:** 13 Python scripts (`01_data_preparation.py` through `13_ecosystem_overview.py`)

---

### Merged Analysis (`analytics_merged/`)
Second-generation analysis incorporating merged datasets. Produced structured thesis documents with methodology, results, insights, and anomalies sections.

- [Overview](/analytics/merged/)
- [Methodology](/analytics/merged/methodology)
- [Results & Discussion](/analytics/merged/results)
- [Key Insights](/analytics/merged/insights)
- [Anomalies](/analytics/merged/anomalies)
- [Thesis Brief](/analytics/merged/brief)

**Scripts:** 7 Python scripts (`01_prepare.py` through `07_thesis_docs.py`) + lib modules

---

### Latest Analysis (`analytics_new/`)
Most current analysis pipeline, incorporating cohort-based analysis and refined metrics. This is the canonical analysis referenced in the thesis.

- [Overview](/analytics/latest/)
- [Methodology](/analytics/latest/methodology)
- [Results & Discussion](/analytics/latest/results)
- [Key Insights](/analytics/latest/insights)
- [Anomalies](/analytics/latest/anomalies)
- [Thesis Brief](/analytics/latest/brief)

**Scripts:** 4 Python scripts (`01_prepare_cohorts.py` through `04_thesis_report.py`) + lib modules

---

## Data Pipeline Overview

```
Raw Data Sources
├── DappRadar API (top-500 UAW rankings)
├── DeFiLlama API (TVL data)
├── CoinMarketCap API (market cap, token data)
└── CoinGecko API (price history, social metrics)
        ↓
Dataset Construction (855 DApps, 48 variables)
        ↓
Sample Construction
├── Loose sample (N=834) — eligibility-filtered
└── Strict sample (N=68) — full data coverage
        ↓
Analytics Pipeline
├── Governance analysis (K-means, scoring)
├── Market structure analysis (concentration, Gini)
├── Chain deployment analysis
├── Sector performance analysis
└── Cohort analysis (PCA + K-means)
        ↓
Thesis Outputs
```
