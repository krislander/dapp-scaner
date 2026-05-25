---
title: Merged Analysis — Key Insights
---

# Key insights (ecosystem and market level)

Conceptual statements derived from the strict eligible universe. See `conceptual_insights.csv` for structured fields.

## INS-GOV-01 — Decentralisation label mix in the high-signal subset
*governance*
Among DApps passing strict activity thresholds, the distribution of decentralisation labels shows how far the sample is from fully on-chain, community-controlled ideals.
- **Metric:** `pct_level_DECENTRALIZED` = `13.24`
- **Figure:** `figures/02_governance_distribution_strict.png`

## INS-GOV-02 — Team-operated governance remains common at scale
*governance*
Even when restricting to well-measured DApps, team-controlled governance types account for a large share—relevant for thesis arguments on progressive decentralisation.
- **Metric:** `pct_governance_TEAM_CONTROLLED` = `26.47`
- **Figure:** `figures/02_governance_distribution_strict.png`

## INS-MKT-01 — Capital concentration in the strict universe
*market*
Token market capitalisation remains heavily concentrated among a small head when only DApps with rich metrics are analysed—consistent with winner-takes-most dynamics in attention and liquidity.
- **Metric:** `top10_share_of_mcap_pct` = `80.46`
- **Figure:** `figures/03_market_dynamics_strict.png`

## INS-ADP-01 — User attention concentration
*adoption*
Active wallets aggregate on a small set of destinations; the tail is long but thin once minimum-user filters apply.
- **Metric:** `top10_share_of_users_pct` = `90.14`
- **Figure:** `figures/03_market_dynamics_strict.png`

## INS-ADP-02 — Multichain deployment rate
*adoption*
Share of strict-eligible DApps that list more than one chain; indicates ecosystem-level expansion vs chain-specialisation strategies.
- **Metric:** `pct_multichain` = `70.59`
- **Figure:** `figures/04_chain_top15_strict.png`

## INS-ECO-is_defi — DeFi-tagged slice (category/sector heuristic)
*ecosystem*
Theme flags from analytics/01-style heuristics show how much of the strict sample and its user base each vertical absorbs.
- **Metric:** `pct_of_strict_dapps|pct_of_strict_users` = `57.35% | 54.33%`
- **Figure:** `figures/05_performance_strict.png`

## INS-ECO-is_gaming — Gaming-tagged slice
*ecosystem*
Theme flags from analytics/01-style heuristics show how much of the strict sample and its user base each vertical absorbs.
- **Metric:** `pct_of_strict_dapps|pct_of_strict_users` = `26.47% | 34.54%`
- **Figure:** `figures/05_performance_strict.png`

## INS-ECO-is_social — Social-tagged slice
*ecosystem*
Theme flags from analytics/01-style heuristics show how much of the strict sample and its user base each vertical absorbs.
- **Metric:** `pct_of_strict_dapps|pct_of_strict_users` = `4.41% | 0.7%`
- **Figure:** `figures/05_performance_strict.png`

## INS-TOK-01 — Governance-labelled tokens in the strict cohort
*token*
Prevalence of governance-type tokens among DApps that already pass engagement filters informs how often tokens are framed as voting assets vs pure utility.
- **Metric:** `pct_is_governance_token` = `26.47`
- **Figure:** `figures/02_governance_token_heatmap_strict.png`
