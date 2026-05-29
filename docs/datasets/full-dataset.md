---
title: Full DApp Dataset
---

# Full DApp Dataset

The complete research dataset of **855 decentralised applications** collected for the MSc thesis *Decentralised Applications in Focus: Governance, Market Structure, and Adoption Patterns* (Politecnico di Milano, 2024–2025).

Data snapshot: **November 2025**. Sources: DappRadar, DeFiLlama, CoinMarketCap, CoinGecko, and manual coding.

> **How to use this table:** Search by name, sector, category, token symbol, or chain. Use the dropdowns to filter by sector, governance type, or decentralisation level. Click any column header to sort. Toggle columns at the bottom to customise the view. The table is paginated — 50 rows per page.

---

<DataTable />

---

## Column Reference

| Column | Description |
|--------|-------------|
| `name` | DApp name |
| `dapp_sector` | Broad sector (exchanges, defi, games, social, infrastructure, nft, other) |
| `dapp_category` | Primary functional category (DEX, Lending, NFT Marketplace, …) |
| `sub_category` | More granular sub-type labels |
| `is_active` | Whether the DApp was active at snapshot date |
| `is_multi_chain` | Deployed on more than one blockchain |
| `governance_type` | Coded governance model (ONCHAIN\_TOKEN\_GOVERNANCE, DAO\_WITH\_TIMELOCK, TEAM\_CONTROLLED, HYBRID, etc.) |
| `ownership_status` | Entity controlling the protocol (DAO\_OWNED, COMPANY\_OWNED, FOUNDATION\_OWNED, MIXED) |
| `level_of_decentralisation` | Three-level summary: DECENTRALIZED / SEMI\_DECENTRALIZED / CENTRALIZED |
| `token_symbol` | Native token ticker |
| `token_type` | GOVERNANCE, UTILITY, or blank |
| `website` | Official website |
| `chains` | Blockchain(s) the DApp is deployed on |
| `tvl` | Total Value Locked (USD) at snapshot |
| `market_cap` | Market capitalisation (USD) |
| `users` | 30-day unique active wallets |
| `volume` | 30-day trading volume (USD) |
| `transactions` | 30-day transaction count |
| `price` | Token price (USD) |
| `raised_capital` | Known fundraising amount (USD, partial coverage) |
| `percent_change_*` | Price change over 1h / 24h / 7d / 30d / 60d / 90d windows |

> Full variable definitions and coding rules: [Appendix A — Variable Codebook](/appendices/variable-codebook)

---

## Download

The raw dataset files used in this research are available in the project repository:

- **CSV** — `DAPP_Dataset_Nov_2025 - Final.csv` (root of the repository)
- **Excel (enriched)** — `DAPP_Dataset_Nov_2025 - Final_ENRICHED_v2coded.xlsx`
- **Thesis output folder** — `the-thesis-output/Datasets/Final datasets/`
