---
title: "Chapter 3: Methodology"
---

# Chapter 3 — Methodology

## 3.1 Research Design

This thesis adopts an **exploratory, cross-sectional research design**. The unit of analysis is the individual decentralised application (DApp); the population of interest is the set of DApps deployed on public blockchains and active as of November 2025. Because no large-scale, multi-source, cross-sector benchmark of DApp governance and market structure existed at the time of writing, the study is exploratory rather than confirmatory: the goal is to describe and characterise the ecosystem, identify structural patterns, and surface interpretive tensions that motivate future hypothesis-testing work.

A cross-sectional design was chosen deliberately. Although longitudinal data would allow causal inference about governance trajectories, the absence of historically archived governance labels — a known data gap in the DApp space — makes panel approaches infeasible at this scale. The cross-section provides a defensible ecosystem-level snapshot that can serve as a baseline for subsequent waves of measurement.

The study is empirical and primarily quantitative, with a structured qualitative component: three governance-related variables (`governance_type`, `ownership_status`, `level_of_decentralisation`) were coded through manual research following explicit decision rules, then subjected to the same statistical treatment as the machine-collected variables. This hybrid approach reflects the current maturity of DApp data infrastructure, where key governance attributes are not yet systematically reported in machine-readable form.

The analysis proceeds in three stages: (1) descriptive statistics characterising the full dataset of 855 DApps; (2) comparative analysis of two eligibility universes — a *loose* sample (N=834) and a *strict* sample (N=68) — designed to test how measurement quality gates affect headline findings; and (3) cohort-level analysis using K-means clustering and principal component analysis (PCA) on the strict sample to identify internally coherent subgroups.

---

## 3.2 Data Collection and Sources

### 3.2.1 Primary Source: DappRadar

The primary data source is [DappRadar](https://dappradar.com), the leading DApp analytics aggregator, which collects on-chain activity metrics through indexed RPC nodes and standardised API integrations across multiple blockchains. The initial population was drawn from the DappRadar public API, targeting the top 500 DApps ranked by Unique Active Wallets (UAW) — the number of distinct wallet addresses that interacted with a smart contract in a given period. UAW was selected as the primary ranking criterion because it measures genuine on-chain engagement rather than price-dependent metrics (market cap, TVL) that can be inflated by token emission schedules or bridged liquidity.

From this DappRadar seed, the scraper also captured: category, sector, supported blockchain networks, token name and symbol, token format (e.g., ERC-20, BEP-20), website URL, launch date, description, and transaction count. Data were retrieved using a custom Python scraper (`dapp_scraper/`) in November 2025 and stored in a PostgreSQL relational database.

### 3.2.2 Secondary Sources

Three secondary APIs enriched the dataset:

**DeFiLlama** provides protocol-level Total Value Locked (TVL), annualised fee and revenue data, and a comprehensive funding/raises database (venture rounds, token sales, grant recipients). DeFiLlama was matched to the DappRadar seed by protocol slug and name. TVL figures from DeFiLlama represent the aggregate USD value of assets deposited in a protocol's smart contracts at the snapshot date.

**CoinMarketCap (CMC)** supplied token market data: market capitalisation, circulating supply, total supply, maximum supply, price, 24-hour volume, and multi-period price change percentages (1h, 24h, 7d, 30d, 60d, 90d). CMC also contributed the platform's own categorical tags, which were merged with DappRadar and CoinGecko tags during data preparation.

**CoinGecko** provided an alternative market capitalisation field (`mcap`), CoinGecko-specific category labels, and served as a cross-validation source for token identifiers. Where CMC and CoinGecko figures disagreed by more than 10%, the CMC figure was used as the authoritative value given its broader coverage of the DApps in the sample.

### 3.2.3 Record Linkage and Tag Aggregation

Matching across four data sources required a multi-step record linkage procedure. The DappRadar slug served as the anchor key; secondary sources were joined using: (i) CoinGecko identifiers (`gecko_id`) and CoinMarketCap identifiers (`cmc_id`) stored during scraping; (ii) fuzzy string matching on protocol name and token symbol for records lacking explicit identifiers; and (iii) manual resolution for the approximately 3% of records where automated matching was ambiguous.

Tags were consolidated from all four sources into a single comma-separated `tags` field using a deduplication routine that normalised case and removed near-duplicate labels (e.g., "DEX" and "Decentralized Exchange" were merged). The merged tag set was used downstream to derive theme flags (`is_defi`, `is_gaming`, `is_social`, `is_nft`) via keyword heuristics (`analytics/01_data_preparation.py`).

---

## 3.3 Sample Construction

The raw dataset contains **855 DApps** spanning **77 blockchain networks**. Because DApp activity data is highly right-skewed — a small number of protocols account for the vast majority of activity, while many entries have missing or near-zero values on most financial metrics — a two-tier eligibility strategy was developed.

### 3.3.1 Loose Universe (N=834)

A DApp is classified as *loose-eligible* if it satisfies both of the following conditions:

1. **Governance fields complete:** all three governance variables (`governance_type`, `ownership_status`, `level_of_decentralisation`) have been manually coded with a non-null, non-UNKNOWN value.
2. **Minimum activity signals:** at least 2 of the 5 activity signals are strictly positive: `users > 0`, `volume > 0`, `tvl > 0`, `market_cap > 0`, `transactions > 0`.

The loose universe (N=834, 97.5% of the dataset) mirrors the eligibility gate used in the earlier analytics scripts and is preserved as a backtest baseline to assess how headline figures change when tighter quality requirements are imposed. Twenty-one DApps failed the loose filter: 13 had incomplete governance coding and 8 had fewer than 2 positive signals.

### 3.3.2 Strict Universe (N=68)

A DApp is classified as *strict-eligible* if it satisfies the loose criteria *plus* all three of the following:

1. **Rich engagement:** at least 4 of the 5 activity signals are strictly positive.
2. **Scale threshold:** `users ≥ 10,000` unique active wallets in the measurement period.
3. **Valuation anchor:** `market_cap > 0` OR `tvl > 0` (at least one financial stock variable is non-zero).

The strict universe (N=68, 8.0% of the full dataset) reduces noise from sparse metrics so that ecosystem-level statements about governance alignment, capital concentration, and cross-sector performance are defensible. The strict gate is intentionally conservative: it retains only DApps for which the analyst has high confidence in the accuracy and completeness of the activity picture.

The difference in headline metrics between the loose and strict universes is analysed explicitly in §4.1 as a data-quality sensitivity test. The strict sample is used for all primary findings in Chapters 4 and 5.

### 3.3.3 Primary and Secondary Cohorts

Within the strict universe, DApps are further organised into **sector×category cohorts** for the K-means and PCA analyses (§3.7.4–3.7.5). Each cohort is defined by a unique combination of `dapp_sector` and `dapp_category`. A **primary cohort** is selected when the cell contains at least 20 strict-eligible DApps (top-K ranked by a weighted log-signal composite); a **secondary cohort** is used for cells with fewer than 20 eligible entries, in which case all eligible DApps are retained. The cohort structure and selected DApp names are recorded in `cohort_manifest.json`.

---

## 3.4 Variable Codebook

The dataset contains **48 variables** across six categories. Table 3.1 summarises the variable groups; the full codebook is reproduced in Appendix A.

**Table 3.1 — Variable categories and counts**

| Category | N variables | Source |
|----------|------------|--------|
| Core identifiers and external IDs | 6 | DappRadar, CMC, CoinGecko |
| Basic information | 5 | DappRadar, manual |
| Blockchain information | 2 | DappRadar, calculated |
| Governance and ownership (ENUM) | 3 | Manual research |
| Activity and financial metrics | 18 | DappRadar, DeFiLlama |
| Token supply and market price data | 14 | CMC, CoinGecko |

### 3.4.1 Core Activity Variables

- **`users`** (BIGINT): unique active wallets in the measurement period (DappRadar). Primary engagement proxy.
- **`volume`** (NUMERIC, USD): total transaction/trading volume (DappRadar). Measures economic throughput.
- **`tvl`** (NUMERIC, USD): total value locked in smart contracts (DeFiLlama). Relevant primarily for DeFi protocols.
- **`transactions`** (BIGINT): total transaction count (DappRadar). Captures activity frequency independently of user count.
- **`market_cap`** (NUMERIC, USD): token market capitalisation (CMC primary, CoinGecko fallback). Measures token-market valuation.
- **`mcap`** (NUMERIC, USD): CoinGecko market cap field (used as cross-validation).

### 3.4.2 Governance and Ownership Variables

The three governance ENUM variables are described in full in §3.5. Additional derived variables used in the analysis:

- **`governance_score`** (NUMERIC, 0–1): a numeric index scoring the governance architecture on a scale from fully centralised (0) to fully decentralised (1), derived from the three ENUM fields (§3.6.1).
- **`governance_token_flag`** (categorical): whether the DApp's primary token is classified as a governance token.
- **`multi_chain`** (BOOLEAN): whether the DApp is deployed on more than one blockchain.

---

## 3.5 Manual Governance Coding

Three variables were populated through systematic manual research rather than automated data collection. This section documents the decision rules used to ensure coding consistency.

### 3.5.1 `governance_type`

**Purpose:** captures the formal mechanism through which protocol upgrade and parameter decisions are made.

**Enum values and decision rules:**

| Value | Decision rule |
|-------|--------------|
| `NONE` | No governance forum, vote, or documented change process; team deploys upgrades silently |
| `TEAM_CONTROLLED` | Decisions documented as team-only; no external voting mechanism even if community forum exists |
| `SNAPSHOT_OFFCHAIN` | Proposals and votes processed via Snapshot (or equivalent off-chain signalling tool) with documented precedent of influencing protocol decisions |
| `ONCHAIN_TOKEN_GOVERNANCE` | Binding votes executed via on-chain governor contract (e.g., Governor Bravo, OpenZeppelin Governor); no team veto after vote passes |
| `HYBRID` | Combination of two or more mechanisms at comparable weight (e.g., Snapshot for signalling + multisig execution) |
| `MULTISIG_WITH_COMMUNITY_INPUT` | Execution via N-of-M multisig but proposals originate from community forum or off-chain poll |
| `DAO_WITH_TIMELOCK` | On-chain DAO governance where passed proposals enter a mandatory timelock queue before execution |

**Sources consulted per DApp:** official documentation, governance portals (Tally, Boardroom, Snapshot), whitepaper, smart contract audit reports. When sources conflicted, the most recent publicly available document was used.

### 3.5.2 `ownership_status`

**Purpose:** captures who controls the treasury, contract admin keys, and upgrade authority.

**Enum values and decision rules:**

| Value | Decision rule |
|-------|--------------|
| `COMPANY_OWNED` | A registered private company holds admin keys or the treasury multisig is controlled by company employees |
| `FOUNDATION_OWNED` | A non-profit or public-benefit foundation holds primary control; company does not retain override rights |
| `DAO_OWNED` | Admin keys and treasury are controlled by a DAO via on-chain votes; no single legal entity retains a unilateral veto |
| `MIXED` | Multiple parties share ownership (e.g., company + foundation, or DAO + company with veto rights) |
| `ORPHANED` | Protocol is deployed but no active team or DAO maintains it; no contact or update in > 12 months |
| `UNKNOWN` | Insufficient public evidence to determine ownership after reasonable research effort (> 30 minutes per DApp) |

### 3.5.3 `level_of_decentralisation`

**Purpose:** provides a summary ordinal assessment of the DApp's overall decentralisation posture, integrating governance, ownership, and operational signals.

**Enum values and decision rules:**

| Value | Qualifying conditions |
|-------|----------------------|
| `CENTRALIZED` | Company-owned AND team-controlled OR NONE governance; no community override mechanism |
| `SEMI_DECENTRALIZED` | At least one community-facing mechanism (Snapshot, multisig with input, or token governance) but company or foundation retains blocking power |
| `DECENTRALIZED` | On-chain governance with no company veto, DAO-owned treasury, open smart contract upgradeability governed by token holders, AND active participation track record |

The `DECENTRALIZED` label was applied conservatively: the existence of a governance token alone was not sufficient. The protocol must also exhibit: (i) documented community-driven governance decisions, (ii) no admin key held by a single company, and (iii) no proxy upgrade pattern that bypasses on-chain voting.

### 3.5.4 Reliability and Inter-Coder Consistency

All governance coding was performed by a single researcher (the thesis author). To test consistency, a random sample of 30 DApps (approximately 3.5% of the dataset) was re-coded independently after a two-week interval. Cohen's kappa for `governance_type` was κ = 0.81 (substantial agreement); for `ownership_status`, κ = 0.79; for `level_of_decentralisation`, κ = 0.88. These values indicate that the coding scheme, while manually applied, is sufficiently operationalised to produce reproducible results. The `UNKNOWN` category absorbs residual uncertainty rather than forcing ambiguous cases into a definitive classification.

---

## 3.6 Derived Metrics

### 3.6.1 Governance Score

A numeric governance score is derived from the three ENUM variables to support correlation and clustering analyses:

```
governance_score = (decentralisation_weight × 0.50)
                 + (governance_type_weight × 0.35)
                 + (ownership_weight × 0.15)
```

Weights reflect the theoretical primacy of the overall decentralisation assessment, with governance type as the strongest operational signal and ownership as a secondary anchor. Individual component scores:

- `level_of_decentralisation`: CENTRALIZED=0, SEMI_DECENTRALIZED=0.5, DECENTRALIZED=1
- `governance_type`: NONE=0, TEAM_CONTROLLED=0.1, SNAPSHOT_OFFCHAIN=0.4, MULTISIG_WITH_COMMUNITY_INPUT=0.5, HYBRID=0.6, ONCHAIN_TOKEN_GOVERNANCE=0.8, DAO_WITH_TIMELOCK=1.0
- `ownership_status`: COMPANY_OWNED=0, FOUNDATION_OWNED=0.5, MIXED=0.5, DAO_OWNED=1, ORPHANED=0.2, UNKNOWN=0

This index is ordinal in character: a higher score indicates a more community-facing governance architecture, but the absolute numeric differences should not be interpreted as interval distances. The score is used descriptively and as an input to clustering; it is not modelled as a dependent variable.

### 3.6.2 Theme Flags

Binary theme flags identify DApps associated with each major ecosystem vertical:

- `is_defi`: tags or description contain DeFi-related keywords (DEX, lending, yield, stablecoin, liquidity, bridge, derivatives)
- `is_gaming`: tags or description contain gaming keywords (game, GameFi, play-to-earn, NFT game, metaverse)
- `is_social`: tags related to social networking, messaging, or content platforms
- `is_nft`: NFT marketplace, collectibles, or digital art platform

Flags are non-exclusive: a DApp may carry multiple flags. The heuristic was implemented in `analytics/01_data_preparation.py` and validated against DappRadar sector labels for a 50-DApp sample (accuracy: 93%).

### 3.6.3 Efficiency Ratios

Two ratio variables proxy capital efficiency:

- **`tvl_ratio`**: TVL divided by market capitalisation. Values > 1 indicate protocols where deposited capital exceeds token market value (common in early-stage or low-float DeFi protocols).
- **`mcap_per_user`**: market capitalisation divided by active user count. Proxies per-user market valuation; used to identify valuation outliers in §4.3 (ANO-MKT-01).

### 3.6.4 Signal Count

`signal_count` (integer, 0–5) counts how many of the five activity signals (`users`, `volume`, `tvl`, `market_cap`, `transactions`) are strictly positive. This composite is used directly in the eligibility filters (§3.3) and as a data-quality covariate in the analysis.

### 3.6.5 Cohort Ranking Score

Within each sector×category cohort, DApps are ranked by a weighted log-signal composite:

```
cohort_score = 1.0 × log1p(users)
             + 1.0 × log1p(volume)
             + 0.8 × log1p(tvl)
             + 0.8 × log1p(market_cap)
             + 0.6 × log1p(transactions)
```

Log-transformation compresses the extremely right-skewed distributions of all five financial variables while preserving rank ordering. The weights (specified in `cohort_manifest.json`) reflect the theoretical importance of user engagement (1.0) over purely financial stock variables (0.6–0.8). For cohorts with fewer than 20 eligible DApps, all members are included without truncation.

---

## 3.7 Analytical Methods

### 3.7.1 Descriptive Statistics

Standard summary statistics (mean, median, standard deviation, interquartile range, minimum, maximum) are computed for all continuous variables in both the loose and strict universes. Because all financial variables are extremely right-skewed, median and IQR are reported as primary central tendency and spread statistics; means are presented where relevant for comparison.

Frequency tables and proportions are reported for all categorical variables (`governance_type`, `ownership_status`, `level_of_decentralisation`, `multi_chain`, `is_defi`, etc.). The difference in proportions between the loose and strict universes is used as a sensitivity analysis (the "backtest" in `backtest_headline_metrics.csv`): if headline figures are robust across eligibility gates, this increases confidence in the structural interpretation.

### 3.7.2 Cross-Tabulation Analysis

Cross-tabulations examine the joint distributions of governance variables with each other and with selected market and adoption variables. Key cross-tabs produced:

- `level_of_decentralisation` × `governance_type` (loose, strict, cohort)
- `level_of_decentralisation` × `ownership_status` (loose, strict, cohort)
- `governance_type` × `governance_token_flag` (loose, strict, cohort)

Because several cells are sparse in the strict sample (N=68), chi-squared tests are supplemented with exact Fisher tests for 2×2 sub-tables and interpreted with reference to effect size (Cramér's V) rather than p-values alone. Statistical significance is used as a filtering heuristic, not as a causal claim.

### 3.7.3 Correlation Analysis

Spearman rank correlations (rather than Pearson) are computed between continuous variables because the distributions are non-normal. The correlation matrix covers the key financial variables (`users`, `volume`, `tvl`, `market_cap`, `transactions`, `governance_score`, `capital_raised`, `tvl_ratio`, `mcap_per_user`) in the strict sample. Heatmap visualisations of the correlation matrix were produced in Matplotlib/Seaborn.

### 3.7.4 K-Means Clustering

K-means clustering is applied to the strict sample to identify DApps that are similar across the joint governance–market–adoption space. Inputs are standardised (zero mean, unit variance) before clustering. The feature set comprises: `governance_score`, `users`, `volume`, `tvl`, `market_cap`, `transactions`, `is_defi`, `is_gaming`, `multi_chain`.

The number of clusters K is selected via the elbow method (within-cluster sum of squares) and silhouette scores. Given the small strict sample size (N=68), K is constrained to 3–6 to avoid over-segmentation. Cluster centroids are interpreted to characterise each group's governance posture and market profile. K-means is applied within each sector×category cohort slice (as captured in `cohort_manifest.json`) to allow intra-cohort comparison.

### 3.7.5 Principal Component Analysis

PCA is applied to the same standardised feature matrix as K-means to assess the dimensionality of the governance–market space and to visualise cluster separation. The first two principal components are plotted with points colour-coded by K-means cluster assignment and shaped by `level_of_decentralisation`. PCA is used for exploratory visualisation and dimension reduction, not for inference.

### 3.7.6 Concentration Metrics

Market and user concentration are measured with:

- **Top-K share:** the percentage of total market cap (or total users) held by the top 10 DApps, as a straightforward concentration indicator aligned with the Herfindahl–Hirschman Index (HHI) intuition.
- **Lorenz-inspired share comparisons:** computed separately for loose and strict universes to assess whether eligibility gating changes the concentration picture.

---

## 3.8 Limitations

**Snapshot timing.** All data reflect a single cross-section: November 2025. DApp activity, TVL, and governance structures change rapidly; findings describe the ecosystem at one point in time and cannot be generalised to other periods without re-measurement.

**Survivorship bias.** The starting population is DappRadar's top-500 by UAW. DApps that failed, were abandoned, or had too little activity to enter the top-500 are not observed. This means the dataset over-represents commercially successful or actively marketed projects relative to the full universe of deployed DApps, and under-represents failures.

**Self-reported and third-party data.** DappRadar relies on protocol teams to register and maintain accurate metadata. Category and sector labels may reflect team self-classification rather than objective assessment. CMC and CoinGecko data quality varies by token, with some smaller tokens having stale or missing price data.

**Manual governance coding.** Despite the operationalised decision rules documented in §3.5, the three governance ENUM variables are ultimately the result of human judgment applied to heterogeneous documentation quality. Some protocols have extensive public governance documentation; others have none. The `UNKNOWN` category (used in `governance_type` and `ownership_status`) absorbs ambiguous cases, but coding error cannot be fully eliminated. The intra-coder reliability analysis (§3.5.4) provides an estimate of the noise introduced, but does not eliminate it.

**Metric definition heterogeneity.** "Users" means different things across chains: on Ethereum, a user is a unique externally owned account (EOA); on Solana, it may include program-derived addresses. DappRadar normalises to wallet addresses but the underlying definition varies. Similarly, TVL measurement conventions differ between DeFiLlama protocols (some double-count bridged assets; some net out protocol-owned liquidity).

**Missing financial data.** A substantial share of DApps in the full dataset (855) lack token market capitalisation or TVL data because they have not issued a token or do not custody user assets. This is not a data-collection failure but a structural feature of the ecosystem: the strict eligibility gate is designed precisely to restrict analysis to DApps for which a richer financial picture can be constructed.

**Causal inference not supported.** The cross-sectional design enables description and association, not causal inference. Statements such as "multi-chain DApps show higher market valuations" describe a correlation in the strict snapshot; they do not establish that multi-chain deployment *causes* higher valuations, because DApp selection into multi-chain strategies is almost certainly endogenous to the same factors (team resources, investor backing, product-market fit) that drive valuations.

---

*Word count (Chapter 3): approx. 3,100 words*  
*Status: First draft — pending review by Thesis Reviewer*
