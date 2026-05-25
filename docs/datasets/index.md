---
title: Dataset Inventory
---

# Dataset Inventory

This page documents all datasets used in the MSc thesis research on decentralised applications.

---

## Primary Research Dataset

### DAPP_Dataset_Nov_2025 — Final (ENRICHED)
**File:** `the-thesis-output/DAPP_Dataset_Nov_2025 - Final_ENRICHED.xlsx`  
**Format:** Excel (.xlsx)  
**Records:** 855 DApps  
**Variables:** 48 columns  
**Snapshot date:** November 2025  

The primary dataset used for all thesis analyses. Contains manually coded governance and ownership variables combined with automatically collected market, adoption, and technical metrics.

**Data sources integrated:**
- DappRadar API — UAW rankings, category, chain deployment
- DeFiLlama API — Total Value Locked (TVL)
- CoinMarketCap API — market capitalisation, trading volume, token data
- CoinGecko API — price history, social media follower counts, developer activity

---

## Empirical Analysis Datasets

### Analysis Iteration Dataset
**File:** `the-thesis-output/Datasets/Empirical analysis/Analysis Iteration.xlsx`  
**Format:** Excel (.xlsx)  
**Purpose:** Intermediate analysis iteration file with computed metrics and derived variables during the empirical analysis phase.

### DAPP_Dataset_Nov_2025 (Original)
**File:** `the-thesis-output/Datasets/Empirical analysis/DAPP_Dataset_Nov_2025.xlsx`  
**Format:** Excel (.xlsx)  
**Purpose:** Original raw dataset before enrichment and final cleaning.

---

## Final Datasets

**Location:** `the-thesis-output/Datasets/Final datasets/`  
*(See the `Final datasets/` folder for production-ready data files used in the thesis analyses.)*

---

## Root-Level Dataset

### DAPP_Dataset_Nov_2025 — Final (CSV)
**File:** `DAPP_Dataset_Nov_2025 - Final.csv`  
**Format:** CSV  
**Records:** 855 rows  
**Purpose:** Flat CSV export of the final dataset for script processing and version control.

---

## Sample Definitions

| Sample | N | Definition |
|--------|---|------------|
| Full universe | 855 | All DApps in the dataset |
| Loose sample | 834 | Eligibility-filtered: active, non-CEX, non-infrastructure DApps |
| Strict sample | 68 | Full data coverage: loose sample with complete market cap, TVL, and governance data |

---

## Variable Overview

The dataset contains **48 variables** covering:

| Category | Variables |
|----------|-----------|
| Identification | `dapp_name`, `dapp_url`, `category`, `chain`, `chain_count` |
| Governance | `governance_type`, `ownership_status`, `level_of_decentralisation`, `governance_score` |
| Token | `has_token`, `token_type`, `token_symbol` |
| Market | `market_cap_usd`, `volume_24h_usd`, `price_usd`, `fdv_usd` |
| Adoption | `uaw_30d`, `transactions_30d`, `tvl_usd` |
| Social | `twitter_followers`, `github_commits_4w`, `coingecko_score` |
| Structural | `founding_year`, `funding_type`, `admin_key_risk`, `is_multichain` |
| Derived | `governance_score`, `adoption_score`, `concentration_score` |

> See [Appendix A: Variable Codebook](/appendices/variable-codebook) for full definitions and coding rules.
