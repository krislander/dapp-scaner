# analytics_merged

Combines **analytics_new** methodology (strict gates, cohort manifest, ranked slices) with **analytics/** empirical derived features and chart styles (governance, market, chains, performance).

## Run order (from repo root)

```bash
python3 analytics_merged/01_prepare.py
python3 analytics_merged/02_governance.py
python3 analytics_merged/03_market.py
python3 analytics_merged/04_chains.py
python3 analytics_merged/05_performance.py
python3 analytics_merged/06_concept_synthesis.py
python3 analytics_merged/07_thesis_docs.py
```

## Outputs

- `outputs/prepared_merged.csv` — full table with `eligible_loose`, `analysis_eligible`, cohort flags, derived columns
- `outputs/cohort_manifest.json`
- `outputs/backtest_headline_metrics.csv` — loose vs strict vs cohort headline statistics
- `outputs/conceptual_insights.csv`, `conceptual_anomalies.csv`, `discussion_topics.csv` — **ecosystem-level** statements (no per-DApp anomaly export)
- `outputs/figures/*.png`
- `outputs/METHODOLOGY.md`, `KEY_INSIGHTS.md`, `ANOMALIES.md`, `RESULTS_AND_DISCUSSION.md`, `THESIS_BRIEF.md`

Tune strict sample size in `analytics_merged/config.py` (`MIN_USERS_STRICT`, `MIN_ACTIVITY_SIGNALS_STRICT`, `REQUIRE_MARKET_OR_TVL`).
