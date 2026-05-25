# Chapter Outline — MSc Thesis
## Decentralised Applications in Focus: Governance, Market Structure, and Adoption Patterns

**Institution:** Politecnico di Milano  
**Programme:** Master of Science — Digital Innovation Observatory, Blockchain  
**Total target word count:** 17,000–19,000 words (excluding references and appendices)  
**Dataset:** 855 DApps, 48 variables; strict sample N=68, loose sample N=834

---

## Document Map

| Chapter | Title | Target Words | Status |
|---------|-------|-------------|--------|
| Front Matter | Title, Dedication, Acknowledgements | — | — |
| Sommario | Abstract (Italian) | 300–400 | Draft needed |
| Abstract | Abstract (English) | 300–400 | Draft needed |
| 1 | Introduction | 1,500–2,000 | Draft needed |
| 2 | Literature Review | 3,500–4,500 | Draft needed |
| 3 | Methodology | 3,000–3,500 | **→ This heartbeat** |
| 4 | Results | 3,500–4,000 | Draft needed |
| 5 | Discussion | 2,500–3,000 | Draft needed |
| 6 | Conclusions | 1,000–1,500 | Draft needed |
| References | Bibliography | — | — |
| Appendix A | Variable Codebook | — | DATABASE_COLUMNS.md |
| Appendix B | Analytical Scripts | — | code repo |

---

## Chapter-by-Chapter Breakdown

---

### Front Matter

- **Title page** — PoliMi template: thesis title, candidate name, supervisor, co-supervisor, academic year 2024–2025
- **Dedication** — optional, ~50 words
- **Acknowledgements** — 200–300 words

---

### Sommario (Abstract — Italian) · 300–400 words

**Purpose:** PoliMi requirement; identical scope to the English abstract but written in Italian.

**Key points to cover:**
- Contesto: rapida crescita delle applicazioni decentralizzate (DApp) e domanda di evidence-based governance
- Obiettivo: analisi cross-sectional di 855 DApp su 77 blockchain per verificare se i label di governance corrispondono alla struttura economica
- Metodo: dataset multi-fonte (DappRadar/DeFiLlama/CMC/CoinGecko), campionamento per eligibility, K-means clustering, PCA
- Risultati chiave: 86.8% non è pienamente decentralizzato; top 10 detengono 80.5% della market cap
- Implicazioni: progettazione della governance, metriche di adozione, raccomandazioni policy

---

### Abstract (English) · 300–400 words

**Key points to cover:**
- Context: DApp ecosystem growth and governance accountability gap
- Gap: most studies focus on single protocols or narrow DeFi samples; few cross-sector, large-N analyses exist
- Research question: Do governance and ownership labels align with observed economic and adoption structure?
- Method: 855 DApps, multi-source dataset, exploratory cross-sectional analysis
- Key results: 13.2% fully decentralised in strict sample; 80.5% market cap in top 10; 70.6% multichain; DeFi/Gaming sector split
- Contribution: empirical benchmark across 77 blockchains; methodology for multi-source DApp measurement

---

### Chapter 1 — Introduction · 1,500–2,000 words

#### 1.1 Motivation and Context (400–500 words)
- Rise of DApps: from Bitcoin to permissionless smart contracts
- DeFi, GameFi, NFT, DAO tooling as distinct sectors within the same infrastructure layer
- The governance accountability gap: projects claim decentralisation; evidence is sparse

#### 1.2 Research Questions (200–300 words)
- RQ1: What is the current governance and ownership structure of the DApp ecosystem?
- RQ2: Does governance label align with observed economic concentration and adoption?
- RQ3: What sector-level differences characterise the ecosystem?

#### 1.3 Scope and Boundaries (300–400 words)
- 855 DApps from DappRadar top-500 UAW + manual additions, snapshot November 2025
- 77 blockchains included; EVM and non-EVM chains
- What is excluded: Layer-0/1 protocols, wallets, pure infrastructure, CEX

#### 1.4 Thesis Structure (200–300 words)
- Chapter map with one-sentence description of each chapter's contribution

**Tables/Figures in Chapter 1:** none (conceptual intro)

---

### Chapter 2 — Literature Review · 3,500–4,500 words

#### 2.1 Decentralised Applications: Definition and Taxonomy (600–800 words)
- Buterin's original vision; smart contract as self-executing agreement
- Sector taxonomy: DeFi, GameFi, NFT marketplaces, Social, Infrastructure
- Key distinction: protocol-layer vs application-layer decentralisation

**Cite:** Nakamoto 2008; Buterin 2014; Wood 2014; Chen et al. 2020

#### 2.2 Governance Mechanisms in Web3 (800–1,000 words)
- Off-chain (Snapshot) vs on-chain (Governor Bravo, Compound-style) governance
- Token-weighted voting: empirical evidence on participation rates
- Multisig and timelocks as trust-reduction mechanisms
- Progressive decentralisation model (Founder → DAO transition)

**Cite:** Barbereau et al. 2022; Tan et al. 2023; Freni et al. 2022; Aramonte et al. 2021; literature from the-thesis-output/Literature/

#### 2.3 Market Structure and Economic Concentration (700–900 words)
- Power-law distributions in DeFi TVL and market cap
- Winner-takes-most dynamics in open protocols
- Capital concentration vs permissionless entry paradox

**Cite:** Lommers et al. 2021; Schär 2021; relevant DeFi literature

#### 2.4 Adoption and Activity Metrics (600–800 words)
- Unique Active Wallets (UAW) as primary engagement proxy
- TVL vs volume vs user count: what each measures and misses
- Survivorship bias in DApp studies

#### 2.5 Research Gap and Positioning (400–500 words)
- Prior work focuses on single-protocol or single-sector analyses
- Cross-sector, large-N, multi-source empirical benchmarks are scarce
- This thesis fills the gap with an 855-DApp dataset across 77 chains

---

### Chapter 3 — Methodology · 3,000–3,500 words

*(Full draft in `chapters/03_methodology.md`)*

#### 3.1 Research Design
#### 3.2 Data Collection and Sources
#### 3.3 Sample Construction
#### 3.4 Variable Codebook
#### 3.5 Manual Governance Coding
#### 3.6 Derived Metrics
#### 3.7 Analytical Methods
#### 3.8 Limitations

**Tables in Chapter 3:**
- Table 3.1: Data sources and retrieval methods
- Table 3.2: Eligibility criteria comparison (loose vs strict)
- Table 3.3: Variable codebook (48 variables — also Appendix A)
- Table 3.4: Governance ENUM definitions and decision rules

---

### Chapter 4 — Results · 3,500–4,000 words

#### 4.1 Descriptive Statistics of the Full Dataset (600–800 words)
- 855 DApps across 77 chains: sector, chain, activity distributions
- Missing data rates by variable
- Difference between loose (N=834) and strict (N=68) universes

**Figure 4.1:** Governance distribution — loose universe (`02_governance_distribution_loose_backtest.png`)  
**Table 4.1:** Headline metrics comparison — loose vs strict (from `backtest_headline_metrics.csv`)

#### 4.2 Governance and Ownership Structure (800–1,000 words)
- Distribution of `governance_type`, `ownership_status`, `level_of_decentralisation`
- 86.8% not fully decentralised in strict sample (ANO-PARA-01)
- 52.9% company-owned; 26.5% team-controlled governance
- Token type × governance type cross-tabulation

**Figure 4.2:** Governance distribution — strict universe (`02_governance_distribution_strict.png`)  
**Figure 4.3:** Governance heatmaps — strict (`02_governance_heatmaps_strict.png`)  
**Figure 4.4:** Governance × token type heatmap (`02_governance_token_heatmap_strict.png`)  
**Table 4.2:** Cross-tabulation: decentralisation × governance × cohort

#### 4.3 Market Structure and Capital Concentration (700–900 words)
- Top-10 market cap share: 80.5% (strict), 57.5% (loose)
- Top-10 user share: 90.1% (strict)
- TVL-above-mcap anomaly (ANO-MKT-02, 8.8%)
- Unfunded DApps outperforming funded peers (ANO-MKT-03, 29.4%)

**Figure 4.5:** Market dynamics — strict (`03_market_dynamics_strict.png`)  
**Figure 4.6:** Market dynamics — loose (`03_market_dynamics_loose.png`)

#### 4.4 Blockchain and Multi-Chain Deployment (400–600 words)
- Top-15 chains by DApp count and user concentration
- 70.6% multichain in strict sample (INS-ADP-02)
- Chain specialisation patterns: Ethereum DeFi, BSC GameFi

**Figure 4.7:** Chain distribution — strict (`04_chain_top15_strict.png`)  
**Figure 4.8:** Chain distribution — loose (`04_chain_top15_loose.png`)

#### 4.5 Sector-Level Performance (600–800 words)
- DeFi: 57.4% of strict sample, $299.1B volume, 54.3% of users
- Gaming: 26.5% of strict sample, 12.67M users, low per-user value
- Social and NFT: small shares
- Gaming vs DeFi engagement gap: >100× value-per-user differential (ANO-ENG-01)

**Figure 4.9:** Sector performance — strict (`05_performance_strict.png`)  
**Figure 4.10:** Sector performance — loose (`05_performance_loose.png`)

#### 4.6 Cohort Analysis (400–500 words)
- K-means and PCA cluster summaries from `cohort_manifest.json`
- Primary vs secondary cohort composition
- Sector × governance co-structure

**Figure 4.11:** Governance heatmaps — cohort (`02_governance_heatmaps_cohort.png`)  
**Figure 4.12:** Governance × token heatmap — cohort (`02_governance_token_heatmap_cohort.png`)

---

### Chapter 5 — Discussion · 2,500–3,000 words

#### 5.1 The Decentralisation Paradox (600–700 words)
- 86.8% not fully decentralised despite blockchain infrastructure (DIS-01, ANO-PARA-01)
- Governance label as marketing vs verifiable on-chain reality
- Progressive decentralisation: snapshot limitation and the path argument

#### 5.2 Labelling vs Mechanics: Governance Tokens and Real Power (500–600 words)
- Governance token issuance ≠ community control (DIS-02, ANO-GOV-02)
- Token design serving fundraising rather than participation
- Implications for regulatory classification of governance tokens

#### 5.3 Capital Concentration Mirrors Web2 (400–500 words)
- Winner-takes-most in an open, permissionless ecosystem (DIS-03)
- Network effects, liquidity depth, and composability as concentration drivers
- Does decentralised infrastructure actually prevent market dominance?

#### 5.4 Measuring DApp Success: User Count vs Economic Activity (400–500 words)
- Gaming vs DeFi engagement gap (DIS-04, ANO-ENG-01)
- UAW as inadequate single metric
- Proposal for a multi-dimensional activity score

#### 5.5 Multi-Chain Strategy and Survival (300–400 words)
- Causality question: does multi-chain cause success or reflect it? (DIS-07)
- Survivorship bias in the 1.3× premium finding

#### 5.6 Policy Implications (300–400 words)
- Regulating governance labels: disclosure requirements
- Retail investor protection in token-governed protocols
- Index construction for DApp ecosystem monitoring

---

### Chapter 6 — Conclusions · 1,000–1,500 words

#### 6.1 Summary of Contributions (400–500 words)
- Empirical benchmark: 855 DApps, 77 chains, 48 variables
- Governance and ownership structure findings
- Capital concentration and sector dynamics

#### 6.2 Implications for Practice and Policy (300–400 words)
- Builders: governance design trade-offs
- Investors: beyond UAW metrics
- Regulators: label accountability

#### 6.3 Limitations (200–300 words)
- Snapshot timing (November 2025)
- Survivorship bias in DappRadar top-500 sample
- Self-reported and manually coded governance data

#### 6.4 Future Research Directions (200–300 words)
- Longitudinal tracking of progressive decentralisation
- On-chain vote participation analysis
- Cross-chain liquidity aggregation measurement

---

### References

Format: APA 7th edition (PoliMi standard for management/innovation theses)  
Target: 60–80 sources

Key reference clusters:
- Blockchain/DApp fundamentals (Nakamoto, Buterin, Wood)
- DeFi governance (Aramonte, Barbereau, Freni, Tan)
- Market microstructure (Schär, Lommers)
- Research methodology (cross-sectional design, web scraping ethics)
- DappRadar/DeFiLlama technical documentation

---

### Appendix A — Complete Variable Codebook

- Full 48-variable table (reproduced from `DATABASE_COLUMNS.md`)
- ENUM type definitions for `governance_type`, `ownership_status`, `level_of_decentralisation`
- Extended codebook columns: `ecosystem_focus`, `sustainment_model`, `go_to_market`, `main_revenue_generator`, `funding_type`, `admin_key_risk` (from DATABASE_COLUMNS.md v2_ columns)
- Coding rules and decision trees for manual research fields

---

### Appendix B — Analytical Pipeline

- Reproducibility instructions (from `METHODOLOGY.md`)
- Script sequence: `01_prepare.py` → `02_governance.py` → `03_market.py` → `04_chains.py` → `05_performance.py` → `06_concept_synthesis.py` → `07_thesis_docs.py`
- Source data: `DAPP_Dataset_Nov_2025 - Final.csv`

---

## Figure Placement Plan (All 15 Figures)

| Figure ID | File | Placement | Caption |
|-----------|------|-----------|---------|
| 4.1 | `02_governance_distribution_loose_backtest.png` | §4.1 | Governance label distribution — loose universe (N=834) |
| 4.2 | `02_governance_distribution_strict.png` | §4.2 | Governance label distribution — strict universe (N=68) |
| 4.3 | `02_governance_heatmaps_strict.png` | §4.2 | Governance × ownership heatmap — strict sample |
| 4.4 | `02_governance_token_heatmap_strict.png` | §4.2 | Governance type × token type heatmap — strict sample |
| 4.5 | `03_market_dynamics_strict.png` | §4.3 | Market capitalisation and user concentration — strict |
| 4.6 | `03_market_dynamics_loose.png` | §4.3 | Market dynamics — loose universe comparison |
| 4.7 | `04_chain_top15_strict.png` | §4.4 | Top-15 blockchain deployments — strict sample |
| 4.8 | `04_chain_top15_loose.png` | §4.4 | Top-15 blockchain deployments — loose universe |
| 4.9 | `05_performance_strict.png` | §4.5 | Sector-level performance metrics — strict sample |
| 4.10 | `05_performance_loose.png` | §4.5 | Sector-level performance — loose universe |
| 4.11 | `02_governance_heatmaps_cohort.png` | §4.6 | Governance × ownership — primary cohort |
| 4.12 | `02_governance_token_heatmap_cohort.png` | §4.6 | Governance × token type — primary cohort |
| 4.13 | `02_governance_distribution_cohort.png` | §4.6 | Governance distribution — cohort slice |
| 4.14 | `02_governance_heatmaps_loose_backtest.png` | §4.1 (comparison) | Governance heatmap — loose backtest comparison |
| 4.15 | `02_governance_token_heatmap_loose_backtest.png` | §4.1 (comparison) | Token heatmap — loose backtest |

---

## Key Numbers Reference Card

| Metric | Loose (N=834) | Strict (N=68) |
|--------|--------------|--------------|
| % DECENTRALIZED | 4.68% | 13.24% |
| % Team-controlled governance | 62.71% | 26.47% |
| % Company-owned | 82.97% | 52.94% |
| Top-10 market cap share | 57.54% | 80.46% |
| Top-10 user share | n/a | 90.14% |
| % Multichain | 36.21% | 70.59% |
| Median governance score | 0.0667 | 0.2833 |
| DeFi share of DApps | — | 57.35% |
| Gaming share of DApps | — | 26.47% |
| % governance token | — | 26.47% |

---

*Last updated: 2026-05-19 | Status: Ready for review*
