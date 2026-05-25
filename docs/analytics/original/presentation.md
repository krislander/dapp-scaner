---
title: Presentation
---

# DApp Ecosystem Analysis — Pitch Presentation

---

## Slide 1: Title

**Governance, Tokenomics & Decentralisation in the DApp Ecosystem**
An empirical analysis of 855 decentralised applications

*February 2026*

---

## Slide 2: Research Goals

**Core question:** How decentralised are "decentralised" applications, really?

**This analysis aims to:**

- Map the governance, ownership, and tokenomics landscape of the DApp ecosystem
- Identify whether token design choices reflect actual decentralisation
- Compare sectors (DeFi, Gaming, AI, Prediction Markets, RWA) on governance maturity
- Surface anomalies and contradictions that challenge the sector's self-narrative

---

## Slide 3: Methodology

**Data collection** — Web scraping + manual enrichment across DApp aggregators and on-chain sources

**Variables enriched manually** for all 855 DApps:

- `ownership_status` — who controls the project (Company, DAO, Foundation, Mixed)
- `level_of_decentralisation` — Centralised / Semi / Decentralised
- `governance_type` — from Team-Controlled to DAO-with-Timelock (7 levels)
- `token_type` — Utility, Governance, Reward, Speculative

**Analysis pipeline** — 13 Python scripts producing 45+ visualisations, statistical clustering, cross-tabulations, and anomaly detection

---

## Slide 4: The Dataset

| Metric | Value |
|---|---|
| DApps analysed | 855 |
| Categories | 20 |
| Blockchains | 77 |
| Total Users | 90.9M |
| Total Market Cap | $14.9B |
| Total TVL | $115.7B |
| DApps with tokens | 49% |

**Key variables:** governance_type, ownership_status, level_of_decentralisation, token_type (NEW), market_cap, TVL, users, volume, chains

> Visual: `13_ecosystem_at_a_glance.png`

---

## Slide 5: The Decentralisation Paradox

- **Only 4.6%** of DApps are truly decentralised
- **56.8%** remain centralised, **38.6%** semi-decentralised
- **83.3%** are company-owned
- **63.5%** use team-controlled governance

Despite being built on decentralised infrastructure, the vast majority of DApps retain traditional corporate control.

> Visual: `13_governance_maturity.png`

---

## Slide 6: Token Type Economy

| Token Type | Count | Share |
|---|---|---|
| Utility | 202 | 48.2% |
| Reward | 108 | 25.8% |
| Governance | 78 | 18.6% |
| Speculative | 27 | 6.4% |
| Social | 2 | 0.5% |

- Governance tokens → median MCap **$22.4M** (3.2× higher than Utility)
- Yet only **36.6%** of governance-token DApps are actually decentralised
- Token type strongly predicts governance model adoption — DApps that issue governance tokens are far more likely to adopt on-chain or DAO-based governance, while utility/reward tokens cluster around team-controlled models
  - e.g. **Morpho**, **ENS**, **Aerodrome** (governance tokens → on-chain/DAO governance, decentralised)
  - e.g. **Pump.fun**, **SoSoValue**, **aixbt** (utility tokens → team-controlled, centralised)

> Visual: `10_token_type_distribution.png`, `10_token_type_governance.png`

---

## Slide 7: Market Concentration

- Top 10 DApps control **57.5%** of total market cap
- Top 10 DApps control **93.1%** of total TVL
- Power-law distribution — winner-takes-all dynamics
- Mirrors traditional tech monopolies despite decentralised infrastructure

Market Cap Distribution (Log Scale)
A histogram of all DApps by market cap. The vast majority cluster between $10K–$10M, with very few reaching the billions. The distribution is extremely right-skewed — most DApps are small.

Lorenz Curve
Measures inequality of market cap distribution. The huge red area between the curve and the diagonal ("Perfect Equality" line) shows severe concentration — similar to wealth inequality in traditional economies. Roughly 80% of DApps account for less than 20% of total market cap.

Top 10 DApps by Market Cap
Pump.fun (~$1.9B) and Ethena (~$1.8B) massively lead the pack. After that it drops sharply — Morpho, ENS, Aerodrome are in the $600–800M range. By the time you reach Compound (#10), it's around $400M. This visualises the winner-takes-all dynamic.

Power Law Distribution
Plots rank vs market cap on log-log scale. The dashed red line is a power law fit with exponent α=0.61. The data points follow this fit reasonably well, confirming that market cap follows a power law — a small number of DApps capture disproportionate value, which is a structural feature of the ecosystem, not an anomaly.
The key takeaway: the DApp economy mirrors traditional tech monopolies. Despite decentralised infrastructure, value concentrates at the top just as heavily as in Web2.

> Visual: `04_market_cap_distribution.png`

---

## Slide 8: Sector Deep Dives

| Sector | DApps | Token Rate | Decentralised | Avg Gov Score |
|---|---|---|---|---|
| DeFi | 268 | 60% | 9.0% | 0.30 |
| Gaming | 209 | 46% | 1.9% | 0.14 |
| AI | 59 | 80% | 0.0% | 0.22 |
| RWA | 43 | 44% | 2.3% | 0.17 |
| Prediction Mkt | 32 | 25% | 0.0% | 0.13 |
| Social | 108 | 56% | 2.8% | 0.22 |

- DeFi dominates TVL; Gaming dominates user counts
- AI sector: highest token adoption, zero true decentralisation
- Prediction Markets: smallest, lowest token/governance adoption

> Visual: `11_cross_sector_comparison.png`

---

## Slide 9: The Engagement Dichotomy

**Gaming:** 23.8M users, $28M volume
**DeFi/DEX:** 36.8M users, $497.7B volume

- Gaming = mass adoption, low economic value per user
- DeFi = fewer users, **17,775×** more volume
- "Success" must be measured differently per sector

A DApp with 10M users and $5M volume (typical in Gaming) looks like a failure by DeFi standards, where a DApp with 10K users and $5B volume is normal. Evaluating DApps requires sector-specific benchmarks — user count for Gaming, TVL and volume-per-user for DeFi, token adoption for AI. A single universal "success metric" does not exist in this ecosystem.

> Visual: `05_category_engagement.png`

---

## Slide 10: Anomalies & Contradictions

Findings that challenge sector narratives:

- **57 unfunded DApps** outperform the funded median market cap
  - Pump.fun ($1.9B), Ethena ($1.8B), Morpho ($797M) — all unfunded
- **Extreme TVL leverage:** Maple (8,120× MCap), EigenLayer (45×)
- **Governance paradoxes:** DApps with governance tokens but team-controlled
- **185 DApps** have high users but zero TVL (non-financial utility)

> Visual: `12_anomaly_dashboard.png`

---

## Slide 11: Key Takeaways

1. **Decentralisation is the exception**, not the rule (4.6%)
2. **Token type matters** — governance tokens correlate with higher valuations but not with actual decentralisation
3. **Extreme concentration** — top 10 DApps dominate market cap and TVL
4. **Sectors diverge** — DeFi, Gaming, AI each follow different governance and tokenomic patterns
5. **Funding ≠ success** — median funded ROI is 0.11×; unfunded DApps often outperform

---

## Slide 12: Questions & Next Steps

**Open questions for discussion:**

- How should "decentralisation" be measured and validated?
- Does token type drive governance, or does governance drive token design?
- What explains the success of unfunded DApps?

**Next steps:**

- Full thesis structure and chapter outline
- Time-series analysis (dataset evolution over time)
- Deeper statistical modelling of governance–performance link

---

*Supporting materials: 45 visualisations, 4 text reports, 2 interactive HTML charts*
*Full analysis pipeline: scripts 01–13 in `/analytics/`*

Do the opposite of Token Type economy as an approach

TVL is relevant for DeFi

User metrics vs TVL vs MC

Formalize for discussion: Why is DeFi important and why is it the most centralized

Time-series could be interesting. Link to the governance side of the story. Expect to see governance being more centralized at the begininng of the app. Developers want to steer the control. If the apps on the later stage of the evolution try to implement decentralization immediately.

COmpare if decentralisation is most important for a project or is it its go-to market strategy

Be careful when you say words like "predict", "correlated to". Use "suggests" or "needs to be further analysed"

Level of abstraction is good. An all overview of the market, don't focus on individual analysis of DAPPs unless they are special cases

About the scraping, stress in the methodology to make sure the data is relevant and consistent

Table of contents

write that i will be ready for June



