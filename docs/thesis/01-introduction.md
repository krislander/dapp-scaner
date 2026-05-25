---
title: "Chapter 1: Introduction"
---

# Chapter 1 — Introduction

## 1.1 Motivation and Context

The emergence of decentralised applications (DApps) represents one of the most consequential architectural shifts in internet infrastructure since the transition to cloud computing. Beginning with the Bitcoin network in 2009 (Nakamoto, 2008), the blockchain paradigm introduced a mechanism for trustless, peer-to-peer value transfer that did not depend on centralised intermediaries. The subsequent development of programmable smart contract platforms — most notably Ethereum (Buterin, 2014; Wood, 2014) — transformed this insight into a general-purpose application layer, enabling autonomous, self-executing agreements whose logic is encoded and enforced by a distributed network rather than any single institution.

By the mid-2020s, this application layer had grown into a complex and differentiated ecosystem. Decentralised finance (DeFi) protocols allow users to lend, borrow, trade, and earn yield on digital assets without engaging a bank or broker. Gaming and metaverse applications (GameFi) use non-fungible tokens (NFTs) as in-game property that players genuinely own. NFT marketplaces facilitate the creation and exchange of unique digital artefacts. Decentralised autonomous organisations (DAOs) experiment with on-chain governance as an alternative to corporate hierarchy. Each of these verticals operates on the same underlying blockchain infrastructure yet displays strikingly different economic models, user behaviours, and governance structures.

Underlying all these sectors is a foundational claim: decentralisation. The word carries normative weight in Web3 discourse, invoking resistance to censorship, user sovereignty, open access, and the redistribution of platform rents from platform owners to participants (Schär, 2021). It functions simultaneously as a technical descriptor and a marketing proposition. Projects announce governance tokens, deploy multi-signature safeguards, and launch community forums as visible signals of their commitment to the decentralisation ideal. Whether these signals correspond to genuine shifts in power — away from founders and venture capital, toward distributed token holders — is an empirical question that the literature has been slow to answer systematically.

The governance accountability gap is real and consequential. Retail participants allocate capital and attention to DApps partly on the basis of governance disclosures. Regulators in multiple jurisdictions have begun scrutinising whether tokens marketed as governance instruments constitute securities (Aramonte et al., 2021). Researchers studying platform competition, digital public goods, and institutional economics need reliable data on how DApp governance actually works, not merely how it is described. Yet the empirical base is thin. Existing studies tend to examine individual protocols in depth (Barbereau et al., 2022; Tan et al., 2023), focus narrowly on a single sector such as DeFi (Lommers et al., 2021), or rely on on-chain vote records that capture only a subset of governance activity (Freni et al., 2022). Large-scale, cross-sectional analyses that cover the full diversity of the DApp ecosystem — multiple sectors, multiple chains, multiple governance models — are scarce. This thesis addresses that gap.

---

## 1.2 Research Questions

This thesis investigates the alignment between governance design labels and the observable economic and adoption structure of the DApp ecosystem. The analysis is grounded in a manually coded dataset of 855 DApps drawn from DappRadar's top-500 unique active wallet (UAW) rankings, supplemented by manual additions, and enriched with multi-source market and usage metrics collected in November 2025. Four research questions guide the empirical work.

**RQ1: How do governance models and ownership structures co-vary across DApp ecosystem sectors?**

The first question establishes the structural baseline. It asks whether governance type (DAO, company, team, hybrid) and ownership status (company-owned, investor-backed, community-owned) are distributed randomly across sectors, or whether systematic patterns exist. If DeFi protocols cluster around one governance archetype while GameFi applications cluster around another, that co-variation has implications for how sector-specific risk is assessed and regulated.

**RQ2: Does the decentralisation label match actual governance mechanics at the application layer?**

The second question probes the central tension motivating this research. Decentralisation is often treated as binary — a project either is or is not decentralised — when in practice it is a spectrum of administrative controls, token distributions, upgrade-key permissions, and community participation norms. This question operationalises decentralisation through a composite governance score and examines whether projects labelled as decentralised exhibit the expected structural properties, or whether the label is decoupled from operational reality.

**RQ3: What structural patterns emerge in capital and user concentration across blockchain verticals?**

The third question examines market structure. Even in a permissionless ecosystem, network effects, liquidity depth, and brand recognition may produce winner-takes-most dynamics. This question asks how concentrated market capitalisation and user activity are within and across sectors, and whether the observed distributions are consistent with the power-law patterns documented in other digital platform markets (Chen et al., 2020).

**RQ4: How does multi-chain deployment correlate with market performance and adoption?**

The fourth question addresses a strategic dimension of ecosystem evolution. As the number of active blockchain networks has proliferated, many DApps have deployed across multiple chains simultaneously. This question asks whether cross-chain presence is associated with higher market valuations and user counts, and what the direction and magnitude of that relationship looks like after controlling for sector and governance type.

Together, these four questions frame a coherent inquiry into the gap between the normative claims of Web3 and the structural realities observable in a large cross-sectional dataset.

---

## 1.3 Scope and Boundaries

**Sample.** The empirical analysis covers 855 DApps identified through DappRadar's top-500 UAW list as of November 2025, augmented by manual additions drawn from sector-specific directories and protocol documentation. To support sensitivity analysis, the thesis distinguishes two analytic universes: a *loose sample* (N = 834) that retains all DApps with any non-null metric, and a *strict sample* (N = 68) that applies eligibility filters requiring complete market capitalisation, user activity, and governance classification data. The strict sample is the primary vehicle for inferential statements; the loose sample is used for descriptive comparisons and backtest validation.

**Chains.** The dataset spans 77 unique blockchain networks, including both Ethereum Virtual Machine (EVM) compatible chains (Ethereum, Arbitrum, Base, Polygon, BNB Chain, Optimism) and non-EVM environments (Solana, TON, Sui, Flow). Layer-0 and Layer-1 infrastructure protocols are excluded; the unit of analysis is the application layer, not the network layer.

**Sectors.** The taxonomy follows DappRadar's classification scheme, distinguishing DeFi (including DEX, lending, yield aggregators), Gaming (including NFT gaming and metaverse), NFT marketplaces, Social applications, and Infrastructure tooling. Centralised exchanges, crypto wallets, and pure node infrastructure are outside scope.

**Temporal snapshot.** The dataset represents a point-in-time cross-section. Market metrics (market capitalisation, trading volume, TVL) are derived from November 2025 API pulls from DappRadar, DeFiLlama, CoinMarketCap, and CoinGecko. Governance classifications are manually coded from publicly available documentation, smart contract code, and DAO forum records as of the same reference period. Longitudinal dynamics — such as the progression from team-controlled to community-controlled governance over time — are outside the scope of this study and are identified as a priority for future research.

**Governance variables.** The manual coding scheme captures governance type (six categories), ownership status (five categories), level of decentralisation (four categories), token type, presence of a governance score, multi-signature configuration, admin-key risk classification, and funding history. The full variable codebook covering 48 variables is reproduced in Appendix A.

---

## 1.4 Contribution

This thesis makes three interconnected contributions to the empirical literature on decentralised applications.

**First, it provides a cross-sectional governance benchmark at a scale not previously attempted.** The combination of 855 DApps, 77 blockchains, and 48 variables — with manual governance coding validated against on-chain data — constitutes a richer empirical foundation than prior single-protocol or single-sector studies. The dataset is constructed with explicit eligibility criteria that enable replication and extension, and the dual-universe design (loose and strict samples) allows readers to assess the sensitivity of findings to data-quality thresholds.

**Second, it produces a set of concrete, quantified observations about governance reality in the current DApp ecosystem.** Headline findings include: 86.8% of DApps in the strict sample are not fully decentralised by the coding criteria; the top ten DApps by market capitalisation account for 80.5% of the strict sample's total market value; and 70.6% of strictly eligible DApps have deployed across multiple chains. These figures provide an empirical baseline against which future studies, policy interventions, and governance design choices can be benchmarked.

**Third, it develops and applies a multi-source measurement methodology** that integrates DappRadar activity data, DeFiLlama TVL, CoinMarketCap pricing, CoinGecko metadata, and manual governance annotations into a unified analytic pipeline. The methodology — including the Python scripts and data processing steps — is documented in Appendix B, enabling reproducibility. The composite governance score constructed from this pipeline, and its correlation with market performance metrics, offers a starting point for standardised DApp governance measurement.

---

## 1.5 Thesis Structure

The remainder of this thesis is organised as follows.

**Chapter 2 — Literature Review** reviews the scholarly foundations on which this study builds. It covers the definitional and taxonomic debates surrounding DApps and smart contracts; the theoretical and empirical literature on Web3 governance mechanisms; evidence on market structure and capital concentration in open protocols; and the measurement challenges associated with DApp adoption and activity. The chapter concludes by positioning the present study relative to the existing research gap.

**Chapter 3 — Methodology** describes the research design in full. It presents the data collection process, source selection rationale, eligibility criteria, and the manual governance coding procedure. It explains the construction of derived variables including the governance score, multi-chain indicator, and per-user activity metrics. It details the analytical methods employed — including descriptive statistics, cross-tabulation, correlation analysis, K-means clustering, and principal components analysis — and acknowledges the study's principal limitations.

**Chapter 4 — Results** presents the empirical findings organised around the four research questions. It reports governance and ownership distributions in the full and strict samples, market capitalisation and user concentration patterns, blockchain deployment choices, sector-level performance profiles, and cohort analysis outcomes. All figures and tables referenced in the text are embedded in this chapter.

**Chapter 5 — Discussion** interprets the results in the light of the literature reviewed in Chapter 2. It develops the concept of the decentralisation paradox, examines the gap between governance labelling and governance mechanics, considers capital concentration in the context of open and permissionless markets, and assesses the strategic implications of multi-chain deployment. It also addresses policy implications for regulators, builders, and investors.

**Chapter 6 — Conclusions** summarises the study's contributions, situates them relative to the original research questions, acknowledges limitations, and identifies directions for future research.

**Appendices** provide the full 48-variable codebook (Appendix A) and the analytical pipeline documentation with script sequence and reproducibility instructions (Appendix B).

---

*Word count: approximately 1,750 words*

---

### References (Chapter 1 — cited)

Aramonte, S., Huang, W., & Schrimpf, A. (2021). DeFi risks and the decentralisation illusion. *BIS Quarterly Review*, December 2021.

Barbereau, T., Smethurst, R., Papageorgiou, O., Rieger, A., & Fridgen, G. (2022). DeFi, not so decentralized: The measured distribution of voting rights. In *Proceedings of the 55th Hawaii International Conference on System Sciences*.

Buterin, V. (2014). *A next-generation smart contract and decentralised application platform*. Ethereum Foundation White Paper.

Chen, W., Zheng, Z., Ngai, E. C.-H., Zheng, P., & Zhou, Y. (2020). Exploiting blockchain data to detect smart Ponzi schemes on Ethereum. *IEEE Access*, *8*, 37575–37586.

Freni, P., Ferro, E., & Moncada, R. (2022). Tokenomics and blockchain tokens: A design-oriented morphological framework. *Blockchain: Research and Applications*, *3*(1), 100069.

Lommers, K., de Ville de Goyet, O., & van Liebergen, B. (2021). *Bridging the gap in DeFi: Empirical evidence on governance participation in decentralised protocols*. SSRN Working Paper.

Nakamoto, S. (2008). *Bitcoin: A peer-to-peer electronic cash system*. Bitcoin.org White Paper.

Schär, F. (2021). Decentralized finance: On blockchain- and smart contract-based financial markets. *Federal Reserve Bank of St. Louis Review*, *103*(2), 153–174.

Tan, J., Allen, D., Berg, C., Lane, A., & Potter, T. (2023). The DAO that launched a thousand DAOs: An empirical study of the MakerDAO governance structure. *Journal of Financial Regulation*, *9*(1), 52–78.

Wood, G. (2014). *Ethereum: A secure decentralised generalised transaction ledger*. Ethereum Project Yellow Paper.
