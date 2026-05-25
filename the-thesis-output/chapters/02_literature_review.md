# Chapter 2 — Literature Review

## 2.1 Blockchain Fundamentals and the DApp Ecosystem

### 2.1.1 From Bitcoin to Programmable Blockchains

The intellectual lineage of decentralised applications begins with Nakamoto's (2008) Bitcoin white paper, which demonstrated that a peer-to-peer electronic cash system could operate without a trusted third party by relying on cryptographic proof and a distributed ledger maintained through proof-of-work consensus. Bitcoin established the foundational primitives — append-only ledger, hash-linked blocks, decentralised validator set — but offered only a constrained scripting language that prevented general-purpose computation. The conceptual leap enabling DApps arrived with Buterin's (2014) Ethereum white paper, which proposed a Turing-complete virtual machine (the Ethereum Virtual Machine, EVM) embedded directly in a blockchain. Wood's (2014) Yellow Paper formalised the EVM specification and introduced *gas* — a metering mechanism that priced computational steps to prevent infinite loops and allocate network resources. These two documents together define the technical substrate on which every DApp in the thesis dataset is ultimately deployed.

A *smart contract*, in the sense established by this literature, is a deterministic programme stored on-chain whose execution is triggered by transactions and whose outputs are validated by every node in the network. Because no single entity controls execution, the smart contract displaces the trusted intermediary with verifiable logic (Cong & He, 2019). A *decentralised application* extends this primitive by composing one or more smart contracts with off-chain user interfaces and, in many cases, governance systems that allow stakeholders to amend the contract logic itself. The boundary between protocol and application is deliberately porous: a DApp's smart contracts define the rules of a financial market, a game economy, or a social coordination mechanism, while its governance layer determines who can change those rules and under what conditions.

### 2.1.2 DApp Ecosystem Growth and Taxonomy

Wu et al. (2019) conducted the first systematic empirical census of the DApp ecosystem, drawing on 734 applications catalogued across three aggregators — Ethereum, State of the DApps, and DappRadar. Their study established foundational structural facts that subsequent research has largely replicated at larger scale: activity is concentrated in fewer than 20 per cent of all DApps; approximately 75 per cent of DApps consist of a single smart contract; and only 15.7 per cent of DApps are fully open source. These findings already suggested that the ecosystem's technical decentralisation at the infrastructure layer coexists with highly unequal activity distribution at the application layer.

The Politecnico di Milano Blockchain & Web3 Observatory provides the institutional context most directly relevant to this thesis. Perego et al. (2023) surveyed 1,046 established blockchain projects and classified them into three categories: Internet of Value (28%), Blockchain for Business (54%), and Decentralised Web (18%). For 2022, BNB Chain was identified as the largest blockchain by DApp count and active users — a finding that motivates the thesis's multi-chain comparative design. The Observatory's 2022 DApp census (*Censimento DApp 2022*) introduced a structured classification schema covering DApp categories (DeFi, GameFi, NFT, Social, Infrastructure) and chain presence (Vella & Ghezzi, 2022), which serves as the direct methodological predecessor to the 855-DApp dataset on which this thesis is based.

The DApp sector taxonomy used throughout this thesis — DeFi, GameFi, NFT, Social, and Infrastructure — maps onto the broader classification proposed by Schär (2021), whose five-layer DeFi stack (settlement, asset, protocol, application, aggregation layers) provides a canonical structural reference for categorising DApp types within the financial sector. By 2024, the Observatory was tracking 500+ DApps and Web3 services annually, with multi-chain partnership strategies and user community dynamics emerging as dominant competitive themes (Vella & Ghezzi, 2024).

The operational economics of DApps are not uniform across sectors. Zarir et al. (2021) document significant variation in smart contract complexity and transaction gas costs across DApp categories: DeFi and gaming DApps exhibit systematically higher gas costs, creating effective entry barriers for smaller users and shaping which categories can achieve broad adoption. Frontiers in Blockchain (2023) further demonstrates that DApp utilisation is episodic rather than organic, with adoption spikes driven by speculative market events — the Terra-Luna collapse and FTX bankruptcy are identified as structural breaks in utilisation time series — rather than steady user growth.

---

## 2.2 Governance in Blockchain Systems

### 2.2.1 Conceptual Foundations

The governance of blockchain systems has attracted increasing scholarly attention as it has become clear that the technical architecture of decentralisation does not automatically produce decentralised decision-making. Atzori (2017) argued, in an early theoretical examination, that *blockchain-based governance* is itself a political construct that replicates power asymmetries in new forms: core developers and early token holders exert outsized influence regardless of the formal on-chain voting arrangements. Atzori's distinction between *technical decentralisation* (permissionless access and distributed infrastructure) and *governance decentralisation* (distributed decision-making power) establishes the conceptual tension that this thesis operationalises empirically.

Cong and He (2019) formalised this tension in a theoretical model showing that smart contracts eliminate information asymmetry between platform operators and users but simultaneously create new governance challenges around protocol upgrades. Their key conceptual contribution is the distinction between *hard governance* — rules encoded in immutable smart contract logic — and *soft governance* — off-chain coordination, social norms, and signalling. A protocol cannot be upgraded without some form of soft governance, because smart contracts themselves cannot alter their own logic; the governance layer is therefore always partly off-chain, regardless of how it is marketed.

### 2.2.2 On-Chain and Off-Chain Governance Mechanisms

Empirical research on governance mechanisms has accelerated alongside the growth of the DeFi sector. Feichtinger et al. (2023) conducted an empirical analysis of 21 DAOs across DeFi protocols, documenting recurring governance pathologies: median voter participation below 10%, extreme proposer concentration (the top three addresses account for more than 50% of proposals in most DAOs), and a high proportion of governance votes with predetermined outcomes. The authors classify governance health across four dimensions — participation, proposer diversity, competitive voting, and decision quality — which directly informs the thesis's classification of DApps into "active governance" and "nominal governance" categories.

Fritsch et al. (2022) extended this analysis to the voting power structure of major DeFi protocols (Uniswap, Compound, Aave, Maker), quantifying the Nakamoto coefficient, Gini coefficient, and Herfindahl-Hirschman Index (HHI) for each. Their central finding — that even in ostensibly decentralised protocols, three to ten delegate addresses control majority voting power — distinguishes between token *holder* distribution and effective *voting power* distribution. This distinction motivates the thesis's governance coding strategy, which captures both ownership concentration (as a proxy for potential voting power) and the actual governance mechanism in use.

Hassan and De Filippi (2021) offer the most comprehensive typology of DAO governance, distinguishing between *de jure* decentralisation (formal structures encoded in smart contracts) and *de facto* decentralisation (actual distribution of decision-making influence). They identify four primary governance archetypes: token-based voting, reputation-based voting, multisig committee governance, and quadratic voting systems. In practice, the vast majority of DAOs use token-based voting, which systematically replicates financial inequality as governance power. This four-type taxonomy is adopted as the basis for the `governance_type` variable in the thesis dataset.

### 2.2.3 Timelocks and Multisig as Governance Primitives

Beyond voting mechanisms, the literature identifies two technical instruments that moderate the immediacy of on-chain governance. Kiayias and Litos (2020) establish the theoretical architecture of timelocked dispute resolution in off-chain payment protocols; the timelock mechanism — which delays execution of state changes to allow community challenge — has been widely adopted in DApp governance, particularly in DeFi protocols with emergency shutdown mechanisms. A protocol that enforces a minimum delay between a governance vote passing and the change taking effect provides stakeholders a window to exit or object, thus partially compensating for low participation rates and proposal concentration.

Multisig wallets similarly distribute control by requiring a threshold of signatures (*k-of-n*) before a transaction can be executed. In practice, multisig governance spans a wide range of effective centralisation: a 2-of-3 multisig controlled by core team members is functionally equivalent to team-controlled governance, while a 5-of-9 multisig across geographically and organisationally diverse signatories approaches meaningful decentralisation. The thesis dataset captures multisig composition as a component of the governance coding, allowing for analysis of how threshold design relates to other governance and market variables.

---

## 2.3 Decentralisation Measurement

### 2.3.1 Metrics Landscape

The measurement of decentralisation has attracted a dedicated strand of empirical literature. Srinivasan and Lee (2017) introduced the *Nakamoto coefficient* — the minimum number of entities that together control more than 50% of a critical system resource — as a single-number measure of decentralisation analogous to the Gini coefficient for income inequality. The Nakamoto coefficient is directly applicable to any distributional problem in a blockchain system: mining pool concentration, validator stake, governance token ownership, or voting power delegation.

Ovezik et al. (2025) provide the most comprehensive synthesis of this literature in a Systematization of Knowledge (SoK) paper cataloguing the full landscape of decentralisation metrics. Their unified three-step measurement framework asks: (1) what is the relevant resource; (2) how is it distributed across entities; and (3) how should the distribution be aggregated into a scalar measure? The SoK evaluates the comparative strengths and weaknesses of the Nakamoto coefficient, Gini coefficient, HHI, Shannon entropy, and Theil index. Its most important finding for the present study is that nearly all existing empirical work measures decentralisation at the *protocol layer* (consensus mechanism resources); *application-layer* governance decentralisation remains, in the authors' characterisation, "severely understudied." This gap directly motivates the thesis's contribution.

### 2.3.2 Application-Layer Governance Decentralisation

Jensen et al. (2021) represent the closest existing work to the thesis's empirical contribution at the application layer. Their study measures governance token concentration across four DeFi protocols (Uniswap, Compound, Curve, Yearn) using Gini coefficients, Nakamoto coefficients, and entropy measures, finding that initial token distribution methodology significantly impacts medium-term voting power concentration: protocols using airdrops achieve more distributed governance than those that sold tokens through Initial Coin Offerings (ICOs). The study also demonstrates that governance token *ownership* and active governance *participation* are frequently decoupled — a finding that motivates the thesis's separation of ownership-based and participation-based decentralisation proxies.

Rahimian and Hassan (2023) extend the measurement framework to multiple dimensions, proposing a decentralisation index that incorporates geographic distribution of voters, temporal consistency of participation, proposal diversity, and decision outcome diversity alongside the standard token distribution metrics. Protocols that score high on token distribution but low on temporal participation consistency display what the authors term "pseudo-decentralisation" — the appearance of distributed governance without its substance. This multidimensional framing supports the thesis's approach of coding governance across several variables (voting mechanism, multisig composition, timelock presence, ownership concentration) rather than relying on any single proxy.

---

## 2.4 Platform Economics and Market Concentration

### 2.4.1 DApps as Multi-Sided Platforms

The theoretical architecture for understanding DApp market structure is grounded in platform economics. Parker et al. (2016) establish the foundational framework: platforms create value by facilitating interactions between distinct user groups, generating indirect network externalities — the value a user on one side derives from participation by users on the other side. Winner-takes-most dynamics emerge because the platform with the largest network on either side attracts the most participants from the other side, compounding its advantage. These dynamics are well documented in traditional digital markets and provide the baseline from which DApp market structures either conform or deviate.

Trabucchi et al. (2020) extend this analysis to blockchain-enabled platforms through a multiple-case-study investigation of five Ethereum DApp marketplaces. Their central insight is that blockchain transforms traditional platform providers into *service providers* who leverage blockchain as Platform-as-a-Service (PaaS), with tokens replacing transaction fees as the primary externality mechanism. The concept of *value sharing* — where value is distributed to ecosystem participants rather than captured by a central operator — is identified as a fundamental departure from traditional platform economics. The paper introduces a four-variable framework characterising blockchain-enabled platforms: governance model, token type, user type, and value-sharing mechanism. Each of these dimensions corresponds to variables in the thesis dataset, making Trabucchi et al. (2020) the closest existing empirical paper to this study's research design.

Trabucchi and Buganza (2022) further propose the concept of *Hybrid Multi-Sided Platforms* to describe platforms that combine transaction-enabling and community-building functions simultaneously. DApps that run financial transactions on-chain while governing protocol upgrades through token voting exemplify this hybrid form: the same token serves as both medium of exchange and governance instrument. The "landlords with no lands" metaphor captures the economic position of governance token holders who extract value from protocol revenues without owning the underlying infrastructure — a characterisation that maps directly to the DApp governance structures catalogued in the thesis.

### 2.4.2 DeFi as a Platform Ecosystem

Schär (2021) provides the canonical taxonomy of the DeFi stack, characterising it as a five-layer architecture in which each layer depends on and builds upon the layers below it. The *composability* of DeFi protocols — the ability of one application to interact programmatically with another — creates winner-takes-ecosystem dynamics: protocols with high Total Value Locked (TVL) attract disproportionate integrations and user flows, amplifying initial advantages. This "money lego" dynamic explains why TVL concentration in the DeFi sector is even more extreme than user concentration, as liquidity attracts liquidity.

Aramonte et al. (2021), writing for the Bank for International Settlements, provide an institutional perspective on DeFi's structural risks that directly corroborates the thesis's empirical findings. Their analysis documents governance token ownership concentration, smart contract vulnerabilities, and the centralised intermediaries (oracles, bridges, user interfaces) that underpin ostensibly decentralised protocols. The BIS report's central claim — that effective control in most major DeFi protocols is concentrated in a small number of development teams and token whales, creating a "decentralisation illusion" — provides regulatory framing for interpreting the thesis's finding that 86.8% of the strict sample is not fully decentralised.

Leiponen et al. (2022) characterise the DApp economy as a new form of distributed innovation platform and argue that the limited governability of open blockchain platforms — compared to centralised app stores — creates conditions for generativity and unpredictable innovation, but also makes strategic direction-setting by any single actor nearly impossible. Their framework introduces *transaction validators* as a new economic actor type and argues that decentralisation shifts the locus of value capture from platform providers to token holders and validators. The thesis operationalises many of these constructs at scale.

### 2.4.3 NFT and Gaming Market Concentration

Ante (2021) documents power-law distributions in NFT market activity on Ethereum — volume and price are both highly concentrated around a small number of collections and creators, consistent with winner-takes-all dynamics in digital collectibles markets. Zhang et al. (2019) demonstrate that DApp adoption follows social contagion patterns analogous to product diffusion, with strong peer influence effects but rapid retention decay. These sector-specific studies provide empirical precedents for the concentration patterns observed in the thesis's results and support the interpretation that market dominance in the DApp ecosystem reflects network effect dynamics rather than purely merit-based selection.

---

## 2.5 Token Design and Incentive Structures

### 2.5.1 Tokenomics and Value Dynamics

Cong et al. (2021) provide the foundational theoretical model of token adoption and valuation dynamics. Tokens serve dual functions: as a *medium of exchange* for platform services (utility dimension) and as a *store of speculative value* (financial dimension). The model shows that the speculative component creates self-fulfilling adoption cycles — platform growth drives token appreciation, which attracts new users, which drives further growth — but also implies that when speculative cycles reverse, tokens provide weaker adoption incentives than traditional pricing mechanisms. This dual-function tension is directly observable in the thesis dataset: governance tokens in the strict sample are held partly for their voting rights and partly for capital appreciation, and the balance between these motivations shapes participation rates.

Li and Mann (2018) model the platform-building incentives created by ICOs, showing that token pre-sales enable DApps to solve the classic chicken-and-egg problem of two-sided markets by monetising future platform utility before the platform exists. However, ICOs create governance coordination problems: early investors who bought tokens at a discount have systematically different incentives from later users, because they benefit primarily from token appreciation rather than platform utility growth. This misalignment is most acute in governance token structures, where early investors' financial interests may diverge from the governance decisions that would maximise long-run platform value. The thesis's governance coding captures funding type as a variable, enabling an empirical test of whether ICO-funded DApps exhibit more centralised governance structures.

### 2.5.2 Governance Token Design and Control

Boreiko et al. (2019), analysing 253 ICOs, document how governance token design reflects founding teams' desire to retain control while projecting decentralisation. Most ICO tokens blur the regulatory distinction between utility tokens (access rights) and security tokens (ownership rights), with governance tokens occupying a legally ambiguous middle ground. Governance token design choices — total supply, initial distribution, vesting schedules, voting weight allocations — are strategic decisions, not merely technical ones.

Hassan and De Filippi's (2021) de jure/de facto decentralisation distinction is particularly salient in this context: a protocol may encode sophisticated on-chain governance mechanisms while the effective distribution of token supply ensures that a small number of founding-team wallets control outcomes. The thesis's governance coding explicitly captures both the formal mechanism and proxies for effective control to identify this gap.

Tan and Shi (2023) provide longitudinal evidence that governance design choices at protocol launch are predictive of long-term community health. Their study of 47 DAOs over three or more years finds that DAOs with higher governance participation rates and more diversified treasuries show better survival rates. This result motivates the thesis's inclusion of governance variables alongside financial metrics in analysing DApp market dynamics: governance is not merely a descriptive dimension but a structural variable associated with organisational viability.

---

## 2.6 Research Gaps and Thesis Positioning

The literature surveyed above, while growing rapidly, exhibits five systematic gaps that this thesis directly addresses.

**Gap 1: No large-scale, cross-category, manually coded governance dataset.** The empirical governance literature focuses almost exclusively on a small number of high-TVL DeFi protocols (Uniswap, Compound, Aave, Maker, Curve). Wu et al. (2019) analysed 734 DApps but without governance dimensions. Jensen et al. (2021) coded governance token distributions for four protocols; Fritsch et al. (2022) extended to approximately a dozen. No existing study combines governance classification (voting mechanism, multisig structure, ownership concentration, timelock presence) with market and adoption metrics across a representative cross-category DApp sample at the scale of hundreds of DApps. The thesis contributes a manually coded dataset of 855 DApps spanning DeFi, GameFi, NFT, Social, and Infrastructure categories, with governance variables merged with market capitalisation, TVL, active user, and transaction data from four independent sources.

**Gap 2: Governance measurement confined to the protocol layer.** Ovezik et al. (2025) explicitly identify application-layer governance decentralisation as "severely understudied." Existing decentralisation metrics have been applied primarily to consensus-layer resources. Even Jensen et al. (2021), the closest existing work, focuses on token distribution as a proxy rather than directly coding the governance mechanism in use, the multisig composition, or the timelock configuration. The thesis contributes application-layer governance decentralisation metrics for 855 DApps, enabling the first large-scale examination of whether DApp decentralisation correlates with market success, user adoption, or category membership.

**Gap 3: Missing empirical link between governance structure and market dynamics.** The platform economics literature (Parker et al., 2016; Trabucchi et al., 2020; Leiponen et al., 2022) discusses governance qualitatively but does not empirically link governance structure to market outcomes. The DeFi risk literature (Aramonte et al., 2021; Schär, 2021) documents governance concerns without quantitative analysis of the relationship between governance design and TVL, market capitalisation, or user adoption. The thesis contributes regression analysis linking governance variables to market dynamics outcomes, testing whether more decentralised governance is associated with higher adoption, greater TVL, or broader multi-chain deployment.

**Gap 4: Multi-chain ecosystem dynamics underexplored.** Most existing studies treat individual protocols or single blockchains as the unit of analysis. The multi-chain expansion of DeFi and Web3 — where a single DApp is simultaneously deployed on Ethereum, BNB Chain, Polygon, Arbitrum, and other networks — creates competitive dynamics not captured by single-chain analyses. Perego et al. (2023) note BNB Chain's leadership in DApp count without analysing the governance or ownership dimensions of multi-chain deployment strategies. The thesis contributes a multi-chain deployment variable for each of the 855 DApps, enabling analysis of whether governance structure, token design, or category predicts multi-chain adoption.

**Gap 5: The Censimento DApp methodology has not been published as peer-reviewed academic research.** Vella and Ghezzi's (2022) DApp census represents a pioneering effort at systematic DApp cataloguing in the Italian academic context but exists only as internal Observatory workshop material. The thesis extends this dataset substantially, documents its methodology with the transparency requirements of academic publication, and makes the data infrastructure available as a research artifact — establishing a reproducible baseline for future longitudinal studies of the DApp ecosystem.

Together, these five contributions position the thesis at the intersection of empirical DApp ecosystem research, governance measurement methodology, and platform economics. The study does not hypothesise causal mechanisms but establishes the empirical baseline needed for future hypothesis-testing work: a large, multi-source, cross-sector snapshot of governance, ownership, and market structure that allows the field to move beyond single-protocol case studies toward ecosystem-level inference.

---

## References for Chapter 2

Ante, L. (2021). Non-fungible token (NFT) markets on the Ethereum blockchain: Temporal development, cointegration, and interrelations. *Economics of Innovation and New Technology*.

Aramonte, S., Huang, W., & Schrimpf, A. (2021). DeFi risks and the decentralization illusion. *BIS Quarterly Review*, December 2021.

Atzori, M. (2017). Blockchain technology and decentralized governance: Is the state still necessary? *Journal of Governance and Regulation, 6*(1).

Boreiko, D., Ferrarini, G., & Giudici, P. (2019). Blockchain startups and prospectus regulation. *European Business Organization Law Review, 20*(4), 665–694.

Cong, L. W., & He, Z. (2019). Blockchain disruption and smart contracts. *Review of Financial Studies, 32*(5), 1754–1797.

Cong, L. W., Li, Y., & Wang, N. (2021). Tokenomics: Dynamic adoption and valuation. *Review of Financial Studies, 34*(3), 1105–1155.

Feichtinger, R., Fritsch, R., Vonlanthen, Y., & Wattenhofer, R. (2023). *The hidden shortcomings of (D)AOs: An empirical study of on-chain governance*. arXiv:2302.12125.

Fritsch, R., Müller, M., & Wattenhofer, R. (2022). Analyzing voting power in decentralized governance: Who controls DAOs? *Journal of Network and Computer Applications*.

Frontiers in Blockchain. (2023). A statistical examination of utilization trends in decentralized applications. *Frontiers in Blockchain*.

Hassan, S., & De Filippi, P. (2021). Decentralized autonomous organizations: Towards a blockchain-induced paradigm shift in the nature of financial intermediation. *Internet Policy Review, 10*(2).

Jensen, J. R., von Wachter, V., & Ross, O. (2021). *How decentralized is the governance of blockchain-based finance: Empirical evidence from four governance token distributions*. arXiv:2102.10096.

Kiayias, A., & Litos, O. (2020). A composable security treatment of the lightning network. *2020 IEEE Symposium on Security and Privacy*.

Leiponen, A., Thomas, L. D. W., & Wang, Q. (2022). The dApp economy: A new platform for distributed innovation? *Innovation, 24*(1), 1–26.

Li, J., & Mann, W. (2018). *Initial coin offerings and platform building*. SSRN Working Paper 3088726.

Ovezik, G., Karakostas, D., Kiayias, A., & Woods, D. (2025). *SoK: Measuring blockchain decentralization*. arXiv:2501.18279.

Parker, G., Van Alstyne, M., & Choudary, S. P. (2016). *Platform revolution: How networked markets are transforming the economy and how to make them work for you*. W. W. Norton & Company.

Perego, A., Sciuto, D., Portale, V., Bruschi, F., & Vella, G. (2023). *Blockchain & Web3: Time to build*. Politecnico di Milano, Blockchain & Distributed Ledger Observatory.

Rahimian, F., & Hassan, S. (2023). Measuring decentralization in blockchain-based voting systems: A multi-dimensional framework. *Frontiers in Blockchain*.

Schär, F. (2021). Decentralized finance: On blockchain- and smart contract-based financial markets. *Federal Reserve Bank of St. Louis Review, 103*(2), 153–174.

Srinivasan, B. S., & Lee, L. (2017). *Quantifying decentralization*. news.earn.com.

Tan, L., & Shi, J. (2023). *Evaluating DAO sustainability and longevity through on-chain governance metrics*. arXiv:2504.11341.

Trabucchi, D., Moretto, A., Buganza, T., & MacCormack, A. (2020). Disrupting the disruptors or enhancing them? How blockchain reshapes two-sided platforms. *Journal of Product Innovation Management, 37*(6), 552–574.

Trabucchi, D., & Buganza, T. (2022). Landlords with no lands: Exploring the tensions between Platform Thinking and Hybrid Multi-Sided Platforms. *European Journal of Innovation Management, 25*(6), 64–96.

Vella, G., & Ghezzi, D. (2022). *Workshop DApp & Web3*. Blockchain & Web3 Observatory, Politecnico di Milano. [Includes Censimento_Dapp_2022.xlsx]

Vella, G., & Ghezzi, D. (2024). *The Web3 playbook: New rules of the game for businesses*. Blockchain & Web3 Observatory, Politecnico di Milano.

Wu, K., Ma, Y., Huang, G., & Liu, X. (2019). *An empirical study of blockchain-based decentralized applications*. arXiv:1902.04969.

Zarir, A. A., Oliva, G. A., Jiang, Z. M., & Hassan, A. E. (2021). Developing cost-effective blockchain-powered applications: A case study of the gas usage of smart contract transactions in the Ethereum blockchain platform. *ACM Transactions on Software Engineering and Methodology, 30*(3).

Zhang, B., Cai, X., Zhao, X., & Feng, G. (2019). *Unraveling peer influence in DApp adoption: An empirical study using lifetime data from the Ethereum platform*. SSRN Working Paper 3387794.
