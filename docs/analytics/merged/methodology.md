---
title: Merged Analysis — Methodology
---

# Methodology (analytics_merged)

## Purpose
Merge **analytics_new** cohort discipline (ranked slices, manifest) with **analytics/** empirical feature engineering and chart idioms, evaluated on `DAPP_Dataset_Nov_2025 - Final.csv`.
Translation: I saw that my dataset had too much noise and data was not clean enough (simply some DAPPs did not have enough data to provide or were not scaled enough as products/solutions). This called for a new strategy. Do one iteration of analysis on the whole dataset, then create a "loose" dataset, do analysis again, then create a "strict" dataset and do analysis again. Extract insights, anomalies, limitations and more.

## Eligibility
- **Loose universe** (`eligible_loose`): governance fields complete + ≥2 positive activity signals — mirrors analytics_new for **backtest** comparison.
- **Strict universe** (`analysis_eligible`): loose rules **plus** ≥4 signals, users ≥ 10,000, and `market_cap>0` OR `tvl>0`.
- Derived columns follow `analytics/01_data_preparation.py` (governance_score, theme flags, efficiency ratios).

## Cohorts
Primary/secondary cohorts rank strict-eligible DApps per slice by weighted log signal; manifest in `cohort_manifest.json`.

## Outputs philosophy
- **Insights and anomalies** are stored as **conceptual rows** (patterns, prevalence, interpretation) — not DApp-level anomaly lists.

## Backtest vs legacy approach
The loose row approximates the older analytics pipeline universe; the strict row shows how headlines change under tighter measurement gates.

### Headline comparison
| n | pct_decentralized | pct_team_controlled_gov | pct_company_owned | top10_mcap_share_pct | pct_multichain | median_governance_score | universe |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 834 | 4.68 | 62.71 | 82.97 | 57.54 | 36.21 | 0.0667 | loose_universe_analytics_new_style |
| 68 | 13.24 | 26.47 | 52.94 | 80.46 | 70.59 | 0.2833 | strict_high_signal |
| 68 | 13.24 | 26.47 | 52.94 | 80.46 | 70.59 | 0.2833 | primary_cohort_topK |

## Reproducibility
```bash
python3 analytics_merged/01_prepare.py
python3 analytics_merged/02_governance.py
python3 analytics_merged/03_market.py
python3 analytics_merged/04_chains.py
python3 analytics_merged/05_performance.py
python3 analytics_merged/06_concept_synthesis.py
python3 analytics_merged/07_thesis_docs.py
```

**Source:** `DAPP_Dataset_Nov_2025 - Final.csv` — **rows:** 855 — **strict N:** 68 — **loose N:** 834.
