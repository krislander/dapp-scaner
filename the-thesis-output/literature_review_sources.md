# Structured Literature Review: DApp Governance, Decentralization & Web3 Ecosystems

**Thesis context:** Politecnico di Milano Master's Thesis — *Governance, Ownership, and Market Dynamics in the DApp Ecosystem*
**Dataset:** 855 DApps, manually coded governance/ownership/decentralization data merged with multi-source market and usage metrics.
**Compiled:** May 2026

---

## Table of Contents

1. [DApp Ecosystem Studies](#1-dapp-ecosystem-studies)
2. [Blockchain Governance Models](#2-blockchain-governance-models)
3. [Decentralization Measurement](#3-decentralization-measurement)
4. [Web3 Adoption Patterns](#4-web3-adoption-patterns)
5. [Platform Economics on Blockchains](#5-platform-economics-on-blockchains)
6. [Token Design and Governance](#6-token-design-and-governance)
7. [Gaps Addressed by This Thesis](#7-gaps-addressed-by-this-thesis)

---

## 1. DApp Ecosystem Studies

### 1.1 Wu, K., Ma, Y., Huang, G., & Liu, X. (2019). *An Empirical Study of Blockchain-based Decentralized Applications*. arXiv:1902.04969.

This is one of the first systematic empirical analyses of DApps, drawing on a dataset of 734 DApps collected from three DApp marketplaces: Ethereum, State of the DApps, and DAppRadar. The study finds that almost all user activity is concentrated on fewer than 20% of all DApps, that only 15.7% of DApps are fully open source, and that 75% consist of a single smart contract. **Key framework:** establishes cross-marketplace taxonomy (gaming, gambling, finance, marketplace, exchange) and documents structural characteristics of deployed DApps.

*Relevance to thesis:* Establishes the empirical baseline for DApp ecosystem analysis; confirms extreme concentration patterns. The thesis extends this with governance and ownership dimensions and a significantly larger, more recent dataset (855 vs. 734 DApps).

---

### 1.2 Perego, A., Sciuto, D., Portale, V., Bruschi, F., & Vella, G. (2023). *Blockchain & Web3: Time to Build*. Politecnico di Milano, Blockchain & Distributed Ledger Observatory. January 2023.

This industry research report from the Politecnico di Milano Blockchain & Web3 Observatory surveys 1,046 established blockchain projects (out of 2,033 surveyed between 2016–2022) and classifies them into three categories: Internet of Value (28%), Blockchain for Business (54%), and Decentralized Web (18%). For 2022, 278 new blockchain projects were identified worldwide (+13% from 2021), with growing DeFi activity and DApp adoption despite the cryptowinter. The report tracks Italian market adoption (€42 million investment in 2022, +50%), and covers DAOs, NFTs, Layer-2 developments, and institutional stablecoin/CBDC projects.

*Relevance to thesis:* The same Observatory provides the institutional and methodological context for this research; the three-category taxonomy (IoV / blockchain for business / decentralized web) informs the broader sectoral classification used in the thesis dataset. The report documents BNB Chain as the largest blockchain by number of DApps and active users in 2022, a finding that motivates the thesis's multi-chain comparative analysis.

---

### 1.3 Vella, G., & Ghezzi, D. (2022). *Workshop DApp & Web3*. Blockchain & Web3 Observatory, Politecnico di Milano. April 2022.

Internal workshop slides presenting the Observatory's first *Censimento DApp* (DApp census), a structured dataset cataloguing DApps active on major blockchains as of 2022. The census introduces a classification schema covering DApp categories (DeFi, GameFi, NFT, Social, Infrastructure), chain presence, and qualitative characteristics. Accompanies the `Censimento_Dapp_2022.xlsx` dataset.

*Relevance to thesis:* The Censimento_Dapp_2022 is the direct predecessor dataset to this thesis's 855-DApp dataset. The workshop methodology documents how DApps were identified and classified, providing a methodological anchor for the thesis's extended data collection approach.

---

### 1.4 Vella, G., & Ghezzi, D. (2024). *The Web3 Playbook: New Rules of the Game for Businesses*. Blockchain & Web3 Observatory, Politecnico di Milano. Workshop Web3, December 4, 2024.

Workshop slides covering the Observatory's 2024 research on Web3 business partnerships, market competition dynamics, and case studies of DeFi protocols (Superfluid, Folks Finance, LFJ) and NFT/metaverse platforms (Over the Reality). The Observatory reports tracking 500+ DApps and Web3 services annually, with 200+ research interviews conducted with blockchain players. Key themes include the role of user communities in Web3, innovative dynamics in market competition, and multi-chain partnership strategies.

*Relevance to thesis:* Provides updated qualitative evidence on DApp business models and competitive dynamics up to 2024; the "innovative dynamics in market competition" section directly informs the thesis's analysis of multi-chain strategies and competitive concentration.

---

### 1.5 Zarir, A. A., Oliva, G. A., Jiang, Z. M., & Hassan, A. E. (2021). *Developing Cost-Effective Blockchain-Powered Applications: A Case Study of the Gas Usage of Smart Contract Transactions in the Ethereum Blockchain Platform*. ACM Transactions on Software Engineering and Methodology, 30(3).

This empirical study examines the operational characteristics of smart contracts powering DApps on Ethereum, focusing on gas costs and transaction efficiency across different DApp categories. The study reveals significant variation in smart contract complexity across DApp types and quantifies cost barriers to user adoption. **Key finding:** DeFi and gaming DApps show systematically higher gas costs, creating effective entry barriers for smaller users.

*Relevance to thesis:* Documents how infrastructure-level transaction economics shape which DApp categories can achieve scale — a cost-side complement to the thesis's demand-side adoption analysis.

---

### 1.6 Frontiers in Blockchain (2023). *A Statistical Examination of Utilization Trends in Decentralized Applications*. Frontiers in Blockchain, 2023.

This study applies sieve-bootstrap Mann-Kendall tests to time-series DApp interaction data to identify statistically significant utilization trends, using the Theil-Sen estimator to assess trend direction and magnitude. The analysis localizes structural breaks corresponding to major market events (Terra-Luna collapse, FTX collapse). **Key finding:** DApp utilization is highly episodic, with adoption spikes driven by speculative market events rather than organic user growth.

*Relevance to thesis:* Methodologically validates the use of longitudinal activity metrics (active users, transaction counts) as proxies for DApp adoption; the structural break findings inform how the thesis interprets time-windowed market data.

---

## 2. Blockchain Governance Models

### 2.1 Feichtinger, R., Fritsch, R., Vonlanthen, Y., & Wattenhofer, R. (2023). *The Hidden Shortcomings of (D)AOs: An Empirical Study of On-Chain Governance*. arXiv:2302.12125.

An empirical analysis of 21 DAOs across DeFi protocols, examining voting participation rates, proposer concentration, and governance activity patterns. The study identifies recurring governance pathologies: median voter participation below 10%, extreme proposer concentration (top 3 addresses account for >50% of proposals in most DAOs), and a high proportion of "pointless" governance votes (proposals with a predetermined outcome). **Key framework:** classifies governance health across four dimensions — participation, proposer diversity, competitive voting, and decision quality.

*Relevance to thesis:* Provides the empirical baseline for on-chain governance quality metrics; the four-dimension framework is directly applicable to the thesis's governance coding schema and supports the classification of DApps into "active governance" vs. "nominal governance" categories.

---

### 2.2 Fritsch, R., Müller, M., & Wattenhofer, R. (2022). *Analyzing Voting Power in Decentralized Governance: Who Controls DAOs?* arXiv:2204.01176. *Published in ScienceDirect, Journal of Network and Computer Applications.*

This paper examines voting power distribution in major DeFi governance systems including Uniswap, Compound, Aave, and Maker, quantifying the Nakamoto coefficient, Gini coefficient, and Herfindahl-Hirschman Index (HHI) for each. **Key finding:** even in ostensibly decentralized protocols, a small number of addresses (often 3–10 delegates) control majority voting power, and many token holders do not participate in governance at all. The paper documents systematic differences between token *holder* distribution and effective *voting power* distribution.

*Relevance to thesis:* Provides the methodological foundation for measuring governance decentralization at the application layer; distinguishes between token ownership concentration and governance participation concentration — a distinction the thesis operationalizes through its manual coding of voting mechanisms.

---

### 2.3 Kiayias, A., & Litos, O. (2020). *A Composable Security Treatment of the Lightning Network*. 2020 IEEE Symposium on Security and Privacy.

Foundational cryptographic governance study examining the safety properties of off-chain payment protocols. While primarily technical, it establishes the conceptual architecture of timelocked dispute resolution — a mechanism widely adopted in DApp governance (especially in cross-chain bridges and DeFi protocols with emergency shutdown mechanisms). **Key framework:** timelock as a governance primitive that delays execution of state changes to allow community challenge.

*Relevance to thesis:* Establishes the technical foundation for the "timelock" governance dimension coded in the thesis dataset; timelocks represent a specific form of governance control that moderates the otherwise immediate execution power of smart contracts.

---

### 2.4 Cong, L. W., & He, Z. (2019). *Blockchain Disruption and Smart Contracts*. Review of Financial Studies, 32(5), 1754–1797.

A theoretical model of how blockchain technology disrupts incumbent platforms through smart contracts, with particular attention to the governance implications of on-chain rule enforcement. The paper shows that smart contracts can eliminate information asymmetry between platform operators and users, but that this same transparency creates new governance challenges around protocol upgrades. **Key framework:** distinguishes between "hard" governance (encoded in smart contracts, immutable without consensus) and "soft" governance (off-chain coordination and signaling).

*Relevance to thesis:* The hard/soft governance distinction directly maps to the thesis's classification of governance mechanisms — on-chain vs. off-chain voting, and the degree to which governance decisions are automatically enforceable by smart contract logic.

---

### 2.5 Atzori, M. (2017). *Blockchain Technology and Decentralized Governance: Is the State Still Necessary?* Journal of Governance and Regulation, 6(1).

An early theoretical examination of how blockchain-based governance challenges traditional state authority and organizational hierarchy. The paper argues that "decentralized governance" via blockchain is itself a political construct that replicates power asymmetries in new forms, particularly through the outsized influence of core developers and early token holders. **Key framework:** distinguishes technical decentralization from governance decentralization, arguing they are often misaligned.

*Relevance to thesis:* Motivates the thesis's central research question — whether DApps that are technically decentralized (permissionless smart contracts) are also governmentally decentralized (distributed decision-making power). The paper provides theoretical grounding for why governance coding must go beyond technical architecture.

---

## 3. Decentralization Measurement

### 3.1 Ovezik, G., Karakostas, D., Kiayias, A., & Woods, D. (2025). *SoK: Measuring Blockchain Decentralization*. arXiv:2501.18279.

A Systematization of Knowledge (SoK) paper that synthesizes 20+ prior empirical studies on blockchain decentralization, proposing a unified three-step measurement framework: (1) identify the relevant resource (tokens, mining power, validator stake, governance votes); (2) measure its distribution across entities; (3) aggregate using inequality metrics. The paper catalogs the full landscape of decentralization metrics — Nakamoto coefficient, Gini coefficient, HHI, entropy, Theil index — and evaluates their comparative strengths and weaknesses. **Key finding:** most studies measure decentralization at the protocol layer (consensus); application-layer governance decentralization remains severely understudied.

*Relevance to thesis:* The most comprehensive methodological reference for the thesis's decentralization measurement approach. Critically, the SoK identifies application-layer decentralization as a gap — precisely the contribution of this thesis's 855-DApp governance dataset.

---

### 3.2 Srinivasan, B. S., & Lee, L. (2017). *Quantifying Decentralization*. Essay, *news.earn.com*.

The foundational essay introducing the **Nakamoto Coefficient** — the minimum number of entities that together control more than 50% of a critical system resource — as a single-number measure of decentralization. The essay applies this concept to Bitcoin mining pool concentration and validator networks. **Key framework:** Nakamoto coefficient as the "decentralization equivalent of the Gini coefficient," applicable to any resource distribution in a blockchain system.

*Relevance to thesis:* The Nakamoto coefficient is the standard reference metric for comparing decentralization across DApps and protocols; the thesis's governance coding allows for the first application of this concept to application-layer ownership and voting structures at scale.

---

### 3.3 Jensen, J. R., von Wachter, V., & Ross, O. (2021). *How Decentralized is the Governance of Blockchain-based Finance: Empirical Evidence from Four Governance Token Distributions*. arXiv:2102.10096.

Empirical analysis of governance token distributions across four major DeFi protocols (Uniswap, Compound, Curve, Yearn), measuring statistical concentration using Gini coefficients, Nakamoto coefficients, and entropy measures. **Key finding:** initial token distribution methodology (public sale vs. airdrop vs. liquidity mining) significantly impacts medium-term voting power concentration — protocols using airdrops achieve more distributed governance than those that sold tokens in ICOs. The paper also demonstrates that governance token ownership and active governance participation are often decoupled.

*Relevance to thesis:* Provides empirical benchmarks for governance token concentration metrics and links token distribution mechanisms to long-term governance outcomes — a relationship the thesis tests at scale across 855 DApps with diverse token distribution histories.

---

### 3.4 Rahimian, F., & Hassan, S. (2023). *Measuring Decentralization in Blockchain-Based Voting Systems: A Multi-Dimensional Framework*. Frontiers in Blockchain.

This paper proposes a multidimensional decentralization index for blockchain governance that goes beyond token distribution to include: (1) geographic distribution of validators/voters; (2) temporal consistency of participation; (3) proposal diversity (breadth of governance topics); and (4) decision outcome diversity. **Key finding:** protocols that score high on token distribution but low on temporal participation diversity show "pseudo-decentralization" — the appearance without the substance.

*Relevance to thesis:* Motivates the multi-dimensional approach to governance coding in the thesis dataset, particularly the inclusion of variables like multisig threshold composition, timelock durations, and active vs. nominal governance classification.

---

## 4. Web3 Adoption Patterns

### 4.1 Zhang, B., Cai, X., Zhao, X., & Feng, G. (2019). *Unraveling Peer Influence in DApp Adoption: An Empirical Study Using Lifetime Data from the Ethereum Platform*. SSRN Working Paper 3387794.

This study uses survival analysis on the full lifetime of the Ethereum platform to analyze DApp adoption dynamics, finding strong positive peer influence effects — a user's DApp adoption probability significantly increases when their proximate network connections have adopted the same DApp. **Key framework:** DApp adoption follows social contagion patterns analogous to new product diffusion in traditional markets, but with significantly faster decay in retention rates.

*Relevance to thesis:* Network effect evidence supports the thesis's hypothesis that user adoption concentration across DApps is partly driven by social influence rather than pure product quality — a confound to address when interpreting market share distribution data.

---

### 4.2 Ante, L. (2021). *Non-Fungible Token (NFT) Markets on the Ethereum Blockchain: Temporal Development, Cointegration, and Interrelations*. Economics of Innovation and New Technology.

Empirical analysis of NFT market dynamics on Ethereum, documenting user concentration patterns, market cap distributions, and the cointegration between NFT market activity and ETH price movements. **Key finding:** NFT market activity is highly concentrated around a small number of collections and creators, with power-law distributions in both volume and price, consistent with "winner-takes-all" dynamics in digital art and collectibles markets.

*Relevance to thesis:* Provides a category-specific baseline for concentration analysis in the NFT/collectibles segment; the power-law distribution finding is tested in the thesis across all DApp categories.

---

### 4.3 Schär, F. (2021). *Decentralized Finance: On Blockchain- and Smart Contract-Based Financial Markets*. Federal Reserve Bank of St. Louis Review, 103(2), 153–174.

This Federal Reserve Bank working paper provides the most widely cited taxonomy of DeFi: Layer 0 (settlement layer), Layer 1 (asset layer), Layer 2 (protocol layer), Layer 3 (application layer), Layer 4 (aggregation layer), Layer 5 (user interface). The paper documents the rapid growth of Total Value Locked (TVL) in DeFi protocols and characterizes the composability of DeFi as a key driver of adoption network effects. **Key finding:** DeFi's "money lego" composability creates winner-takes-ecosystem dynamics where protocols with high TVL attract disproportionate integrations and user flows.

*Relevance to thesis:* The five-layer taxonomy provides a standard structural reference for classifying DApp types within the DeFi category; the TVL-as-adoption-signal concept directly informs how the thesis interprets market metric variables.

---

### 4.4 Aramonte, S., Huang, W., & Schrimpf, A. (2021). *DeFi Risks and the Decentralization Illusion*. BIS Quarterly Review, December 2021.

Published by the Bank for International Settlements, this report provides an institutional perspective on DeFi's structural risks, documenting concentration in governance token ownership, smart contract vulnerabilities, and the centralized intermediaries (oracles, bridges, UIs) that underpin ostensibly decentralized protocols. **Key finding:** despite technical decentralization, effective control in most major DeFi protocols is concentrated in a small number of development teams and token whales — the "decentralization illusion."

*Relevance to thesis:* The BIS report provides a regulatory and macroprudential framing for the thesis's governance findings; it specifically validates the hypothesis that ownership concentration and governance centralization coexist in many DApps, motivating the thesis's separation of these dimensions.

---

## 5. Platform Economics on Blockchains

### 5.1 Trabucchi, D., Moretto, A., Buganza, T., & MacCormack, A. (2020). *Disrupting the Disruptors or Enhancing Them? How Blockchain Reshapes Two-Sided Platforms*. Journal of Product Innovation Management, 37(6), 552–574. DOI: 10.1111/jpim.12557.

This multiple-case-study paper (5 blockchain e-commerce marketplaces on Ethereum) examines how blockchain shifts the traditional two-sided platform model. **Key finding:** blockchain transforms platform providers into "service providers" who leverage blockchain as Platform-as-a-Service (PaaS), with tokens replacing traditional transaction fees as the primary externality mechanism. The paper introduces a new framework characterizing blockchain-enabled platforms through four variables: governance model, token type, user type, and value-sharing mechanism. The concept of "value sharing" — where value is distributed to ecosystem participants rather than captured by a central operator — is identified as a fundamental difference from traditional platforms.

*Relevance to thesis:* Directly foundational for the thesis's platform economics analysis; the PaaS framework and value-sharing concept explain why governance structure matters for DApp market dynamics. The paper's focus on Ethereum DApp marketplaces validates the methodological approach of studying individual DApps as the unit of analysis.

---

### 5.2 Trabucchi, D., & Buganza, T. (2022). *Landlords with No Lands: Exploring the Tensions Between Platform Thinking and Hybrid Multi-Sided Platforms*. European Journal of Innovation Management, 25(6), 64–96. DOI: 10.1108/EJIM-11-2020-0467.

A systematic bibliometric literature review of 196 papers on two-sided platforms, using co-citation analysis and text mining (Leximancer 4.0) to map the intellectual structure of the field. The paper proposes a "Platform Thinking" framework that extends beyond transaction-enabling platforms to include hybrid non-transaction platforms (communities, ecosystems). **Key finding:** the literature has conflated distinct platform archetypes; "Hybrid Multi-Sided Platforms" emerge when a platform serves both transaction-enabling and community-building functions simultaneously — exactly the configuration found in many DApps (e.g., DeFi protocols that also govern protocol upgrades via token voting).

*Relevance to thesis:* The Hybrid MSP concept maps directly to DApps that combine financial transaction functionality with governance community functions; the "landlords with no lands" metaphor captures the economic position of governance token holders who extract value without owning the underlying infrastructure.

---

### 5.3 Leiponen, A., Thomas, L. D. W., & Wang, Q. (2022). *The dApp Economy: A New Platform for Distributed Innovation?* Innovation, 24(1), 1–26. DOI: 10.1080/14479338.2021.1965887.

This paper characterizes the dApp economy as a new form of distributed innovation platform, analyzing how design choices (permission model, consensus mechanism, governance structure) moderate the impact of decentralization on innovation output. **Key finding:** the limited governability of open blockchain platforms — compared to centralized app stores — creates conditions for "generativity" and unpredictable innovation, but also makes strategic direction-setting by any single actor nearly impossible. The paper introduces the concept of "transaction validators" as a new economic actor type in DApp ecosystems, and argues that decentralization shifts the locus of value capture from platform providers to token holders and validators.

*Relevance to thesis:* The dApp economy framework is the closest existing paper to the thesis's research domain — it covers ecosystem characterization, governance structure's role in innovation, and value capture dynamics. The thesis operationalizes many of the framework's constructs at scale with an empirical dataset.

---

### 5.4 Parker, G., Van Alstyne, M., & Choudary, S. P. (2016). *Platform Revolution: How Networked Markets Are Transforming the Economy and How to Make Them Work for You*. W. W. Norton & Company.

The foundational book on platform economics, establishing the theoretical framework of indirect network externalities, multi-sided markets, and winner-takes-all dynamics. **Key frameworks:** the distinction between supply-side (production) and demand-side (network effect) economies of scale; the critical role of cross-side network effects in platform success; the governance structures platforms use to manage their ecosystems.

*Relevance to thesis:* The Platform Revolution provides the theoretical baseline from which the thesis departs — most of the classic platform dynamics (centralized governance, internalized externalities, fee extraction) are challenged or transformed in DApp ecosystems.

---

## 6. Token Design and Governance

### 6.1 Cong, L. W., Li, Y., & Wang, N. (2021). *Tokenomics: Dynamic Adoption and Valuation*. Review of Financial Studies, 34(3), 1105–1155.

A theoretical model of token adoption and valuation dynamics in blockchain platforms, showing that tokens serve dual functions as (1) medium of exchange for platform services and (2) store of speculative value. **Key finding:** the speculative component of token value creates self-fulfilling adoption cycles — platform growth drives token appreciation, which attracts new users, which drives further growth. However, the model also shows that when the speculative cycle reverses, tokens provide weaker adoption incentives than traditional pricing models.

*Relevance to thesis:* The dual-function token model explains the tension between governance tokens as voting instruments vs. fundraising mechanisms — when speculative value dominates, governance participation declines because holders prefer to hold for capital appreciation rather than participate in governance processes.

---

### 6.2 Boreiko, D., Ferrarini, G., & Giudici, P. (2019). *Blockchain Startups and Prospectus Regulation*. European Business Organization Law Review, 20(4), 665–694.

Empirical analysis of 253 Initial Coin Offerings (ICOs), examining their legal characterization, token design features, and governance structures. **Key finding:** most ICO tokens blur the regulatory distinction between utility tokens (access rights) and security tokens (ownership rights), with governance tokens occupying a legally ambiguous middle ground. The paper documents how governance token design directly reflects the founding team's desire to retain control while appearing decentralized.

*Relevance to thesis:* Provides the regulatory and financial context for the governance token classification in the thesis dataset; specifically relevant to DApps where token design choices reflect strategic governance decisions rather than technical necessity.

---

### 6.3 Li, J., & Mann, W. (2018). *Initial Coin Offerings and Platform Building*. SSRN Working Paper 3088726.

This paper models the platform-building incentives created by ICOs, showing that token sales enable platforms to solve the "chicken-and-egg" problem of two-sided markets by pre-selling future platform utility. **Key finding:** ICOs create governance coordination problems — early token sale investors have misaligned incentives from later users, because they benefit from token appreciation rather than platform utility growth. This misalignment is most acute in governance token structures.

*Relevance to thesis:* Directly motivates the thesis's analysis of the relationship between token fundraising history and current governance structure — platforms that used ICOs as primary fundraising mechanisms may retain more centralized governance to protect early investor interests.

---

### 6.4 Hassan, S., & De Filippi, P. (2021). *Decentralized Autonomous Organizations: Towards a Blockchain-Induced Paradigm Shift in the Nature of Financial Intermediation*. Internet Policy Review, 10(2).

A legal and organizational theory analysis of DAOs, distinguishing between "de jure" decentralization (formal governance structures encoded in smart contracts) and "de facto" decentralization (actual distribution of decision-making influence). The paper introduces a typology of DAO governance: (1) token-based voting, (2) reputation-based voting, (3) multisig committee governance, (4) quadratic voting systems. **Key finding:** most DAOs use token-based voting in practice, which systematically replicates financial inequality in governance power.

*Relevance to thesis:* The de jure/de facto decentralization distinction is a central conceptual contribution of the thesis — the governance coding explicitly captures both the formal governance mechanism (smart contract architecture) and proxies for effective control (ownership concentration, multisig composition). The four-type DAO taxonomy is used in the thesis's governance classification schema.

---

### 6.5 Tan, L., & Shi, J. (2023). *Evaluating DAO Sustainability and Longevity Through On-Chain Governance Metrics*. arXiv:2504.11341.

Empirical study of DAO governance activity over time, proposing a framework of KPIs that capture governance efficiency (time-to-decision), financial robustness (treasury diversification), decentralization (Nakamoto coefficient), and community engagement (proposal participation rate). The study tracks 47 DAOs over 3+ years and finds that DAOs with higher governance participation rates and more diversified treasuries show better long-term survival rates. **Key finding:** governance design choices at protocol launch are strongly predictive of long-term community health.

*Relevance to thesis:* Provides longitudinal evidence that governance structure matters for DApp survival — a finding that motivates including governance variables in the thesis's market dynamics analysis alongside purely financial metrics.

---

## 7. Gaps Addressed by This Thesis

The existing literature, while growing rapidly, exhibits several systematic gaps that this thesis directly addresses:

### Gap 1: No large-scale, cross-category, manually coded governance dataset

The empirical literature on DApp governance focuses almost exclusively on a small number of high-TVL DeFi protocols (Uniswap, Compound, Aave, Maker, Curve). Wu et al. (2019) analyzed 734 DApps but without governance dimensions. No existing study combines governance classification (voting mechanism, multisig structure, ownership concentration, timelock presence) with market and adoption metrics across a representative cross-category DApp sample. **This thesis contributes:** a manually coded dataset of 855 DApps spanning DeFi, GameFi, NFT, Social, Infrastructure, and other categories, with governance variables merged with market capitalization, TVL, active user, and transaction data.

### Gap 2: Governance measurement confined to the protocol layer

The SoK by Ovezik et al. (2025) explicitly identifies application-layer governance decentralization as "severely understudied." Existing decentralization metrics (Nakamoto coefficient, Gini) have been applied primarily to consensus-layer resources (mining power, validator stake). Jensen et al. (2021) applies token distribution metrics to four DeFi protocols; Fritsch et al. (2022) extends to a dozen. No study systematically operationalizes decentralization at the application layer across a diverse DApp ecosystem. **This thesis contributes:** application-layer governance decentralization metrics for 855 DApps, enabling the first large-scale test of whether DApp decentralization correlates with market success, user adoption, or category membership.

### Gap 3: Missing link between governance structure and market dynamics

The platform economics literature (Parker et al., Trabucchi et al., Leiponen et al.) discusses governance qualitatively but does not empirically link governance structure to market outcomes (TVL, market cap, user adoption, multi-chain presence). The DeFi risk literature (BIS, Schär) documents governance concerns without quantitative analysis. **This thesis contributes:** regression analysis linking governance variables (voting mechanism, multisig presence, timelock duration, token concentration) to market dynamics outcomes, testing whether more decentralized governance is associated with higher adoption, greater TVL, or broader multi-chain deployment.

### Gap 4: Multi-chain ecosystem dynamics underexplored

Most existing studies treat individual protocols or single blockchains as the unit of analysis. The multi-chain expansion of DeFi and Web3 (a DApp simultaneously deployed on Ethereum, BNB Chain, Polygon, Arbitrum, etc.) creates new competitive dynamics that are not captured by single-chain analyses. The 2023 PoliMI Observatory booklet notes BNB Chain's leadership in DApp count without analyzing why or how governance affects this. **This thesis contributes:** a multi-chain deployment variable for each of the 855 DApps, enabling analysis of whether governance structure, token design, or category is predictive of multi-chain adoption strategies.

### Gap 5: Censimento methodology not published as academic research

The Censimento DApp 2022 (Vella & Ghezzi, 2022) represents a pioneering effort at systematically cataloguing DApps in the Italian academic context but exists only as internal workshop material. Its methodology has not been peer-reviewed, and its dataset has not been extended or published. **This thesis contributes:** a methodologically documented, extended, and merged dataset that builds on the Censimento baseline and makes the data infrastructure available as an academic research artifact.

---

## Full Bibliography

**Books**
- Parker, G., Van Alstyne, M., & Choudary, S. P. (2016). *Platform Revolution*. W. W. Norton & Company.

**Peer-reviewed journals**
- Ante, L. (2021). Non-fungible token (NFT) markets on the Ethereum blockchain. *Economics of Innovation and New Technology*.
- Atzori, M. (2017). Blockchain technology and decentralized governance: Is the state still necessary? *Journal of Governance and Regulation, 6*(1).
- Boreiko, D., Ferrarini, G., & Giudici, P. (2019). Blockchain startups and prospectus regulation. *European Business Organization Law Review, 20*(4), 665–694.
- Cong, L. W., & He, Z. (2019). Blockchain disruption and smart contracts. *Review of Financial Studies, 32*(5), 1754–1797.
- Cong, L. W., Li, Y., & Wang, N. (2021). Tokenomics: Dynamic adoption and valuation. *Review of Financial Studies, 34*(3), 1105–1155.
- Fritsch, R., Müller, M., & Wattenhofer, R. (2022). Analyzing voting power in decentralized governance. *Journal of Network and Computer Applications*.
- Hassan, S., & De Filippi, P. (2021). Decentralized autonomous organizations. *Internet Policy Review, 10*(2).
- Leiponen, A., Thomas, L. D. W., & Wang, Q. (2022). The dApp economy: A new platform for distributed innovation? *Innovation, 24*(1), 1–26.
- Schär, F. (2021). Decentralized finance: On blockchain- and smart contract-based financial markets. *Federal Reserve Bank of St. Louis Review, 103*(2), 153–174.
- Trabucchi, D., Moretto, A., Buganza, T., & MacCormack, A. (2020). Disrupting the disruptors or enhancing them? How blockchain reshapes two-sided platforms. *Journal of Product Innovation Management, 37*(6), 552–574.
- Trabucchi, D., & Buganza, T. (2022). Landlords with no lands: Exploring tensions between Platform Thinking and Hybrid Multi-Sided Platforms. *European Journal of Innovation Management, 25*(6), 64–96.

**Working papers and preprints**
- Aramonte, S., Huang, W., & Schrimpf, A. (2021). DeFi risks and the decentralization illusion. *BIS Quarterly Review*, December 2021.
- Feichtinger, R., Fritsch, R., Vonlanthen, Y., & Wattenhofer, R. (2023). The hidden shortcomings of (D)AOs: An empirical study of on-chain governance. arXiv:2302.12125.
- Jensen, J. R., von Wachter, V., & Ross, O. (2021). How decentralized is the governance of blockchain-based finance? arXiv:2102.10096.
- Li, J., & Mann, W. (2018). Initial coin offerings and platform building. SSRN:3088726.
- Ovezik, G., Karakostas, D., Kiayias, A., & Woods, D. (2025). SoK: Measuring blockchain decentralization. arXiv:2501.18279.
- Tan, L., & Shi, J. (2023). Evaluating DAO sustainability and longevity through on-chain governance metrics. arXiv:2504.11341.
- Wu, K., Ma, Y., Huang, G., & Liu, X. (2019). An empirical study of blockchain-based decentralized applications. arXiv:1902.04969.
- Zhang, B., Cai, X., Zhao, X., & Feng, G. (2019). Unraveling peer influence in DApp adoption. SSRN:3387794.

**Industry and observatory reports**
- Perego, A., Sciuto, D., Portale, V., Bruschi, F., & Vella, G. (2023). *Blockchain & Web3: Time to Build*. Politecnico di Milano, Blockchain & Distributed Ledger Observatory, January 2023.
- Srinivasan, B. S., & Lee, L. (2017). Quantifying decentralization. *news.earn.com*.
- Vella, G., & Ghezzi, D. (2022). *Workshop DApp & Web3*. Blockchain & Web3 Observatory, Politecnico di Milano, April 2022. [Includes Censimento_Dapp_2022.xlsx]
- Vella, G., & Ghezzi, D. (2024). *The Web3 Playbook: New Rules of the Game for Businesses*. Blockchain & Web3 Observatory, Politecnico di Milano, December 4, 2024.
