# Methodology

## 1. Data source and scope
- **Source file:** `DAPP_Dataset_Nov_2025 - Final.csv`
- **Rows:** 855 DApps after load.
- **Analysis-eligible rows:** 834 (see eligibility rules below).
- **Units (financial):** `tvl`, `market_cap`, `volume`, `users`, `transactions` are used as provided in the CSV. `total_liquidity_usd` is documented as **millions USD** in the project brief; the pipeline adds `liquidity_usd = total_liquidity_usd × 10⁶` in preparation for like-for-like comparisons.
- **Multi-label `sub_category`:** comma-separated. **Primary sub-tag** for secondary cohorts is the **first** segment after splitting on commas (documented sensitivity: ordering may affect small slices).

## 2. Eligibility (“sufficient data”)
- **Governance completeness:** non-missing `governance_type`, `ownership_status`, `level_of_decentralisation`.
- **Activity signal:** at least **two** of `{users, volume, transactions, tvl, market_cap}` must be present and **> 0**.
- **Derived fields:** `data_completeness_score` ∈ [0,1] (50% weight on governance completeness, 50% on share of activity metrics populated).

## 3. Cohort construction (noise reduction)
- **Primary slices:** `(dapp_sector, dapp_category)`. **Secondary slices:** `(dapp_sector, dapp_category, primary_sub_tag)`.
- Within each slice, eligible DApps are ranked by a **signal score** = weighted sum of `log1p(metric)` for users, volume, TVL, market cap, transactions (weights in `analytics_new/config.py`).
- **Selection:** if eligible count ≥ 20, take the top **min(50, n_eligible)**; if eligible count < 20, take **all** eligible in that slice. Manifest records `cohort_size_note` per slice.

## 4. Ecosystem vs DApp level
- **Ecosystem:** primary grouping is `dapp_sector` (e.g. defi, exchanges, games). Cross-sector similarity (e.g. DEX under `exchanges` vs `defi`) is discussed as a **labelling limitation**, not merged silently.
- **DApp level:** robust modified z-scores (median / MAD) within each sector for `volume_per_user`, `tx_per_user`, `tvl_to_mcap` (requires `users ≥ 1000` for ratio stability). Flags combine high robust-z and top within-sector percentile (see `analytics_new/config.py`).

## 5. Theme and “strange result” rules
Themes (prediction markets, AI, DePIN/RWA) use documented keyword/category rules in `analytics_new/lib/themes.py`. Hypothesis-style flags (e.g. centralized label but very high users) are precomputed in `01_prepare_cohorts.py`.

## 6. Reproducibility
```bash
python analytics_new/01_prepare_cohorts.py
python analytics_new/02_ecosystem_analysis.py
python analytics_new/03_dapp_level_analysis.py
python analytics_new/04_thesis_report.py
```

## 7. Limitations
- Single cross-sectional snapshot; no time series causality.
- Mixed provenance of metrics (see repository `DATABASE_COLUMNS.md`).
- Keyword themes (AI, DePIN) incur false positives/negatives; rule text is versioned in code for audit.
