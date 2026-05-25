---
title: Latest Analysis Overview
---

# analytics_new

Thesis-oriented pipeline (isolated from `analytics/`). Run from repository root:

```bash
python3 analytics_new/01_prepare_cohorts.py
python3 analytics_new/02_ecosystem_analysis.py
python3 analytics_new/03_dapp_level_analysis.py
python3 analytics_new/04_thesis_report.py
```

Outputs: `analytics_new/outputs/` (CSV, JSON, figures, Markdown reports). Configuration: `analytics_new/config.py`.
