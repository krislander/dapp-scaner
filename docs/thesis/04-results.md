---
title: "Chapter 4: Results"
---

# Chapter 4 — Results

## 4.1 Descriptive Statistics of the Full Dataset

The full dataset comprises 855 decentralised applications (DApps) deployed across 77 distinct blockchain networks, collected in November 2025. Together, these applications report 90.9 million total active users, a combined token market capitalisation of approximately $14.9 billion, and Total Value Locked (TVL) of $115.7 billion. The dataset captures 48 variables per DApp (see Appendix A — *forward reference: variable codebook*), of which 33 contain at least partial coverage across the full sample; the remaining variables are financial or governance fields for which sparse or no data were available for a significant share of the population.

### 4.1.1 Dataset Coverage and Completeness

Coverage varies substantially by variable category. Token market data — market capitalisation, price, volume, and supply fields sourced from CoinMarketCap and CoinGecko — are available for the 50.2 per cent of DApps that operate a native token. The remaining 49.8 per cent either have no token or lacked a match in the token-data APIs at the time of collection. TVL, sourced from DeFiLlama, covers protocol-level locked value and is non-zero for approximately 38 per cent of the dataset; this figure reflects the subset of DApps with measurable on-chain liquidity pools rather than all DApps in the sample. Activity metrics — users, transactions, and volume — sourced from DappRadar are present for the full 855-DApp population but exhibit extreme right skew: the mean user count is pulled far above the median by a small number of very large protocols.

Governance fields (`governance_type`, `ownership_status`, `level_of_decentralisation`) were coded manually for all 855 entries following the decision rules described in §3.6 (*forward reference: governance coding rules*). Of these, 834 records received complete, non-UNKNOWN coding — the remaining 21 entries had insufficient publicly available information to assign definitive labels and were excluded from all subsequent analyses.

### 4.1.2 Loose versus Strict Universe Comparison

Table 4.1 presents the headline metrics comparison between the full loose universe (N=834) and the strict high-signal sample (N=68), as derived from `backtest_headline_metrics.csv`. The transition from loose to strict eligibility does not simply retain the "top" DApps in a linear sense; rather, it selects the subset for which the analyst has high confidence in the accuracy and completeness of *all* major metric categories simultaneously. The result is a meaningful shift in several headline indicators.

**Table 4.1 — Headline metrics comparison: loose universe versus strict high-signal sample**

| Metric | Loose universe (N=834) | Strict sample (N=68) |
|--------|:---------------------:|:--------------------:|
| % Fully decentralised | 4.68% | 13.24% |
| % Team-controlled governance | 62.71% | 26.47% |
| % Company-owned | 82.97% | 52.94% |
| Top-10 market cap share | 57.54% | 80.46% |
| % Multichain | 36.21% | 70.59% |
| Median governance score | 0.067 | 0.283 |

*Source: `backtest_headline_metrics.csv`*

Several contrasts in Table 4.1 are analytically significant. The proportion of fully decentralised DApps more than doubles from 4.7 per cent to 13.2 per cent when moving from the loose to the strict universe, suggesting that DApps with measurable, large-scale activity are somewhat more decentralised than the broader population — though the absolute proportion remains low. The share of company-owned DApps drops from 83.0 per cent to 52.9 per cent, while team-controlled governance falls from 62.7 per cent to 26.5 per cent. This shift likely reflects the composition of the strict sample, which is dominated by well-established DeFi protocols that have had more time and institutional incentive to formalise governance structures.

Market concentration, paradoxically, *increases* in the strict sample: the top-10 market cap share rises from 57.5 per cent to 80.5 per cent. This inversion occurs because the strict filter retains only those protocols with non-trivial financial metrics, and those protocols are predominantly the large incumbents. The median governance score more than quadruples (0.067 to 0.283), consistent with the governance improvements just described.

**[Figure 4.1: Governance label distribution — loose universe (N=834)]**
*File: `figures/02_governance_distribution_loose_backtest.png`*

Figure 4.1 (`02_governance_distribution_loose_backtest.png`) visualises the distribution of governance labels in the loose universe. The dominant category is company-owned, followed by team-controlled, with a small tail of DAO-governed and fully decentralised protocols. Figure 4.2 (`02_governance_heatmaps_loose_backtest.png`) and Figure 4.3 (`02_governance_token_heatmap_loose_backtest.png`) present the corresponding governance × ownership and governance × token heatmaps for the loose universe, providing a visual baseline against which the strict-sample findings can be compared.

**[Figure 4.2: Governance × ownership heatmap — loose backtest universe (N=834)]**
*File: `figures/02_governance_heatmaps_loose_backtest.png`*

**[Figure 4.3: Governance × token type heatmap — loose backtest universe (N=834)]**
*File: `figures/02_governance_token_heatmap_loose_backtest.png`*

---

## 4.2 Governance and Ownership Structure

### 4.2.1 Distribution of Decentralisation Labels

Among the 68 DApps in the strict sample, the distribution of governance labels is substantially more varied than in the loose universe but remains concentrated well away from the "fully decentralised" ideal. Figure 4.4 (`02_governance_distribution_strict.png`) presents the complete breakdown.

**[Figure 4.4: Governance label distribution — strict universe (N=68)]**
*File: `figures/02_governance_distribution_strict.png`*

The data show that 13.24 per cent of the strict sample (nine DApps) are classified as fully decentralised (INS-GOV-01). A majority — 52.94 per cent (36 DApps) — are company-owned, meaning a corporate entity retains ultimate authority over the protocol's smart contracts and governance decisions. Team-controlled governance accounts for a further 26.47 per cent (18 DApps, INS-GOV-02), representing projects in which a founding team or core contributor group sets parameters informally rather than through a codified on-chain process. The remaining share occupies intermediate categories — semi-decentralised projects using snapshot-based off-chain governance, multisig-controlled protocols, and hybrids that combine multiple mechanisms.

In aggregate, 86.8 per cent of the strict sample (59 DApps) are not fully decentralised. This figure is the central empirical finding of the governance analysis: application-layer centralisation is the norm, not the exception, among DApps with sufficient scale and data quality to be included in the strict sample.

The median governance score in the strict sample is 0.283 (on a normalised 0–1 scale), substantially higher than the loose-universe median of 0.067 but still well below the maximum value that would correspond to full decentralisation across all sub-dimensions.

### 4.2.2 Ownership Concentration and Governance Type

Figure 4.5 (`02_governance_heatmaps_strict.png`) presents the two-way cross-tabulations of governance dimensions for the strict sample, illustrating the co-occurrence patterns between `governance_type`, `ownership_status`, and `level_of_decentralisation`.

**[Figure 4.5: Governance × ownership heatmap — strict sample (N=68)]**
*File: `figures/02_governance_heatmaps_strict.png`*

The heatmaps reveal systematic clustering in the governance space. Company-owned DApps are almost exclusively classified as team-controlled or founder-controlled in governance type; they rarely appear in DAO-governed or community-governed cells. Fully decentralised DApps, conversely, tend to be governed through on-chain token voting mechanisms (DAO with timelock or on-chain token governance) and lack a single company-owned identity. The off-diagonal cells — where ownership status and governance type diverge — are sparsely populated, indicating that these governance dimensions are largely co-determined rather than independent. This internal consistency supports the reliability of the manual coding procedure.

Table 4.2 presents the complete cross-tabulation of decentralisation level against governance type for the strict sample, using observed counts from `crosstab_decentralisation_governance_strict.csv`. Governance types are grouped into three analytically meaningful categories for presentation: on-chain governance (DAO with timelock and on-chain token governance), community/hybrid governance (hybrid structures, multisig with community input, and Snapshot-based off-chain governance), and team-controlled (no formal governance and team-controlled types).

**Table 4.2 — Cross-tabulation: decentralisation level × governance type, strict sample (N=68)**

| Decentralisation level | On-chain governance | Community / hybrid governance | Team-controlled | Total |
|----------------------|:-------------------:|:-----------------------------:|:---------------:|:-----:|
| DECENTRALIZED | 8 | 1 | 0 | **9** |
| SEMI\_DECENTRALIZED | 4 | 35 | 14 | **53** |
| CENTRALIZED | 1 | 0 | 5 | **6** |
| **Total** | **13** | **36** | **19** | **68** |

*Source: `crosstab_decentralisation_governance_strict.csv`. On-chain governance = DAO\_WITH\_TIMELOCK (n=1) + ONCHAIN\_TOKEN\_GOVERNANCE (n=12). Community/hybrid = HYBRID (n=2) + MULTISIG\_WITH\_COMMUNITY\_INPUT (n=4) + SNAPSHOT\_OFFCHAIN (n=30). Team-controlled = NONE (n=1) + TEAM\_CONTROLLED (n=18).*

The cross-tabulation confirms that all nine fully decentralised DApps are governed through on-chain mechanisms (eight) or hybrid community processes (one); none are team-controlled. Conversely, of the six centralised DApps, five are team-controlled and only one uses any on-chain governance mechanism — an incongruity likely reflecting a DApp that has deployed a governance token while operational authority remains concentrated. The SEMI\_DECENTRALIZED category (53 DApps, 77.9% of the strict sample) spans all three governance groups, with the plurality (35) using community or hybrid processes dominated by Snapshot off-chain voting (30 DApps within this row).

### 4.2.3 Token Type and Governance Co-Structure

Figure 4.6 (`02_governance_token_heatmap_strict.png`) extends the governance picture to include token classification, producing a view of how token design aligns with governance structure in the strict sample.

**[Figure 4.6: Governance type × token type heatmap — strict sample (N=68)]**
*File: `figures/02_governance_token_heatmap_strict.png`*

The heatmap reveals that on-chain token governance mechanisms are almost exclusively associated with governance-type tokens: all 12 DApps with ONCHAIN\_TOKEN\_GOVERNANCE governance type hold governance tokens, as does the sole DAO\_WITH\_TIMELOCK DApp. Conversely, team-controlled DApps hold no governance tokens — their tokens are classified as utility (n=7), reward (n=6), or absent (n=5). This alignment between governance token design and on-chain governance mechanisms represents an internal consistency that would be expected if token design tracks governance ambition.

However, a meaningful divergence appears in the SNAPSHOT\_OFFCHAIN row (30 DApps): four hold governance tokens, seventeen hold utility tokens, seven hold reward tokens, and one holds a social token. This indicates that off-chain governance via Snapshot is not primarily associated with governance token design — many DApps in this category retain utility or reward token structures despite operating a community voting process. The token design, in these cases, reflects financial engineering rather than governance architecture.

---

## 4.3 Market Structure and Capital Concentration

### 4.3.1 Distributional Properties of Market Capitalisation

The market capitalisation distribution of DApps in the full dataset is highly right-skewed. Across the 855-DApp sample, the mean market capitalisation is $71.8 million and the median is $6.9 million — a mean-to-median ratio of approximately 10.4, diagnostic of a fat-tailed distribution. A power-law regression across the full dataset yields an estimated exponent of α ≈ 0.61, consistent with a Pareto-like scaling regime in which a small number of very large protocols account for a disproportionate share of aggregate market value.

Figure 4.7 (`03_market_dynamics_strict.png`) and Figure 4.8 (`03_market_dynamics_loose.png`) illustrate the concentration and distributional structure of the strict and loose samples respectively.

**[Figure 4.7: Market capitalisation and user concentration — strict sample (N=68)]**
*File: `figures/03_market_dynamics_strict.png`*

**[Figure 4.8: Market dynamics — loose universe comparison (N=834)]**
*File: `figures/03_market_dynamics_loose.png`*

### 4.3.2 Top-10 Concentration Ratios

In the strict sample (N=68), the ten largest DApps by market capitalisation account for 80.46 per cent of the total market cap within that universe (INS-MKT-01), based on the 63 strict-eligible DApps for which market cap data are available. User concentration is even more pronounced: the ten most-active DApps by unique active wallets attract 90.14 per cent of strict-sample users (INS-ADP-01). These ratios are substantially higher than in the loose universe, where the top-10 market cap share is 57.54 per cent, because the strict filter retains only protocols with non-trivial financial metrics, which are predominantly the large incumbents.

TVL concentration mirrors these patterns. Total TVL across the full 855-DApp dataset is $115.7 billion, with the top ten protocols controlling approximately 93.1 per cent of that amount. Median TVL per user across the strict sample is $1,942, but this average conceals enormous variance: the highest-performing protocols by capital efficiency carry TVL-per-user ratios in the hundreds of thousands of dollars (reflecting institutional liquidity provision in DeFi), while many smaller DApps report near-zero TVL per wallet.

### 4.3.3 Structural Anomalies

Two structural anomalies in the market data merit specific attention.

**TVL exceeds market capitalisation (ANO-MKT-02).** Approximately 8.8 per cent of DApps in the strict sample exhibit TVL that exceeds their token market capitalisation. This inversion — where locked capital is worth more than the protocol's own equity — can arise from several mechanisms: rapid TVL accumulation preceding token price appreciation, artificial TVL inflation from looped collateral positions, or sustained depression of token prices relative to protocol utility. The phenomenon indicates that standard market cap figures do not always capture the full economic scale of a protocol and that TVL is a necessary complement to market cap when assessing DApp significance.

**Unfunded DApps outperform funded peers (ANO-MKT-03).** Within the strict sample (N=68), approximately 13 DApps raised documented venture capital. The median return on investment (ROI) for these funded DApps — measured as current market cap divided by total capital raised — is 0.11×, meaning the median venture-backed DApp in the strict sample is currently valued at roughly one-tenth of the capital invested in it. At the same time, 29.4 per cent of the strict sample comprises unfunded DApps whose current market valuations exceed those of their venture-backed counterparts. Across the full 855-DApp dataset, the pattern is consistent: $14.3 billion in documented capital was raised by 38 DApps in total, yet total capital raised exhibits only a weak correlation with subsequent market performance. This broader finding reinforces the strict-sample anomaly and challenges the assumption that capital raised is a reliable predictor of DApp market success.

### 4.3.4 Governance–Performance Correlation

The Spearman rank correlation between the composite governance score and log-transformed market capitalisation across the strict sample is 0.38. While this association does not establish causality, it indicates that governance structure and market scale are not independent: DApps with higher governance scores tend to exhibit larger market capitalisations. DAO-governed DApps additionally show higher transaction intensity, and community governance is associated with more engaged user bases. Whether this reflects market participants rewarding governance quality, or whether financially successful DApps simply have greater resources to invest in governance formalisation, cannot be resolved from this cross-sectional dataset; the interpretive question is addressed in §5.2.

---

## 4.4 Blockchain and Multi-Chain Deployment

### 4.4.1 Chain Distribution

The full 855-DApp dataset spans 77 blockchain networks. The five leading chains by DApp deployment count are BNB Chain (270 deployments, 11.9 per cent of total), Ethereum (221, 9.7 per cent), Polygon (192, 8.4 per cent), Base (176, 7.7 per cent), and Arbitrum (142, 6.2 per cent). The remaining 72 chains collectively account for the balance, with a long tail of single-digit deployment counts.

Figure 4.9 (`04_chain_top15_strict.png`) shows the top-15 chains by DApp presence in the strict sample, and Figure 4.10 (`04_chain_top15_loose.png`) presents the equivalent view for the loose universe.

**[Figure 4.9: Top-15 blockchain deployments — strict sample (N=68)]**
*File: `figures/04_chain_top15_strict.png`*

**[Figure 4.10: Top-15 blockchain deployments — loose universe (N=834)]**
*File: `figures/04_chain_top15_loose.png`*

Chain specialisation is evident across sectors. Ethereum and its EVM-compatible Layer-2 networks (Arbitrum, Optimism, Base) dominate the DeFi segment, where composability with established liquidity protocols and Ethereum's security budget provide structural network advantages. BNB Chain hosts a large share of gaming and NFT-gaming DApps, reflecting lower transaction costs and the presence of major gaming ecosystems in the Binance ecosystem. Solana and Sei concentrate gaming and high-throughput applications where transaction latency is a binding operational constraint.

### 4.4.2 Multi-Chain Adoption Rate

One of the most striking contrasts between the loose and strict universes concerns multi-chain deployment rates. In the loose universe, 36.21 per cent of DApps deploy across more than one chain. In the strict sample, this proportion rises to 70.59 per cent (INS-ADP-02) — nearly double. The increase is not mechanically implied by the strict filter's activity requirements, which operate at the DApp level rather than the chain level; rather, it reflects the fact that the most commercially active DApps are disproportionately those that have expanded across multiple blockchain networks. Among multi-chain DApps in the full dataset, the average number of supported chains is 5.7.

Across the full 855-DApp dataset, multi-chain DApps report an average market capitalisation of $80.2 million compared with $62.1 million for single-chain equivalents — a 1.3× premium. The causal interpretation of this premium is discussed in Chapter 5 (DIS-07); the directional finding is consistent across subsamples even if the mechanism remains ambiguous.

---

## 4.5 Sector-Level Performance

### 4.5.1 Sector Composition of the Strict Sample

The strict sample of 68 DApps is dominated by DeFi-tagged applications. Based on the theme-flag analysis derived from consolidated tag heuristics, the sector composition of the strict sample is as follows (INS-ECO-is\_defi, INS-ECO-is\_gaming, INS-ECO-is\_social):

- **DeFi** (is\_defi flag): 57.35 per cent of strict DApps, accounting for 54.33 per cent of strict-sample users *(strict sample, N=68)*
- **Gaming** (is\_gaming flag): 26.47 per cent of strict DApps, accounting for 34.54 per cent of strict-sample users *(strict sample, N=68)*
- **Social** (is\_social flag): 4.41 per cent of strict DApps, accounting for 0.70 per cent of strict-sample users *(strict sample, N=68)*
- **Other / uncategorised**: residual share, predominantly NFT marketplace and infrastructure-adjacent protocols

Figure 4.11 (`05_performance_strict.png`) presents the sector-level performance metrics for the strict sample, and Figure 4.12 (`05_performance_loose.png`) provides the loose-universe comparison.

**[Figure 4.11: Sector-level performance metrics — strict sample (N=68)]**
*File: `figures/05_performance_strict.png`*

**[Figure 4.12: Sector performance — loose universe (N=834)]**
*File: `figures/05_performance_loose.png`*

### 4.5.2 The DeFi–Gaming Engagement Gap

The most economically significant sectoral contrast is the divergence between DeFi and gaming in value-per-user terms. In the strict sample (N=68), DeFi DApps process approximately $299.1 billion in total volume. Gaming DApps in the strict sample attract approximately 12,670,611 active users — the largest user base of any vertical — while generating comparatively modest financial throughput.

The implied value-per-user gap between these two sectors exceeds 1,000 times (ANO-ENG-01). This is not a marginal difference attributable to measurement error but a structural divide reflecting the distinct user populations and economic purposes of each vertical. DeFi wallets frequently represent participants deploying large capital positions in liquidity pools, yield strategies, and on-chain derivatives. Gaming wallets, by contrast, reflect engagement with in-game economies, NFT ownership, and play-to-earn mechanics — economically real but typically at the level of individual consumer transactions rather than institutional capital deployment.

The pattern is consistent across the full 855-DApp dataset (N=855). DEX-category DApps across the full dataset attract 36.8 million users and process $497.7 billion in volume, while gaming DApps across the full dataset collectively attract 23.8 million users and generate approximately $28 million in volume — a volume-per-user ratio roughly 630 times higher in the DEX category *(full dataset, N=855)*. User count and financial throughput therefore provide incompatible orderings of DApp success when applied across sector boundaries, and any league table or ranking that pools these metrics without sector disaggregation will generate misleading comparisons.

### 4.5.3 Social and NFT DApps

Social-tagged DApps represent the smallest sector in the strict sample both by count (4.41 per cent of strict DApps) and by user share (0.70 per cent of strict-sample users). This marginalisation partly reflects the strict filter's user-count threshold: many social DApps remain small by on-chain user standards, as participants frequently interact through custodial front-ends that do not generate distinct wallet events. Across the full 855-DApp dataset, NFT marketplace protocols hold a more prominent position — second in user count behind DEX (17.1 million users, full dataset) and second in market cap ($864 million, full dataset) — but their reduced presence in the strict sample reflects both the user threshold and NFT trading volume volatility, which can push activity below strict-filter thresholds during quieter market periods.

---

## 4.6 Ecosystem Deep-Dives

The preceding sections characterise the DApp landscape through cross-sectional lenses — governance structure, market concentration, chain deployment, and sector-level performance gaps. This section provides complementary depth by examining five thematically distinct ecosystems: Decentralised Finance (DeFi), Prediction Markets, AI-native DApps, Real-World Assets (RWA), and Decentralised Physical Infrastructure (DePIN). Each ecosystem is governed by a distinct economic logic, user base, and governance trajectory; treating them as a homogeneous "DApp sector" would obscure the structural differences that aggregate analyses can only partially reveal.

*Sample note.* DeFi analysis draws on the 36 DApps in the strict high-signal sample assigned `v2_ecosystem_focus = DEFI` (from the T2 v2 coding, `DAPP_Dataset_Nov_2025 - Final_ENRICHED_v2coded.xlsx`), supplemented by the 105-DApp loose-universe DeFi population where noted. Prediction Markets, AI-native DApps, RWA, and DePIN each contain fewer than 10 DApps in the strict sample (v2 distribution: PREDICTION\_MARKETS=1, AI=3, DEPIN=2; RWA is embedded within DEFI and GAMING categories); accordingly, the analysis for these four ecosystems uses the loose universe throughout and results should be interpreted in light of the correspondingly broader data-quality range.

---

### 4.6.1 Decentralised Finance (DeFi)

DeFi represents the most economically significant sector in the dataset, hosting protocols whose aggregate TVL ($112.7 billion) accounts for 97.4 per cent of all DApp TVL and whose total trading volume ($358.0 billion) constitutes 68.5 per cent of dataset-wide volume. The 105 DeFi DApps in the loose universe span DEXes (automated market makers, order-book exchanges, aggregators), lending protocols, derivatives, yield aggregators, bridge/router infrastructure, and DAO tooling. Despite subcategory diversity they share a common structural foundation: composable open-source smart contracts deployed on EVM-compatible networks, where permissionless interoperability creates pressure toward governance formalisation as protocols accumulate value.

**Chain Distribution**

Table 4.4 presents the top-10 chains by DeFi DApp deployment count in the loose universe (N=105). Chains are counted per DApp per chain deployed; multi-chain DApps appear in each chain they occupy.

**Table 4.4 — Top-10 chains by DeFi DApp presence (loose universe, N=105)**

| Chain | DeFi DApps | Share of universe |
|-------|:----------:|:-----------------:|
| Ethereum | 52 | 49.5% |
| Base | 41 | 39.0% |
| BNB Chain | 41 | 39.0% |
| Arbitrum | 40 | 38.1% |
| Polygon | 34 | 32.4% |
| Optimism | 32 | 30.5% |
| Avalanche | 26 | 24.8% |
| zkSync Era | 23 | 21.9% |
| Linea | 21 | 20.0% |
| Solana | 20 | 19.0% |

*Note: Percentages sum to more than 100% because multi-chain DApps are counted in each chain they deploy on. Source: `chains` field, loose DeFi universe.*

Ethereum's primacy reflects its role as the canonical smart-contract environment — it serves as collateral, liquidity, and trust anchor for a large share of DeFi protocols even when execution migrates to Layer-2 rollups. Solana's entry at 19.0 per cent is driven primarily by high-throughput DEX aggregators (Jupiter Exchange, 3.0 million users) and launchpad protocols (Pump.fun, 7.1 million users) whose UX requirements favour sub-second finality. The 55.2 per cent multi-chain adoption rate in the DeFi universe (compared with 36.2 per cent across all sectors) confirms that DeFi protocols migrate aggressively toward capital and user density wherever it appears. See also Figure 4.9 (`04_chain_top15_strict.png`) for the chain distribution in the strict sample.

**Key DApps**

Table 4.5 presents the top DeFi DApps by active users in the loose universe, illustrating the range of protocol types operating at scale.

**Table 4.5 — Top DeFi DApps by active users (loose universe)**

| DApp | Users | Volume | TVL | Governance | Token |
|------|------:|-------:|----:|:----------:|:-----:|
| Pump.fun | 7,076,435 | $900.1M | — | TEAM\_CONTROLLED | UTILITY |
| Jupiter Exchange | 3,044,937 | $373.7M | — | ONCHAIN\_TOKEN\_GOVERNANCE | GOVERNANCE |
| HOT Protocol | 2,080,513 | $34.2M | — | HYBRID | UTILITY |
| PancakeSwap V3 | 627,839 | $81.4B | — | SNAPSHOT\_OFFCHAIN | UTILITY |
| Jumper Exchange | 519,380 | $3.5B | — | TEAM\_CONTROLLED | — |
| 1inch Network | 363,704 | $12.8B | — | MULTISIG\_WITH\_COMMUNITY\_INPUT | UTILITY |
| Pendle | 270,925 | $6.9B | $9.6B | ONCHAIN\_TOKEN\_GOVERNANCE | GOVERNANCE |
| Aave V3 | — | — | — | ONCHAIN\_TOKEN\_GOVERNANCE | GOVERNANCE |

**Governance Maturity**

Among the 36 strict-sample DeFi DApps (v2 coding), governance is substantially more mature than the cross-ecosystem average. On-chain mechanisms (DAO\_WITH\_TIMELOCK and ONCHAIN\_TOKEN\_GOVERNANCE) account for approximately 30 per cent of strict-sample DeFi protocols, compared with 19.1 per cent across the full strict sample. Table 4.6 presents the full governance distribution across the loose DeFi universe.

**Table 4.6 — DeFi governance distribution (loose universe, N=105)**

| Governance type | Count | Share |
|-----------------|:-----:|:-----:|
| TEAM\_CONTROLLED | 40 | 38.1% |
| SNAPSHOT\_OFFCHAIN | 27 | 25.7% |
| ONCHAIN\_TOKEN\_GOVERNANCE | 14 | 13.3% |
| MULTISIG\_WITH\_COMMUNITY\_INPUT | 11 | 10.5% |
| DAO\_WITH\_TIMELOCK | 4 | 3.8% |
| HYBRID | 4 | 3.8% |
| NONE | 5 | 4.8% |
| **Total** | **105** | **100%** |

*Source: `governance_type` field, loose DeFi universe.*

The 13.3 per cent fully decentralised rate (14 DApps) is nearly three times the cross-ecosystem average of 4.7 per cent in the full loose universe and the highest of any sector. This elevated rate is consistent with DeFi protocols' competitive pressure to establish credible neutrality: a protocol modifiable at will by its team faces user flight to formally governed alternatives. The Snapshot off-chain plurality (25.7 per cent) represents an intermediate governance stage — token-holder voting is possible but execution remains operator-dependent, as documented in the governance heatmaps (Figures 4.5 and 4.6).

**Token Model Patterns**

Utility tokens dominate at 44.8 per cent, reflecting governance-adjacent but non-voting token designs used primarily for fee discounts, liquidity incentives, and staking rewards. Governance tokens appear in 19.0 per cent of DeFi DApps in the loose universe, rising to approximately 31 per cent in the strict sample, where the most financially mature protocols are concentrated. The v2 analysis (`v2_governance_token_flag`) confirms that 55 per cent of strict-sample DeFi DApps have issued a governance token. The `v2_fee_switch_or_value_accrual_to_tokenholders` field indicates that token-holder value accrual is present in approximately 44 per cent of those cases — a lower share, indicating that governance token issuance frequently precedes fee-switch activation.

**Revenue Logic**

The v2 `v2_main_revenue_generator` column identifies three dominant DeFi revenue mechanisms in the strict sample:

1. *Transaction fees* (`TX_FEE`, 20/36 strict DeFi DApps = 55.6 per cent): DEXes charge a percentage of swap volume (typically 0.01–0.30 per cent for AMMs; protocols with volume above $1 billion include Raydium, Pump.fun, PancakeSwap, 1inch, Jupiter Exchange, and SushiSwap). `v2_sustainment_model = FEES` for all TX\_FEE protocols.

2. *Interest margin* (`INTEREST_MARGIN`, 6/36 = 16.7 per cent): Lending and yield protocols (Aave V3, Morpho, Maple, Moonwell, ZeroLend, Velo) earn the spread between borrower and lender rates. `v2_sustainment_model = INTEREST_YIELD`.

3. *Spread/spread arbitrage* (`SPREAD`, 5/36 = 13.9 per cent): Aggregators and bridge protocols (1inch, Mento, Velora, ParaSwap, OpenOcean) capture positive price differences between routes during execution, booking the remainder as protocol revenue.

**Registered Anomalies**

*ANO-DeFi-01 — TVL-to-market-cap inversion.* Six strict-sample DeFi DApps (Pendle, Morpho, Maple, KernelDAO, EigenLayer, LIDO) exhibit TVL that materially exceeds their token market capitalisation, with Morpho reaching a TVL/MCap ratio of approximately 3,437× (TVL $187.5 billion vs MCap at data capture). This pattern is most acute for protocols serving as infrastructure for other protocols' liquidity — TVL accumulates through recursive collateral loops without commensurate token appreciation. The phenomenon is catalogued as ANO-MKT-02 in the broader dataset.

*ANO-DeFi-02 — Team-controlled launchpad at scale.* Pump.fun is the most-used DeFi DApp by active users (7.1 million) yet operates under TEAM\_CONTROLLED governance with a utility token. This inversion of the assumed decentralisation-scale relationship reflects the economics of memecoin launchpads: rapid iteration, content moderation, and fee-structure changes require centralised authority to remain competitive. The protocol's $900 million monthly volume demonstrates that high revenue is achievable without governance formalisation.

*ANO-DeFi-03 — Revenue concentration in non-governance protocols.* Among the five highest-volume DeFi DApps (Pump.fun, PancakeSwap V3, Jumper Exchange, Morpho, Helix), three are team-controlled or hybrid-governed. This indicates that revenue generation is not monotonically associated with governance maturity: the protocols capturing the greatest economic throughput are not necessarily those with the most formal governance structures.

---

### 4.6.2 Prediction Markets

Prediction markets constitute a small but analytically significant ecosystem: 31 DApps identified in the loose universe, with sector activity dominated by a single protocol. Polymarket accounts for 66.6 per cent of all prediction-market user activity and 95.3 per cent of sector volume ($858.8 million of $900.7 million total). The sector sits within the DappRadar `gambling` sector taxonomy — a classification choice that introduces a comparability caveat, since protocols that aggregate forecasts on political events, sports outcomes, or macroeconomic releases share the economic and informational function of financial derivatives, not casino wagering.

*Sample limitation.* Prediction market DApps overwhelmingly lack the financial metrics required for strict-sample inclusion. Polymarket — the dominant protocol — operates without a native token and without reportable TVL, disqualifying it from the strict filter. The v2 dataset identifies only one strict-sample prediction market DApp (Overtime Markets, `v2_ecosystem_focus = PREDICTION_MARKETS`). The analysis uses the loose universe (N=31) throughout.

**Chain Distribution**

**Table 4.7 — Top-5 chains by prediction market DApp presence (loose universe, N=31)**

| Chain | DApps | Share |
|-------|:-----:|:-----:|
| BNB Chain | 8 | 25.8% |
| Base | 6 | 19.4% |
| Polygon | 5 | 16.1% |
| Solana | 4 | 12.9% |
| Arbitrum | 3 | 9.7% |

*Note: multi-chain DApps counted per chain.*

Polygon hosts Polymarket — migrated from Ethereum in 2020 to reduce gas costs for individual resolution transactions. The multi-chain adoption rate for prediction markets (19.4 per cent) is the lowest of the five ecosystems examined, reflecting both the informational complexity of deploying oracle-dependent resolution across chains and the relative maturity barrier of the sector.

**Key DApps**

**Table 4.8 — Top prediction market DApps by active users (loose universe)**

| DApp | Users | Volume | Gov. type | Token | Chain |
|------|------:|-------:|:----------:|:-----:|-------|
| Polymarket | 215,114 | $858.8M | TEAM\_CONTROLLED | — | Polygon |
| CricSage | 59,934 | — | TEAM\_CONTROLLED | — | Skale-Nebula |
| Overtime | 32,296 | $24.8M | MULTISIG\_WITH\_COMMUNITY\_INPUT | UTILITY | Arbitrum/Base/Optimism |
| Predictions (PRDT) | 5,141 | $12.8M | SNAPSHOT\_OFFCHAIN | UTILITY | Multi-chain |
| Limitless | 3,153 | $3.6M | SNAPSHOT\_OFFCHAIN | UTILITY | Base |
| BetSwirl | 1,663 | $0.4M | TEAM\_CONTROLLED | UTILITY | Multi-chain |

**Governance Maturity**

**Table 4.9 — Prediction market governance distribution (loose universe, N=31)**

| Governance type | Count | Share |
|-----------------|:-----:|:-----:|
| TEAM\_CONTROLLED | 22 | 71.0% |
| SNAPSHOT\_OFFCHAIN | 6 | 19.4% |
| NONE | 2 | 6.5% |
| MULTISIG\_WITH\_COMMUNITY\_INPUT | 1 | 3.2% |
| **Total** | **31** | **100%** |

*Source: `governance_type` field, loose prediction market universe.*

Prediction markets are the most centralised of the five ecosystems: 71.0 per cent team-controlled and 100 per cent classified as either Centralized (71.0 per cent) or Semi-Decentralised (29.0 per cent); no prediction market DApp achieves a Decentralised classification. This structural centralisation reflects operational requirements: outcome resolution depends on oracle accuracy and dispute arbitration that necessitate rapid, authoritative intervention — functions difficult to implement through slow token-governance processes.

**Token Model Patterns**

The sector is notable for near-total absence of governance tokens: 74.2 per cent of prediction market DApps carry no native token. Among tokenised protocols, utility tokens predominate (19.4 per cent). This token-free design is commercially rational: a native token would introduce speculative dynamics into a platform whose value proposition depends on price-neutral information aggregation. The single strict-sample prediction market DApp (Overtime) uses a utility token with multisig-guarded community input rather than on-chain token governance, consistent with the sector pattern.

**Revenue Logic**

The v2 coding assigns Overtime a `v2_main_revenue_generator = SPREAD` and `v2_sustainment_model = SPREAD_ARB`, characterising the sector's dominant revenue mechanism. Prediction market protocols earn through: (1) *resolution fees* charged as a percentage of the settled market's volume (typically 2–5 per cent on winning positions); (2) *spread arbitrage* between taker and maker pricing in AMM-style prediction markets (Overtime's `SPREAD_ARB` model); and (3) *oracle service fees* in protocols that route resolution through UMA, Chainlink, or other providers. Polymarket's $858.8 million in volume at a 2 per cent fee structure implies approximately $17.2 million in annual fee revenue for a tokenless, team-controlled operator.

**Registered Anomalies**

*ANO-PRED-01 — Volume-per-user concentration.* Polymarket's implied volume-per-user is $3,992, placing it in the high-volume-per-user outlier category alongside major institutional DeFi protocols (see `dapp_anomalies.csv`). This ratio is driven by large-position wagering on high-stakes events — US elections, sports tournaments, macroeconomic releases — rather than retail participation breadth, and is not representative of the sector median.

*ANO-PRED-02 — "Trade signal" volume outlier.* One prediction-market-adjacent DApp ("Trade signal", `gambling :: NFT marketplace`) records $1.861 billion in volume against only 1,131 active users — a volume-per-user ratio of $1,645,485, the highest registered outlier in the `dapp_anomalies.csv` dataset. This extreme ratio is consistent with a front-end routing institutional order flow rather than reflecting genuine broad user activity, and the DApp carries a `NONE` governance classification with no token.

---

### 4.6.3 AI-Native DApps

#### Sector Definition

**Inclusion criteria.** A DApp is classified as AI-native if any of the following fields — `tags`, `sub_category`, `research_comments`, or `name` — contain at least one of the following terms: *ai*, *llm*, *machine learning*, *ai gaming*, or *ai-big-data* (full regex pattern: `\bai\b|artificial intelligence|machine learning|\bllm\b|ai gaming|ai-big-data`; case-insensitive). The classification is applied mechanically via the `mask_ai_dapps` function in `analytics_new/lib/themes.py`, which evaluates the combined text of all four fields per DApp.

**Exclusion criteria.** DApps excluded from the AI-native cohort despite surface-level AI language are those where: (a) the term "AI" appears only in a DApp name or mascot without reference to ML inference or AI-agent functionality in any documented feature (several memecoin or branding-only cases); or (b) the DApp is already captured in the Prediction Market or DePIN/RWA themes and does not independently qualify through the AI keyword rules. No manual override of the mechanical mask was applied; the 66 eligible DApps are the complete output of the inclusion rule applied to the loose universe.

**Functional definition.** An AI-native DApp, for the purposes of this thesis, is a blockchain-based application whose documented primary or secondary feature set incorporates machine-learning inference, AI-agent coordination, or AI-generated content as a core component of the user experience — whether delivered on-chain, through a hybrid on/off-chain architecture, or via an AI model accessed through a protocol-controlled API. This definition intentionally spans the heterogeneous sub-types identified in the dataset: AI gaming integrations (Hot Spring — The Cozy World, Sleepless AI, FishWar), autonomous AI-agent infrastructure and launchpads (Virtuals Protocol, ChainOpera AI), AI-powered data annotation and contribution platforms (Alaya AI), AI-enhanced social and content tools (Kaito, Sogni AI, CARV), and AI-adjacent security and developer tooling (ChainGPT, ZoRobotics).

*Sample limitation.* The v2 dataset identifies three strict-sample AI DApps: ChainOpera AI, Virtuals Protocol, and ChainGPT. The analysis uses the loose universe (N=66) throughout, with strict-eligible DApps noted where relevant.

---

#### Sector Structure and Category Distribution

The 66 AI-native DApps span nine primary sectors. The `other` sector holds the plurality (29 DApps, 43.9 per cent) — consistent with the cross-cutting, hard-to-classify nature of AI-enabled applications that do not fit neatly into DeFi, gaming, or social taxonomies. NFT Gaming (16 DApps) and NFT marketplace (13 DApps) are the most represented application categories, reflecting the early-adoption of AI features in gaming reward economies and AI-generated content marketplaces.

**Table 4.10 — AI DApp distribution by application category (loose universe, N=66)**

| Category | Count | Share |
|----------|:-----:|:-----:|
| NFT Gaming | 16 | 24.2% |
| NFT marketplace | 13 | 19.7% |
| Social Network | 11 | 16.7% |
| Infrastructure | 7 | 10.6% |
| DAO Tooling | 5 | 7.6% |
| DEX | 4 | 6.1% |
| SocialFi | 3 | 4.5% |
| Metaverse | 2 | 3.0% |
| Other categories | 5 | 7.6% |

*Source: `dapp_category` field, AI DApp theme universe (`theme_ai_dapps`).*

Three functionally distinct archetypes account for the majority of the AI DApp population:

1. **AI gaming and reward-economy applications** (approximately 30–35 DApps): Integrate AI-generated environments, AI non-player characters (NPCs), or AI-scored tasks into play-to-earn or move-to-earn models. Revenue is deferred to token appreciation; on-chain volume is near zero despite high user counts.

2. **AI infrastructure and agent platforms** (approximately 7–10 DApps): Provide compute, model access, or agent-launch infrastructure to other protocols. Revenue is fee-based (usage metering, launchpad take-rate). Market capitalisation is disproportionately high relative to user counts, as markets price platform optionality on the AI-agent economy.

3. **AI-enhanced social and content platforms** (approximately 15–20 DApps): Apply AI to content recommendation, community moderation, or user-generated AI art. Governance is most frequently Snapshot off-chain; token models lean toward utility or governance-adjacent designs.

---

#### Chain Distribution

**Table 4.11 — Top chains by AI DApp deployment (loose universe, N=66)**

| Chain | Deployments | Share of AI cohort |
|-------|:-----------:|:------------------:|
| BNB Chain | 26 | 39.4% |
| Base | 22 | 33.3% |
| Ethereum | 21 | 31.8% |
| Arbitrum | 13 | 19.7% |
| opBNB | 12 | 18.2% |
| Polygon | 10 | 15.2% |
| Solana | 7 | 10.6% |
| Linea | 5 | 7.6% |

*Note: multi-chain DApps are counted once per chain; shares do not sum to 100%.*

BNB Chain's leading position (39.4 per cent of AI DApps) is driven by the preponderance of AI gaming and reward-economy applications targeting the Telegram Mini App and opBNB micro-transaction ecosystems. opBNB itself ranks fifth (18.2 per cent) as the preferred scaling chain for gaming reward distributions that require sub-cent transaction fees. Base's strong showing (33.3 per cent) reflects the concentration of venture-backed AI infrastructure and agent-platform projects on Coinbase's L2 — Virtuals Protocol, its largest AI DApp by market cap, launched on Base and has attracted derivative agent projects to the same chain. The 40.9 per cent multi-chain adoption rate sits above the prediction market baseline (19.4 per cent) and roughly in line with the cross-ecosystem average (36.2 per cent), but well below the DeFi sector rate of 55.2 per cent — suggesting that AI DApps chain-select for user acquisition and cost rather than for financial composability.

---

#### Key DApps

**Table 4.12 — Representative AI DApps by active users (loose universe)**

| DApp | Users | Volume | MCap | Gov. type | Token | Archetype |
|------|------:|-------:|-----:|:----------:|:-----:|:--------:|
| Hot Spring — The Cozy World | 2,924,351 | — | — | HYBRID | REWARD | Gaming/reward |
| Alaya AI | 1,869,774 | — | — | TEAM\_CONTROLLED | UTILITY | Data/reward |
| FishWar | 560,738 | $0.9M | $0.3M | TEAM\_CONTROLLED | REWARD | Gaming/reward |
| OpenPad AI | 293,016 | — | — | TEAM\_CONTROLLED | — | Social/tools |
| ChainOpera AI | 162,072 | $0.1M | $105.5M | SNAPSHOT\_OFFCHAIN | — | Infrastructure |
| Sleepless AI | 73,338 | — | $19.9M | SNAPSHOT\_OFFCHAIN | REWARD | Gaming/reward |
| Virtuals Protocol | 39,464 | $7.8M | $606.3M | ONCHAIN\_TOKEN\_GOVERNANCE | GOVERNANCE | Infrastructure |
| Kaito | ~18,000 | — | $161.4M | SNAPSHOT\_OFFCHAIN | GOVERNANCE | Social/tools |
| ChainGPT | 20,145 | $0.3M | $34.5M | SNAPSHOT\_OFFCHAIN | UTILITY | Infrastructure |

---

#### Governance Structure

**Table 4.13 — AI DApp governance distribution (loose universe, N=66)**

| Governance type | Count | Share |
|-----------------|:-----:|:-----:|
| TEAM\_CONTROLLED | 36 | 54.5% |
| SNAPSHOT\_OFFCHAIN | 26 | 39.4% |
| NONE | 2 | 3.0% |
| HYBRID | 1 | 1.5% |
| ONCHAIN\_TOKEN\_GOVERNANCE | 1 | 1.5% |
| **Total** | **66** | **100%** |

*Source: `governance_type` field, AI DApp theme universe (`theme_ai_dapps`).*

AI DApps exhibit a strongly bimodal governance distribution: protocols are either fully team-controlled (54.5 per cent) or rely on Snapshot off-chain voting (39.4 per cent). On-chain governance is represented by a single DApp — Virtuals Protocol — accounting for 1.5 per cent of the cohort. This compares with 6.4 per cent on-chain governance prevalence in the full loose universe (DAO\_WITH\_TIMELOCK + ONCHAIN\_TOKEN\_GOVERNANCE combined), confirming that AI DApps are substantially less formally governed than the cross-ecosystem baseline.

A notable pattern is that AI DApps are disproportionately represented in the Snapshot off-chain tier relative to the non-AI ecosystem: 39.4 per cent versus 17.5 per cent for non-AI DApps. This suggests that AI-sector teams signal community orientation through off-chain voting mechanisms earlier in their lifecycle than non-AI peers — perhaps as a marketing or fundraising posture — while retaining operational authority to act on or ignore the resulting votes. Research comments confirm this interpretation: for FishWar, the annotation reads "token has 'platform governance voting,' but no evidence of binding on-chain DAO; team likely executes"; for ZoRobotics: "markets DAO-based validation; practical control remains with project team today"; for ChainOpera AI: "Whitepaper describes DAO voting via staked tokens; execution still team-led at present."

By ownership structure, 86.4 per cent of AI DApps are COMPANY\_OWNED — the highest of any thematically defined sub-group in the dataset. A single DApp (Treasure, 1.5 per cent) is DAO\_OWNED; two are FOUNDATION\_OWNED. This near-universal corporate ownership confirms that the AI DApp sector is, in practical terms, a corporate software sector with blockchain token issuance rather than a community-governed decentralised application sector.

**Governance comparison with non-AI ecosystem**

| Metric | AI DApps (N=66) | Non-AI ecosystem (N=789) |
|--------|:---------------:|:------------------------:|
| Team-controlled | 54.5% | 64.3% |
| Snapshot off-chain | 39.4% | 17.5% |
| On-chain governance (any) | 1.5% | 6.4% |
| Company-owned | 86.4% | 82.8% |
| DAO-owned | 1.5% | 2.8% |

The AI sector is slightly *less* team-controlled than the non-AI DApp universe, but achieves this lower rate through Snapshot off-chain mechanisms rather than through formal on-chain governance — a lateral move within the centralised governance zone rather than progress toward decentralisation.

---

#### Decentralisation Analysis: The Zero Fully Decentralised Finding

*This section addresses the finding noted in the thesis goal annotation: zero fully decentralised AI DApps in the loose universe.*

No AI DApp in the 66-DApp cohort achieves the `DECENTRALIZED` classification under the coding framework used in this thesis (which requires: on-chain governance with binding token-weighted voting, open participation, and at least semi-independent protocol execution). The decentralisation distribution is:

**Table 4.14 — Decentralisation levels: AI DApps versus full ecosystem**

| Decentralisation level | AI DApps (N=66) | AI share | Full ecosystem (N=855) | Ecosystem share |
|------------------------|:---------------:|:--------:|:----------------------:|:---------------:|
| CENTRALIZED | 28 | 42.4% | 486 | 56.8% |
| SEMI\_DECENTRALIZED | 38 | 57.6% | 330 | 38.6% |
| DECENTRALIZED | **0** | **0.0%** | 39 | **4.6%** |

*Source: `level_of_decentralisation` field.*

The zero-decentralised finding is not a data artefact. Four independent structural explanations account for it:

**1. Off-chain AI computation as an inherent centralisation vector.** AI inference — whether large language model inference, computer vision, or reinforcement learning — requires substantial off-chain compute. Model weights, training data, and inference endpoints reside on centralised infrastructure (cloud providers or team-operated servers). The `DECENTRALIZED` coding tier requires that protocol execution can function without a central operator. Because the AI inference layer cannot satisfy this requirement with current technology, any DApp whose core functionality depends on AI inference cannot meet the threshold for full decentralisation, regardless of its financial governance structure. This is not a policy choice but a technical constraint of the current AI-blockchain integration paradigm.

**2. Youth of the sector and governance lifecycle position.** The 39 fully decentralised DApps in the broader loose universe are predominantly mature DeFi protocols (Compound, Aave, Uniswap, and their structural analogues) that have traversed a multi-year governance evolution from team control to Snapshot voting to DAO-with-timelock to on-chain self-execution. The AI DApp cohort is concentrated in the 2023–2025 launch window — a period too early for the governance lifecycle to have progressed to the `DECENTRALIZED` tier. Among the 35 fully decentralised non-AI DApps in the DeFi and exchanges sectors, the governance tenure spans three to seven years; the modal AI DApp has governance tenure under two years.

**3. Near-universal corporate ownership constrains governance trajectory.** With 86.4 per cent of AI DApps COMPANY\_OWNED and a single DAO\_OWNED DApp, the ownership structure creates a practical impediment to decentralisation: corporate ownership entities typically retain IP rights, model update authority, and regulatory compliance obligations that are legally incompatible with ceding control to an autonomous DAO. The DeFi protocols that achieved full decentralisation did so by relinquishing corporate control through foundation structures or pure smart-contract deployment — a step that AI-sector companies have not taken, in part because AI model governance (safety updates, capability restrictions) requires a responsible legal entity.

**4. Regulatory and safety imperatives for centralised override.** AI systems require the ability to roll back or patch deployed models in response to safety incidents, capability misuse, or regulatory directives (e.g., EU AI Act obligations on high-risk AI systems). This override requirement is structurally incompatible with the governance immutability that characterises fully decentralised on-chain protocols, where code changes require token-holder supermajority approval with timelock delays. The research comment for ZoRobotics is illustrative: the team "markets DAO-based validation; practical control remains with project team today" — a configuration that likely reflects not only product maturity but also a deliberate preservation of team-override authority.

**The Virtuals Protocol paradox.** Virtuals Protocol is classified as ONCHAIN\_TOKEN\_GOVERNANCE — the most formally governed AI DApp in the dataset — yet remains coded CENTRALIZED. The research annotation reads: "eVIRTUAL tokenholders vote on-chain; DAO/forum active; team still builds products but governance powers sit with veVIRTUAL holders → high decentralization." This constitutes a borderline case: the governance mechanism is on-chain, but the AI agent curation and platform operational decisions remain team-led. The CENTRALIZED rating reflects the current state of operational control rather than the governance architecture alone — a distinction that highlights the insufficiency of formal governance apparatus as a proxy for effective decentralisation in AI-native protocols.

**INS-AI-01 — Structural impossibility of fully decentralised AI DApps under current technology.** The zero-decentralised finding warrants formalisation as a sector-level insight: *fully decentralised AI-native DApps are a theoretical category that the 2023–2025 technology stack cannot realise*. Decentralised AI inference (homomorphic encryption of model weights, fully verifiable on-chain ML execution, or comparable approaches) remains a research problem rather than a deployed product. Until these compute primitives mature, the AI DApp sector will structurally occupy the CENTRALIZED or SEMI\_DECENTRALIZED tiers regardless of governance maturation, and performance comparisons with the DECENTRALIZED tier of the broader DApp universe are not meaningful.

---

#### Token Model Patterns

Of the 66 AI DApps, 50 (75.8 per cent) have issued a token. The remaining 16 (24.2 per cent) are tokenless — a higher no-token rate than the DeFi sector (approximately 15 per cent) but lower than prediction markets (approximately 40 per cent).

**Table 4.15 — AI DApp token type distribution (token-issuing DApps, N=50)**

| Token type | Count | Share of token-issuers |
|------------|:-----:|:----------------------:|
| UTILITY | 28 | 56.0% |
| REWARD | 10 | 20.0% |
| GOVERNANCE | 6 | 12.0% |
| SPECULATIVE | 3 | 6.0% |
| GOVERNANCE + UTILITY | 2 | 4.0% |
| SOCIAL | 1 | 2.0% |

*Source: `token_type` field.*

Utility tokens dominate (56.0 per cent of token-issuers; 42.4 per cent of the full cohort), consistent with AI DApps using tokens primarily to gate access to AI services, distribute compute credits, and incentivise data contributions. Reward tokens (20.0 per cent of token-issuers) are concentrated in gaming-adjacent AI applications that distribute tokens for AI-beneficial tasks: data labelling (Alaya AI), physical movement (Sleepless AI), and play-to-earn completion (Hot Spring — The Cozy World, FishWar). Pure governance tokens appear in 12.0 per cent of token-issuing AI DApps (6 DApps) — a low governance-token prevalence consistent with the sector's limited formal governance development. The `theme_cohort_summary.csv` records a cross-cohort governance token prevalence of 12.1 per cent, aligned with this range.

No AI DApp in the dataset operates a pure fee-switch governance token model (where governance rights map directly to protocol revenue claims) at scale — the closest approximation is Virtuals Protocol's veVIRTUAL staking, which grants governance votes and fee-distribution rights but within a corporate-controlled product environment.

---

#### Revenue Logic

AI DApp revenue divides into three models, identified through the v2 `v2_main_revenue_generator` field for the three strict-sample DApps and extended analytically to the loose universe:

1. **Usage metering** (`USAGE_METERING`): ChainOpera AI and ChainGPT charge compute credits for API-accessible AI inference; `v2_sustainment_model = FEES` and `SUBSCRIPTION` respectively. This model mirrors enterprise SaaS pricing applied to on-chain-accessible AI services. It is financially sustainable but concentrates revenue in the infrastructure sub-type rather than the broad AI DApp population.

2. **Take-rate on agent launches** (`TAKE_RATE`): Virtuals Protocol charges a percentage of initial bonding-curve liquidity when AI agents are launched on its platform. This model is analogous to token launchpad fees but applied to autonomous agent primitives, enabling revenue proportional to the growth of the AI agent economy.

3. **Tokenomics-subsidised engagement** (majority of the loose-universe AI DApps): Hot Spring, Alaya AI, FishWar, and most large-user-count AI DApps distribute reward tokens for in-application activity rather than extracting fees. This is a user-acquisition model that defers monetisation to token appreciation and secondary-market activity — a structure with positive cash flow only if token markets sustain or appreciate, an assumption that holds during bull markets but collapses during contractions.

---

#### Maturity Indicators

Assessed across the standard maturity dimensions used in this thesis:

| Metric | AI DApps (N=66) | Full loose universe (N=855) |
|--------|:---------------:|:---------------------------:|
| Median active users | 1,232 | ~2,400 |
| Median volume (USD) | $785 | ~$28,000 |
| Multi-chain rate | 40.9% | 36.2% |
| Mean activity signal count | 3.4 | ~3.1 |
| Data completeness score (mean) | 0.84 | ~0.79 |
| Token issuance rate | 75.8% | ~65% |

*Source: `prepared_data.csv`; full-universe figures are derived from the full dataset for comparison.*

The AI DApp cohort is relatively data-complete (mean score 0.84) and slightly above average on activity signal count (3.4 versus ~3.1 ecosystem-wide), indicating that AI-branded projects attract sufficient analytic coverage to be reliably coded. However, median active users (1,232) and volume ($785) are well below ecosystem medians — reflecting the preponderance of early-stage or reward-economy protocols whose user activity does not generate financial throughput. Multi-chain adoption at 40.9 per cent is above the ecosystem median, consistent with AI DApps actively seeking broad user distribution across multiple L2 and L1 ecosystems.

The high token issuance rate (75.8 per cent) relative to the AI sector's governance and revenue maturity represents a structural tension: tokens are issued early — often as the primary incentive and funding mechanism — but governance and decentralisation infrastructure lag behind, producing a cohort in which most token-holders hold instruments that carry no meaningful governance rights in practice.

---

#### Registered Anomalies

*ANO-AI-01 — User–volume decoupling.* The two most-used AI DApps by active wallet count — Hot Spring (2.9 million users) and Alaya AI (1.9 million users) — report zero recorded volume. This decoupling indicates reward economies in which activity generates token distributions but not financial throughput traceable as on-chain "volume" in DappRadar's framework. The same pattern holds for OpenPad AI (293,016 users, $0 volume) and Sleepless AI (73,338 users, $0 volume), classifying these DApps as structurally incompatible with volume-based performance benchmarks calibrated on DeFi or NFT activity.

*ANO-AI-02 — Market capitalisation inversion relative to user scale.* Virtuals Protocol carries a $606.3 million MCap with 39,464 active users (MCap-per-user ≈ $15,365), while Hot Spring has 2.9 million users and zero MCap. This near-perfect anti-correlation between financial valuation and user activity within the AI sector indicates that market participants price AI protocol infrastructure as platform options on the emerging AI-agent economy — not on revenue or user metrics. The total AI DApp combined market cap of $1.61 billion is dominated by the infrastructure sub-type (Virtuals Protocol, ChainOpera AI, Kaito, CARV) despite these protocols collectively holding fewer than 250,000 active users.

---

### 4.6.4 Real-World Assets (RWA)

The RWA ecosystem encompasses DApps whose economic purpose involves bridging on-chain protocols with off-chain financial assets: tokenised securities, institutional lending markets, synthetic yield instruments, and payment infrastructure. Forty-three DApps are identified in the loose universe through tag and category matching on "rwa", "real world", and the `Payments/RWA` sub-category field. The category spans two economically distinct protocol types that share a common attribute — off-chain asset backing — but differ substantially in scale, user profile, and revenue model: *institutional DeFi* protocols (Ethena, Maple) targeting capital-intensive participants, and *tokenised consumer asset* protocols (Courtyard, WiFi Map) targeting retail participants through tokenised physical objects or service rights.

*Sample limitation.* The strict sample contains approximately three to five RWA-adjacent DApps. Ethena — classified in the `defi` sector with a `Payments/RWA` sub-category — is the most metrics-complete RWA DApp and is included via its sub-category classification. Velo and Maple are coded `v2_ecosystem_focus = DEFI` but operate in institutional yield and lending spaces that are functionally RWA-adjacent. The v2 DEPIN category additionally captures some infrastructure DApps that have RWA characteristics (WiFi Map). The analysis uses the loose RWA universe (N=43) with these cross-coding notes.

**Chain Distribution**

**Table 4.13 — Top-5 chains by RWA DApp presence (loose universe, N=43)**

| Chain | RWA DApps | Share |
|-------|:---------:|:-----:|
| Ethereum | 11 | 25.6% |
| Polygon | 10 | 23.3% |
| Base | 10 | 23.3% |
| TON | 8 | 18.6% |
| BNB Chain | 8 | 18.6% |

*Note: multi-chain DApps counted per chain.*

Ethereum's leading position is expected: tokenised treasuries, institutional lending, and synthetic dollar protocols require the settlement finality and regulatory familiarity associated with Ethereum mainnet. TON's 18.6 per cent share reflects Telegram's strategy of integrating real-world payment and asset rails within its messaging ecosystem. The 37.2 per cent multi-chain adoption rate is lower than DeFi (55.2 per cent), consistent with the institutional focus of leading RWA protocols where single-chain deployment limits cross-chain composability risk.

**Key DApps**

**Table 4.14 — Top RWA DApps by TVL and users (loose universe)**

| DApp | Users | Volume | TVL | MCap | Gov. type |
|------|------:|-------:|----:|-----:|:----------:|
| Ethena | 9,104 | $892.6M | $14,224.9M | $1,830.8M | HYBRID |
| Maple | 12,797 | $34,295.5M | $2,629.0M | $0.3M | SNAPSHOT\_OFFCHAIN |
| WiFi Map | 1,648,601 | $0.5K | — | $2.0M | SNAPSHOT\_OFFCHAIN |
| WorldShards | 520,148 | $91.8K | — | $15.1M | TEAM\_CONTROLLED |
| Velo | 78,519 | $739.5K | $94.5K | $260.1M | TEAM\_CONTROLLED |
| Courtyard | 40,275 | $30.2M | — | — | TEAM\_CONTROLLED |
| Fiat24 | 13,821 | $5.5M | — | — | NONE |
| Solayer | 9,371 | $1.2K | $40.4M | $46.9M | SNAPSHOT\_OFFCHAIN |

**Governance Maturity**

**Table 4.15 — RWA governance distribution (loose universe, N=43)**

| Governance type | Count | Share |
|-----------------|:-----:|:-----:|
| TEAM\_CONTROLLED | 26 | 60.5% |
| SNAPSHOT\_OFFCHAIN | 9 | 20.9% |
| NONE | 6 | 14.0% |
| HYBRID | 1 | 2.3% |
| DAO\_WITH\_TIMELOCK | 1 | 2.3% |
| **Total** | **43** | **100%** |

*Source: `governance_type` field, loose RWA universe. `theme_depin_rwa` theme cohort governance token prevalence: 7.2%, `top_governance_type`: TEAM\_CONTROLLED.*

RWA protocols are the second-most centralised ecosystem (60.5 per cent team-controlled) after prediction markets. Only KlimaDAO (carbon-credit tokenisation) operates a DAO\_WITH\_TIMELOCK. The decentralisation rate (2.3 per cent) is the lowest of the five ecosystems. This structural centralisation is partly regulatory: compliance for tokenised real-world assets frequently requires a corporate entity as legal custodian, making full on-chain governance legally and operationally problematic. The contrast with DeFi's 13.3 per cent decentralisation rate is stark and reflects the fundamentally different legal exposure of RWA versus pure on-chain DeFi protocols.

**Token Model Patterns**

The no-token share (55.8 per cent) is the highest of the five ecosystems, reflecting institutional DeFi protocols (Maple, Fiat24) and payment infrastructure that derive value from financial execution rather than token-mediated incentives. Among tokenised protocols, utility tokens are the most common design (32.6 per cent), used primarily to access protocol services (Ethena's ENA for committee-based governance participation, WiFi Map's WIFI for hotspot data access). Governance tokens appear in only 2.3 per cent of RWA DApps (KlimaDAO alone), the lowest governance-token prevalence of the five ecosystems.

**Revenue Logic**

RWA revenue mechanisms are sector-specific, and the v2 coding captures three patterns for strict-adjacent DApps:

1. *Yield spread on real-world assets* (`INTEREST_MARGIN`; Velo, Maple, Aave v3 RWA pools): Ethena earns basis-trade yields from staked ETH derivatives and perpetual futures funding rates, passing yield to sUSDe holders minus a protocol fee. Maple intermediates institutional lending, charging origination and management fees on a $2.6 billion TVL base. The v2 `v2_sustainment_model = INTEREST_YIELD` for these protocols.

2. *Tokenised asset transaction fees* (`TAKE_RATE`): Courtyard charges minting, redemption, and marketplace fees for tokenised physical collectibles (authenticated trading cards), with revenue proportional to secondary-market volume ($30.2 million in the data period).

3. *Performance fees* (`PERFORMANCE_FEE`): Mitosis (a yield coordination protocol operating at the boundary of DeFi and RWA) captures a share of yield generated above benchmark rates for depositors, with `v2_main_revenue_generator = PERFORMANCE_FEE`.

**Registered Anomalies**

*ANO-RWA-01 — Ethena TVL-to-MCap inversion.* Ethena's TVL ($14.2 billion) exceeds its token market capitalisation ($1.8 billion) by a factor of approximately 7.8×. This is an instance of the broad ANO-MKT-02 anomaly (§4.3.3) and is structurally explained by Ethena's model: sUSDe deposits are backed by staked ETH and short perpetual positions, generating TVL as depositor liability rather than equity value. The result is a protocol whose economic scale dwarfs its equity capitalisation by design.

*ANO-RWA-02 — Maple capital velocity.* Maple's 30-day volume ($34.3 billion) exceeds its TVL ($2.6 billion) by approximately 13.1×, indicating capital velocity — the repeated recycling of institutional capital through short-tenor lending cycles — rather than passive lock-up. This velocity ratio is the highest observed in the dataset for any lending-category protocol and identifies Maple as an active liquidity intermediary operating a revolving-door model rather than a static collateral warehouse.

---

### 4.6.5 Decentralised Physical Infrastructure (DePIN)

DePIN encompasses protocols that coordinate physical hardware or physical-world data collection through token-incentivised networks. Twenty-nine DApps are identified in the loose universe through "depin" and "move to earn" tag matching. The category spans wireless data sharing (WiFi Map, XPIN Network), fitness and movement tracking (Sweat Economy, SuperWalk, dexGO), gaming hardware (Gaimin), and messaging infrastructure (Dmail Network). The v2 coding identifies two strict-sample DePIN DApps (WiFi Map and XPIN Network), both coded `v2_sustainment_model = TOKENOMICS`, confirming the sector-wide pattern of token-incentivised rather than fee-based sustainability.

*Sample limitation.* DePIN DApps rarely meet strict-sample financial criteria: most protocols report near-zero token market capitalisation and minimal volume, failing the strict filter. The v2 strict sample has only two DePIN DApps (both LOW-to-MEDIUM v2 coding confidence). The analysis uses the loose universe (N=29) throughout.

**Chain Distribution**

**Table 4.16 — Top-5 chains by DePIN DApp presence (loose universe, N=29)**

| Chain | DePIN DApps | Share |
|-------|:-----------:|:-----:|
| BNB Chain | 13 | 44.8% |
| Ethereum | 11 | 37.9% |
| Polygon | 10 | 34.5% |
| opBNB | 7 | 24.1% |
| Base | 7 | 24.1% |

*Note: multi-chain DApps counted per chain.*

BNB Chain's dominance (44.8 per cent) reflects consumer hardware applications with frequent micro-transactions — a use pattern well-suited to BNB Chain's low gas fees and opBNB's further fee reduction. The 55.2 per cent multi-chain adoption rate is the highest of the non-DeFi ecosystems, indicating that DePIN protocols deploy across chains primarily to reach broader user and token-distribution networks rather than for financial composability.

**Key DApps**

**Table 4.17 — Top DePIN DApps by active users (loose universe)**

| DApp | Users | Volume | Gov. type | Token | Activity type |
|------|------:|-------:|:----------:|:-----:|:-------------:|
| Dmail Network | 2,088,315 | $13.7K | TEAM\_CONTROLLED | — | Web3 messaging |
| WiFi Map | 1,648,601 | $0.5K | SNAPSHOT\_OFFCHAIN | UTILITY | WiFi data sharing |
| Sweat Economy | 831,766 | $160.7K | HYBRID | REWARD | Move-to-earn |
| dexGO | 106,751 | — | TEAM\_CONTROLLED | — | GPS data collection |
| Piratopia | 100,648 | $3 | TEAM\_CONTROLLED | — | Gaming + DePIN |
| XPIN Network | 66,681 | $88.4K | TEAM\_CONTROLLED | — | Mobile network mapping |
| SuperWalk | 27,895 | $603.6K | SNAPSHOT\_OFFCHAIN | REWARD | Move-to-earn |
| Gaimin | 9,765 | $12.5 | TEAM\_CONTROLLED | — | GPU compute |

**Governance Maturity**

**Table 4.18 — DePIN governance distribution (loose universe, N=29)**

| Governance type | Count | Share |
|-----------------|:-----:|:-----:|
| TEAM\_CONTROLLED | 16 | 55.2% |
| SNAPSHOT\_OFFCHAIN | 10 | 34.5% |
| HYBRID | 1 | 3.4% |
| ONCHAIN\_TOKEN\_GOVERNANCE | 1 | 3.4% |
| NONE | 1 | 3.4% |
| **Total** | **29** | **100%** |

*Source: `governance_type` field, loose DePIN universe.*

Two DApps (6.9 per cent) achieve Decentralised status — the highest rate outside the DeFi and exchanges sectors. Sweat Economy achieves Hybrid decentralisation through a "one-person, one-vote" model enforced by physical activity verification rather than token weighting. The remaining 55.2 per cent semi-decentralised DApps typically operate Snapshot-based voting for token reward parameters while retaining centralised control over hardware onboarding and network topology. The `theme_depin_rwa` theme cohort reports TEAM\_CONTROLLED as the top governance type (consistent with this distribution) and 7.2 per cent governance token prevalence.

**Token Model Patterns**

The no-token share (37.9 per cent) is lower than RWA (55.8 per cent) and prediction markets (74.2 per cent) but higher than DeFi (30.5 per cent), reflecting the phase-specific token deployment of DePIN networks: protocols in pre-token phases attract participants with future token promises, while mature protocols use reward tokens to incentivise infrastructure provision. Reward tokens (20.7 per cent) are proportionally more common in DePIN than in any other ecosystem examined, consistent with the participation-reward model where tokens compensate hardware contribution rather than represent governance rights. The v2 coding confirms that both strict-sample DePIN DApps rely on tokenomics (`v2_sustainment_model = TOKENOMICS`) with advertising (WiFi Map: `v2_main_revenue_generator = ADS`) as WiFi Map's primary cash-denominated revenue source.

**Revenue Logic**

DePIN revenue models differ structurally from DeFi and prediction markets:

1. *Infrastructure reward cycles*: Contributors receive token rewards for providing capacity (WiFi hotspots, GPS waypoints, GPU compute cycles). Protocol-level revenue is implicitly extracted through token inflation, with treasury-owned supply funding contributor rewards at the expense of existing token holders. Both strict-sample DePIN DApps (WiFi Map, XPIN Network) operate under this model.

2. *Data monetisation* (WiFi Map): The protocol aggregates crowd-sourced hotspot data and sells data access to navigation apps and telecoms, distributing a share of data revenue to contributors. The v2 coding assigns `v2_main_revenue_generator = ADS` for WiFi Map, reflecting ad-supported and data-licensing revenue embedded in the platform's consumer app.

3. *Enterprise compute contracts* (Gaimin): Gaimin and similar GPU-compute DePIN protocols contract with AI/ML enterprises for burst compute capacity, distributing fees to hardware node operators. This model introduces direct enterprise revenue in addition to tokenomics-based incentives, though at small absolute scale ($12.5 monthly volume in the data period).

**Registered Anomalies**

*ANO-DEPIN-01 — Near-zero volume at large user scale.* The DePIN sector collectively records $8.6 million in volume against 4.9 million active users — an average volume-per-user of $1.74, the lowest of any sector in the dataset. This figure is not anomalous within DePIN's economic model (participation rewards rather than financial transactions generate activity), but it represents a categorical incompatibility with volume-based DApp performance metrics. DePIN protocols are misclassified as low-performing when evaluated against volume benchmarks calibrated on DeFi or NFT marketplace activity. The finding reinforces the broader argument (§4.5.2) that sector-disaggregated metrics are required for accurate ecosystem assessment.

*ANO-DEPIN-02 — Decentralisation through physical consensus.* Sweat Economy (831,766 users) achieves Hybrid decentralisation status through a "one-person, one-vote" governance model enforced by physical activity verification rather than token-weighted voting — a mechanism with no precedent in the DeFi governance literature. This pattern indicates that DePIN protocols may develop effective decentralisation through physical-world verification architectures rather than through the token-based governance structures that define decentralisation in DeFi sectors. The cross-sector applicability of standard decentralisation metrics to DePIN governance is therefore an open methodological question.

---

## 4.7 Token Analysis

### 4.7.1 Token Adoption Rate

Across the full 855-DApp dataset, 50.2 per cent of DApps operate a native token; the remaining 49.8 per cent either have no token or lacked a verifiable token match in the CoinMarketCap and CoinGecko APIs at the time of collection. Token adoption is substantially higher in DeFi-adjacent categories — where token design enables incentive alignment, liquidity mining, and governance participation — than in gaming and social DApps, where token integration is more varied in form and economic function.

Within the strict sample (N=68), six DApps (8.8 per cent) have no token, as recorded in the `token_type` field of the governance × token cross-tabulation (`crosstab_governance_token_strict.csv`).

### 4.7.2 Token Type Distribution in the Strict Sample

Table 4.3 presents the token type distribution for the strict sample, derived from `crosstab_governance_token_strict.csv`.

**Table 4.3 — Token type distribution: strict sample (N=68)**

| Token type | Count | Share of strict sample |
|-----------|:-----:|:----------------------:|
| UTILITY | 30 | 44.1% |
| GOVERNANCE | 17 | 25.0% |
| REWARD | 14 | 20.6% |
| NONE (no token) | 6 | 8.8% |
| SOCIAL | 1 | 1.5% |
| **Total** | **68** | **100%** |

*Source: `crosstab_governance_token_strict.csv`*

Utility tokens represent the plurality at 44.1 per cent. Reward tokens — typically used in liquidity mining, staking, or play-to-earn programmes — account for 20.6 per cent, reflecting the prevalence of yield-bearing incentive structures even among high-signal DApps. Social tokens constitute a marginal share (1.5 per cent), consistent with the small footprint of the social sector in the strict sample noted in §4.5.3.

### 4.7.3 Governance Token Prevalence (INS-TOK-01)

Governance tokens are present in 17 DApps as classified by the `token_type` field (25.0 per cent of the strict sample). The governance-token flag analysis (INS-TOK-01) reports a governance token prevalence of 26.47 per cent, which reflects a slightly broader classification that includes tokens with hybrid governance and utility characteristics; the two figures bracket the effective range of governance token prevalence in the strict sample.

Governance tokens are concentrated in on-chain governance regimes: all 13 DApps with DAO-with-timelock or on-chain token governance hold governance tokens, accounting for 76.5 per cent of all governance tokens in the sample. The remaining four governance tokens appear in DApps operating Snapshot off-chain governance — indicating that some projects issue governance tokens while conducting voting off-chain rather than on-chain, potentially to reduce gas costs or simplify the voting interface.

The co-occurrence pattern between governance token issuance and governance architecture has an important implication: the presence of a governance token is a necessary but not sufficient condition for on-chain governance. Many utility and reward tokens coexist with community governance processes (particularly Snapshot-based voting), while some governance tokens coexist with team-controlled governance structures, suggesting that token design and operational governance authority are partially decoupled in practice. This decoupling is examined interpretively in §5.3.

---

## 4.8 Cohort Analysis

### 4.8.1 Sector × Category Cohort Structure

Within the strict universe (N=68), DApps are organised into sector × category cohorts using a composite signal-weighting scheme (`cohort_manifest.json`). The cohort selection algorithm assigns each DApp to a cell defined by its `dapp_sector` and `dapp_category`. Cells with at least 20 strict-eligible DApps are designated primary cohorts, from which a top-K subset is drawn by weighted log-signal composite; cells with fewer than 20 eligible entries are designated secondary cohorts and retain all eligible DApps.

The composite signal score weights the five core activity signals as follows: users (weight 1.0), volume (1.0), TVL (0.8), market cap (0.8), and transactions (0.6). Signals are log-transformed before weighting to reduce the influence of extreme outliers.

In practice, no sector × category cell in the strict universe reaches the 20-DApp threshold for primary cohort selection — the largest cell (exchanges :: DEX) contains 13 eligible DApps and the next largest (defi :: DEX) contains eight. Consequently, all cohorts in the strict universe are secondary cohorts, retaining all eligible DApps within each cell. This means the cohort analysis is in effect a sector × category decomposition of the strict sample rather than a filtered top-K selection.

**[Figure 4.13: Governance × ownership heatmap — primary cohort]**
*File: `figures/02_governance_heatmaps_cohort.png`*

**[Figure 4.14: Governance × token type heatmap — primary cohort]**
*File: `figures/02_governance_token_heatmap_cohort.png`*

**[Figure 4.15: Governance label distribution — primary cohort]**
*File: `figures/02_governance_distribution_cohort.png`*

### 4.8.2 Performance Clustering (K-means)

A complementary performance clustering analysis, applied to the full 855-DApp dataset using K-means (k=4, random\_state=42, n\_init=10), partitions DApps with complete performance data into four tiers based on seven features: log-transformed active users, market cap, TVL, volume, and transaction count, plus the composite governance score and a market maturity index (both entered without log transformation). All features are standardised using z-score normalisation before clustering. The four resulting clusters, as reported in the full-dataset analysis (`analytics/06_performance_analysis.py`), are characterised as follows:

**Struggling** (approximately 30 per cent of DApps with complete data): below-median performance on all seven features; predominantly team-controlled or company-owned governance; single-chain deployment common.

**Emerging** (approximately 25 per cent): moderate user bases but low financial metrics; positive TVL and user counts above minimum thresholds; below-median market cap and volume. Several gaming protocols fall here, reflecting the high user-to-value gap documented in §4.5.2.

**Growing** (approximately 23 per cent): above-median user growth, improving governance scores, and meaningful though not top-tier financial metrics; multi-chain deployment common.

**Leading** (approximately 22 per cent): market cap, TVL, and volume all above the 75th percentile; highest median governance scores of any cluster; nearly all multi-chain. This cluster is dominated by established DeFi protocols.

These cluster typologies apply to the full 855-DApp dataset and are presented here as a complementary structural characterisation. Primary analytical findings throughout this chapter derive from the strict sample (N=68) unless otherwise noted.

### 4.8.3 Sector × Governance Co-Structure in Cohorts

The cohort analysis reveals systematic co-structure between sector membership and governance characteristics. DeFi DApps — concentrated in the exchanges :: DEX and defi :: Lending cohorts — exhibit the highest median governance scores and the highest prevalence of on-chain and community governance types. Gaming DApps, spanning games :: NFT Gaming, games :: NFT marketplace, and games :: Payments/RWA cohorts, cluster in the lower governance-score quadrants with predominantly team-controlled or company-owned structures. Social DApps (social :: Social Network, social :: SocialFi) are too few in the strict sample (two DApps each) to support within-category generalisations.

This sector–governance co-structure is consistent with the positive governance–performance correlation reported in §4.3.4: DeFi protocols operating in a competitive, financially sophisticated market face stronger institutional pressure to formalise governance, while gaming DApps competing on product and entertainment value retain more centralised structures.

---

## 4.9 Anomalies, Contradictions, and Challenges to the DApp Narrative

The preceding sections characterise the DApp landscape through systematic cross-sectional lenses. This section catalogues four categories of structural anomaly that emerge from the dataset and resist easy explanation within the dominant framings of DApp governance and market efficiency. Each anomaly is quantified, illustrated with representative examples, and cross-referenced to the interpretive discussion in Chapter 5. Together, they constitute an empirical challenge to four simplifying narratives — that governance tokens enable community control, that venture capital predicts market success, that user scale signals economic value, and that TVL is a reliable proxy for protocol importance — that pervade how the DApp ecosystem is publicly assessed.

---

### 4.9.1 Governance Tokens Without Governance Authority

The first anomaly concerns the co-occurrence of governance token issuance with team-controlled governance processes. The dataset includes a `strange_governance_token_team_control` flag, identifying DApps that hold a token classified as a governance asset while the operational governance structure is coded `TEAM_CONTROLLED`. Two DApps in the strict eligible set meet this strict definition — both hold governance-type tokens yet retain all material decision-making authority within a founding team or core contributor group, without evidence of binding on-chain or off-chain community votes.

The pattern becomes more pronounced under a broader definitional lens. In the strict sample (N=68), four DApps operating Snapshot off-chain governance hold governance tokens (§4.7.3), a configuration in which token holders can register preferences but execution authority rests with a team-operated multisig or founding committee rather than with an autonomous on-chain process. Beyond those, one DApp in the CENTRALIZED decentralisation tier holds on-chain token governance as its stated mechanism while remaining operationally centralised (ANO-GOV-03; prevalence: 1.47 per cent of the strict sample) — a configuration typically attributable to upgradeability keys, time-limited multisig overrides, or governance proposals authored and passed by team-controlled wallets without meaningful external participation.

These cases represent a structural decoupling of token design from governance authority. The presence of a governance token does not transfer decision-making power to token holders if proposal thresholds, voting quorums, or execution keys remain team-controlled. In such configurations, the governance token functions primarily as a capital formation instrument — attracting investment and conferring nominal legitimacy — rather than as an effective community governance mechanism. Star Atlas illustrates the ambiguity: its POLIS ve-model and claimed on-chain execution signal formal governance architecture, yet research annotations document team-led execution of game-economy decisions and a retained foundation coordination role. The broader eligible population of 834 DApps would likely surface a materially larger cohort under a permissive screen that included Snapshot-governed DApps with concentrated team token holdings.

This anomaly is examined interpretively in §5.3 (Labelling Versus Mechanics, DIS-02), where the gap between governance token design and governance authority is situated within the broader decentralisation paradox and its implications for regulatory framing are assessed.

---

### 4.9.2 Unfunded DApps Outperforming Venture-Backed Peers

The second anomaly challenges the assumption that venture capital backing predicts long-term market performance. Among the strict eligible sample (N=68), 13 DApps raised documented venture capital. The median return on investment for those protocols — calculated as current market capitalisation divided by total capital raised — is 0.11×, meaning the median funded DApp in the strict sample is valued at approximately one-tenth of the aggregate investment made in it. At the same time, 29.4 per cent of the strict sample's unfunded DApps — approximately 20 protocols (ANO-MKT-03) — achieve market capitalisations that exceed the median funded DApp in the same universe.

Across the broader 855-DApp dataset, $14.3 billion in documented capital was raised by 38 DApps; despite this concentrated investment, capital raised correlates only weakly with subsequent market performance. The directional relationship between capital raised and market capitalisation for funded DApps in the strict sample is negative — indicating that higher-funded projects are not systematically associated with proportionately higher market valuations at the time of data capture.

This pattern is consistent across the loose universe, where the broad unfunded-outperformance dynamic holds even as the composition of the funded and unfunded cohorts changes. Several mechanisms are candidates: (1) selection timing, whereby VC capital entered the ecosystem during elevated speculative periods, compressing subsequent return multiples as prices reverted; (2) the structural open-source dynamics of DApps, which reduce the competitive moats that make institutional backing valuable in traditional startups — if any developer can fork the protocol, the technical exclusivity that justifies a high entry valuation erodes quickly; and (3) community-driven distribution paths that deliver user acquisition independently of the venture networks that typically provide distribution advantages in enterprise software.

The anomaly does not imply that capital is without value in DApp development. Security audits, engineering hiring, and regulatory navigation all benefit from liquidity. What the data challenge is the stronger claim that capital raised serves as a reliable predictor of long-term market performance. This finding is developed interpretively in §5.7 (Funding Efficiency, DIS-06), where three competing causal mechanisms are assessed and the implications for DApp builders are considered.

---

### 4.9.3 High-User DApps with Zero Measurable TVL

The third anomaly concerns the decoupling of user scale from economic substance, as measured by Total Value Locked. Thirty-three DApps in the eligible population of 834 are flagged under `strange_centralized_high_users` — identifying protocols with above-threshold active user counts combined with centralised governance classifications. Within this group, several of the most-used protocols by active wallet count report effectively zero TVL, a combination that directly contradicts the implicit model in which user scale predicts capital deployment.

Representative cases from the strict and adjacent samples illustrate the pattern:

- **Hot Spring — The Cozy World** (2,924,351 active users; TVL: not reported; volume: $0): an AI-native gaming application operating under HYBRID governance. User activity generates token distributions rather than on-chain liquidity; the protocol's economic throughput is not captured by DeFiLlama's TVL methodology.
- **Alaya AI** (1,869,774 active users; TVL: not reported; volume: $0): a data-labelling protocol using reward tokens for task completion. Economic value is generated off-chain through data sales and captured by the protocol operator, with no on-chain TVL.
- **Dmail Network** (2,088,315 active users; volume: $13,700; TVL: not reported): a decentralised messaging protocol under TEAM_CONTROLLED governance, with near-zero financial throughput despite a user base larger than many established DeFi protocols.
- **FishWar** (560,738 active users; market cap: $0.3M; TVL: not reported): a gaming protocol distributing reward tokens under team-controlled governance with claimed governance voting but no evidence of binding DAO execution.

Across the DePIN sector (N=29, loose universe), 4.9 million collective active users generate only $8.6 million in total volume — an average of $1.74 per user — and negligible TVL. Within the AI sector (N=67, loose universe), the four most-used DApps by wallet count (Hot Spring, Alaya AI, OpenPad AI, and Sleepless AI) report combined volume of approximately zero (ANO-AI-01, §4.6.3). Neither pattern represents operational failure within the reward-economy models of these protocols; both are structurally expected given business models that distribute token rewards rather than intermediate financial transactions.

What makes the pattern anomalous is the category error it introduces when these protocols are evaluated against DeFi-calibrated metrics. A protocol with two million active users and zero TVL cannot be meaningfully ranked against a DeFi protocol with 50,000 users and $5 billion TVL using a composite metric that aggregates both dimensions. The two measurements index different economic logics, and their aggregation produces a distorted picture of relative importance in the DApp ecosystem. This methodological implication is developed in §5.5 (The Engagement Gap, DIS-04) and acknowledged explicitly in the limitations framework of §5.10.

---

### 4.9.4 Extreme TVL Leverage Cases

The fourth anomaly concerns protocols in which TVL substantially exceeds the token market capitalisation — what this study terms the TVL leverage phenomenon. In the strict sample (N=68), 8.82 per cent of DApps (six protocols, ANO-MKT-02) exhibit TVL that materially exceeds their token market capitalisation. The most pronounced cases are:

- **Morpho** (TVL approximately $187.5 billion; MCap materially lower; implied TVL/MCap approximately 3,437×): a modular DeFi lending protocol serving as infrastructure for other protocols' liquidity. TVL accumulates through recursive collateral loops where depositors use Morpho positions as collateral in secondary markets; the aggregate locked value therefore includes collateral committed by protocols building on Morpho, not only by end-users directly.
- **EigenLayer** (large TVL from restaked ETH; MCap substantially lower): a restaking protocol in which ETH holders commit already-staked assets to additional security commitments, effectively enrolling existing security collateral in an additional system. DeFiLlama's TVL methodology counts the committed ETH as locked, producing TVL that substantially exceeds the protocol's token market capitalisation.
- **LIDO** (TVL from staked ETH; MCap representing governance and fee rights over a fraction of staking yield): the dominant liquid staking protocol, where user deposits generate TVL through the staking mechanism while LDO token holders retain governance and fee-accrual rights proportional to the protocol's yield margin rather than the full deposited value.
- **Ethena** (TVL: $14.2 billion; MCap: $1.8 billion; TVL/MCap ≈ 7.8×): a synthetic dollar protocol whose sUSDe deposits are backed by staked ETH and short perpetual futures positions. TVL represents depositor liabilities that Ethena services, not protocol equity; the ENA token captures governance and a share of the basis-trade yield, not ownership of the deposited collateral.
- **KernelDAO** and **Pendle** exhibit moderate TVL/MCap inversions consistent with infrastructure and yield-market roles where fee capture is calibrated on a small fraction of managed value.

Three distinct structural mechanisms produce the TVL leverage phenomenon. The first is *recursive collateral looping*: infrastructure-layer protocols accumulate TVL through other protocols' use of their facilities, not through direct deposits by retail or institutional end-users. The second is *staking and restaking economics*: liquid staking and restaking protocols capture committed ETH as TVL under DeFiLlama's methodology, producing figures that reflect security commitments rather than traditional financial lock-up. The third is *liability-side TVL*: in synthetic asset protocols, TVL represents user deposits backing a synthetic liability rather than protocol equity; the protocol's equity interest is the fee on the spread between yield components, not ownership of the deposited collateral.

The analytical consequence is that TVL, like user count, is not a single-dimensional measure of economic weight. A protocol with TVL of $187 billion and MCap of tens of millions is not necessarily undervalued; it may instead reflect a business model in which the protocol captures a small fee percentage on managed value, and market capitalisation prices the present value of those fees rather than the face value of managed assets. Practitioners and researchers who use TVL as an unmodified proxy for protocol importance will systematically overstate the economic significance of infrastructure protocols relative to application-layer protocols where TVL/MCap ratios are more moderate.

Note also the related but directionally inverse case documented in §4.6.4 (ANO-RWA-02): Maple's 30-day volume ($34.3 billion) exceeds its TVL ($2.6 billion) by approximately 13.1×, indicating capital velocity — the repeated recycling of institutional capital through short-tenor lending cycles — rather than the passive accumulation that TVL is conventionally taken to represent. TVL leverage and TVL velocity are therefore twin distortions, pulling in opposite directions relative to the naive interpretation of the TVL metric.

This anomaly reinforces the broader argument developed in §5.4 (Concentration Mirrors Traditional Technology, DIS-03) that headline metrics in the DApp ecosystem require sector-aware and model-aware interpretation.

---

### 4.9.5 Synthesis: Challenges to the DApp Narrative

The four anomalies documented in this section share a common structure: each exposes a divergence between a metric that the DApp ecosystem's dominant narrative treats as a reliable signal and the underlying economic or governance reality that metric purports to index.

**Table 4.19 — Summary of anomaly categories, prevalence, and cross-references**

| Anomaly category | Flag / identifier | N DApps affected | Cross-reference |
|------------------|-------------------|:----------------:|:----------------|
| Governance token with team-controlled governance | `strange_governance_token_team_control` | 2 (strict definition); broader under inclusive screen | §5.3 DIS-02 |
| Unfunded DApps outperforming funded peers | ANO-MKT-03 | ~20 (29.4% of strict sample, N=68) | §5.7 DIS-06 |
| High-user / zero TVL | `strange_centralized_high_users` | 33 (loose eligible, N=834) | §5.5 DIS-04 |
| Extreme TVL leverage (TVL >> MCap) | ANO-MKT-02 | 6 (8.82% of strict sample, N=68) | §5.4 DIS-03 |

*Source: `docs/analytics/latest/anomalies.md`, `docs/analytics/merged/anomalies.md`, and strict-sample analysis. DApp counts refer to the strict sample (N=68) unless otherwise noted.*

Together, these anomalies constitute an empirical case for methodological caution in DApp research and practice. No single metric — governance label, token type, funding status, user count, or TVL — should be treated as a stand-alone indicator of DApp quality, governance authenticity, or economic significance. The interpretive weight given to any metric depends on the sector, business model, and revenue architecture of the DApp in question. This observation motivates the multi-dimensional evaluation framework proposed in §5.9 (Implications for Theory and Practice) and underpins the limitations discussed in §5.10.

---

## 4.10 Cross-Sectional Summary

The results presented in this chapter address the thesis's three research questions: (RQ1) the current governance and ownership structure of the DApp ecosystem; (RQ2) the alignment between governance labels and observed economic structure; and (RQ3) sector-level differences characterising the ecosystem. The findings are summarised below.

**RQ1 — Governance structure.** The DApp ecosystem is predominantly centrally governed at the application layer. In the strict high-signal sample (N=68), 86.8 per cent of DApps are not fully decentralised; 52.9 per cent are company-owned and 26.5 per cent are team-controlled. Governance token issuance (25–26 per cent of the strict sample) is concentrated in on-chain governance regimes but also appears in off-chain and hybrid contexts, indicating partial decoupling of token design from governance authority. These findings respond directly to RQ1 by establishing that the application-layer governance reality diverges substantially from the blockchain infrastructure's decentralisation properties.

**RQ2 — Governance alignment and economic concentration.** The strict universe simultaneously exhibits better governance quality and higher market concentration than the loose universe — a combination that directly addresses RQ2. The top-10 market cap share is 80.5 per cent in the strict sample versus 57.5 per cent in the loose universe, while the multi-chain deployment rate doubles. The 1.3× market cap premium for multi-chain DApps (full dataset, N=855), the positive governance–performance correlation (r=0.38), and the unfunded-outperformance anomaly (29.4 per cent of strict DApps) all suggest that structural features of the ecosystem — governance, chain strategy, capital structure — correlate with market outcomes in non-trivial ways. However, the cross-sectional design cannot establish causal direction.

**RQ3 — Sector-level differentiation.** The DeFi–gaming divide is large enough to render ecosystem-wide averages analytically misleading. DeFi DApps dominate the strict sample in volume ($299.1 billion), market capitalisation, and governance quality; gaming DApps dominate in user count (12.7 million active wallets in the strict sample) but generate orders-of-magnitude less financial throughput per user. Any evaluation of DApp performance or ecosystem health must account for this sectoral heterogeneity — a point that motivates the sector-disaggregated analysis throughout Chapter 5.
