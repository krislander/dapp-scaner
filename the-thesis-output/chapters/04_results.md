# Chapter 4 — Results

## 4.1 Descriptive Statistics of the Full Dataset

The full dataset comprises 855 decentralised applications (DApps) deployed across 77 distinct blockchain networks, collected in November 2025. Together, these applications report 90.9 million total active users, a combined token market capitalisation of approximately $14.9 billion, and Total Value Locked (TVL) of $115.7 billion. The dataset captures 48 variables per DApp (see Appendix A — *forward reference: variable codebook*), of which 33 contain at least partial coverage across the full sample; the remaining variables are financial or governance fields for which sparse or no data were available for a significant share of the population.

### 4.1.1 Dataset Coverage and Completeness

Coverage varies substantially by variable category. Token market data — market capitalisation, price, volume, and supply fields sourced from CoinMarketCap and CoinGecko — are available for the 50.2 per cent of DApps that operate a native token. The remaining 49.8 per cent either have no token or lacked a match in the token-data APIs at the time of collection. TVL, sourced from DeFiLlama, covers protocol-level locked value and is non-zero for approximately 38 per cent of the dataset; this figure reflects the subset of DApps with measurable on-chain liquidity pools rather than all DApps in the sample. Activity metrics — users, transactions, and volume — sourced from DappRadar are present for the full 855-DApp population but exhibit extreme right skew: the mean user count is pulled far above the median by a small number of very large protocols.

Governance fields (`governance_type`, `ownership_status`, `level_of_decentralisation`) were coded manually for all 855 entries following the decision rules described in §3.5 (*forward reference: governance coding rules*). Of these, 834 records received complete, non-UNKNOWN coding — the remaining 21 entries had insufficient publicly available information to assign definitive labels and were excluded from all subsequent analyses.

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

## 4.6 Token Analysis

### 4.6.1 Token Adoption Rate

Across the full 855-DApp dataset, 50.2 per cent of DApps operate a native token; the remaining 49.8 per cent either have no token or lacked a verifiable token match in the CoinMarketCap and CoinGecko APIs at the time of collection. Token adoption is substantially higher in DeFi-adjacent categories — where token design enables incentive alignment, liquidity mining, and governance participation — than in gaming and social DApps, where token integration is more varied in form and economic function.

Within the strict sample (N=68), six DApps (8.8 per cent) have no token, as recorded in the `token_type` field of the governance × token cross-tabulation (`crosstab_governance_token_strict.csv`).

### 4.6.2 Token Type Distribution in the Strict Sample

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

### 4.6.3 Governance Token Prevalence (INS-TOK-01)

Governance tokens are present in 17 DApps as classified by the `token_type` field (25.0 per cent of the strict sample). The governance-token flag analysis (INS-TOK-01) reports a governance token prevalence of 26.47 per cent, which reflects a slightly broader classification that includes tokens with hybrid governance and utility characteristics; the two figures bracket the effective range of governance token prevalence in the strict sample.

Governance tokens are concentrated in on-chain governance regimes: all 13 DApps with DAO-with-timelock or on-chain token governance hold governance tokens, accounting for 76.5 per cent of all governance tokens in the sample. The remaining four governance tokens appear in DApps operating Snapshot off-chain governance — indicating that some projects issue governance tokens while conducting voting off-chain rather than on-chain, potentially to reduce gas costs or simplify the voting interface.

The co-occurrence pattern between governance token issuance and governance architecture has an important implication: the presence of a governance token is a necessary but not sufficient condition for on-chain governance. Many utility and reward tokens coexist with community governance processes (particularly Snapshot-based voting), while some governance tokens coexist with team-controlled governance structures, suggesting that token design and operational governance authority are partially decoupled in practice. This decoupling is examined interpretively in §5.3.

---

## 4.7 Cohort Analysis

### 4.7.1 Sector × Category Cohort Structure

Within the strict universe (N=68), DApps are organised into sector × category cohorts using a composite signal-weighting scheme (`cohort_manifest.json`). The cohort selection algorithm assigns each DApp to a cell defined by its `dapp_sector` and `dapp_category`. Cells with at least 20 strict-eligible DApps are designated primary cohorts, from which a top-K subset is drawn by weighted log-signal composite; cells with fewer than 20 eligible entries are designated secondary cohorts and retain all eligible DApps.

The composite signal score weights the five core activity signals as follows: users (weight 1.0), volume (1.0), TVL (0.8), market cap (0.8), and transactions (0.6). Signals are log-transformed before weighting to reduce the influence of extreme outliers.

In practice, no sector × category cell in the strict universe reaches the 20-DApp threshold for primary cohort selection — the largest cell (exchanges :: DEX) contains 13 eligible DApps and the next largest (defi :: DEX) contains eight. Consequently, all cohorts in the strict universe are secondary cohorts, retaining all eligible DApps within each cell. This means the cohort analysis is in effect a sector × category decomposition of the strict sample rather than a filtered top-K selection.

**[Figure 4.13: Governance × ownership heatmap — primary cohort]**
*File: `figures/02_governance_heatmaps_cohort.png`*

**[Figure 4.14: Governance × token type heatmap — primary cohort]**
*File: `figures/02_governance_token_heatmap_cohort.png`*

**[Figure 4.15: Governance label distribution — primary cohort]**
*File: `figures/02_governance_distribution_cohort.png`*

### 4.7.2 Performance Clustering (K-means)

A complementary performance clustering analysis, applied to the full 855-DApp dataset using K-means (k=4, random\_state=42, n\_init=10), partitions DApps with complete performance data into four tiers based on seven features: log-transformed active users, market cap, TVL, volume, and transaction count, plus the composite governance score and a market maturity index (both entered without log transformation). All features are standardised using z-score normalisation before clustering. The four resulting clusters, as reported in the full-dataset analysis (`analytics/06_performance_analysis.py`), are characterised as follows:

**Struggling** (approximately 30 per cent of DApps with complete data): below-median performance on all seven features; predominantly team-controlled or company-owned governance; single-chain deployment common.

**Emerging** (approximately 25 per cent): moderate user bases but low financial metrics; positive TVL and user counts above minimum thresholds; below-median market cap and volume. Several gaming protocols fall here, reflecting the high user-to-value gap documented in §4.5.2.

**Growing** (approximately 23 per cent): above-median user growth, improving governance scores, and meaningful though not top-tier financial metrics; multi-chain deployment common.

**Leading** (approximately 22 per cent): market cap, TVL, and volume all above the 75th percentile; highest median governance scores of any cluster; nearly all multi-chain. This cluster is dominated by established DeFi protocols.

These cluster typologies apply to the full 855-DApp dataset and are presented here as a complementary structural characterisation. Primary analytical findings throughout this chapter derive from the strict sample (N=68) unless otherwise noted.

### 4.7.3 Sector × Governance Co-Structure in Cohorts

The cohort analysis reveals systematic co-structure between sector membership and governance characteristics. DeFi DApps — concentrated in the exchanges :: DEX and defi :: Lending cohorts — exhibit the highest median governance scores and the highest prevalence of on-chain and community governance types. Gaming DApps, spanning games :: NFT Gaming, games :: NFT marketplace, and games :: Payments/RWA cohorts, cluster in the lower governance-score quadrants with predominantly team-controlled or company-owned structures. Social DApps (social :: Social Network, social :: SocialFi) are too few in the strict sample (two DApps each) to support within-category generalisations.

This sector–governance co-structure is consistent with the positive governance–performance correlation reported in §4.3.4: DeFi protocols operating in a competitive, financially sophisticated market face stronger institutional pressure to formalise governance, while gaming DApps competing on product and entertainment value retain more centralised structures.

---

## 4.8 Cross-Sectional Summary

The results presented in this chapter address the thesis's three research questions: (RQ1) the current governance and ownership structure of the DApp ecosystem; (RQ2) the alignment between governance labels and observed economic structure; and (RQ3) sector-level differences characterising the ecosystem. The findings are summarised below.

**RQ1 — Governance structure.** The DApp ecosystem is predominantly centrally governed at the application layer. In the strict high-signal sample (N=68), 86.8 per cent of DApps are not fully decentralised; 52.9 per cent are company-owned and 26.5 per cent are team-controlled. Governance token issuance (25–26 per cent of the strict sample) is concentrated in on-chain governance regimes but also appears in off-chain and hybrid contexts, indicating partial decoupling of token design from governance authority. These findings respond directly to RQ1 by establishing that the application-layer governance reality diverges substantially from the blockchain infrastructure's decentralisation properties.

**RQ2 — Governance alignment and economic concentration.** The strict universe simultaneously exhibits better governance quality and higher market concentration than the loose universe — a combination that directly addresses RQ2. The top-10 market cap share is 80.5 per cent in the strict sample versus 57.5 per cent in the loose universe, while the multi-chain deployment rate doubles. The 1.3× market cap premium for multi-chain DApps (full dataset, N=855), the positive governance–performance correlation (r=0.38), and the unfunded-outperformance anomaly (29.4 per cent of strict DApps) all suggest that structural features of the ecosystem — governance, chain strategy, capital structure — correlate with market outcomes in non-trivial ways. However, the cross-sectional design cannot establish causal direction.

**RQ3 — Sector-level differentiation.** The DeFi–gaming divide is large enough to render ecosystem-wide averages analytically misleading. DeFi DApps dominate the strict sample in volume ($299.1 billion), market capitalisation, and governance quality; gaming DApps dominate in user count (12.7 million active wallets in the strict sample) but generate orders-of-magnitude less financial throughput per user. Any evaluation of DApp performance or ecosystem health must account for this sectoral heterogeneity — a point that motivates the sector-disaggregated analysis throughout Chapter 5.
