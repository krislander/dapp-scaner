# Chapter 6 — Conclusions

## 6.1 Summary of Contributions

This thesis set out to examine whether governance and ownership labels in the DApp ecosystem correspond to observable economic and adoption realities. The motivating concern was the governance accountability gap: a structural asymmetry in which retail participants, regulators, and researchers rely on self-reported decentralisation claims while the empirical evidence base for evaluating those claims remains thin. By constructing and analysing a cross-sectional dataset of 855 decentralised applications spanning 77 blockchain networks and 48 variables — with manual governance coding and multi-source market enrichment — this study provides an empirical benchmark at a scale not previously attempted in the literature.

Three principal contributions emerge from this work.

**An empirical governance benchmark.** The dataset, built from DappRadar activity rankings, DeFiLlama TVL records, CoinMarketCap pricing, and CoinGecko metadata, constitutes the most comprehensive cross-sectional governance census of the DApp ecosystem assembled to date. The dual analytic design — a loose universe of N = 834 and a strict high-signal universe of N = 68 — demonstrates that headline governance statistics are sensitive to data-quality thresholds, underscoring the importance of explicit eligibility criteria in ecosystem-level studies. In the strict sample, 86.8% of DApps are not fully decentralised under the applied coding criteria, 52.9% are company-owned, and the median governance score is 0.2833 on a 0–1 composite scale.

**Quantified observations about governance reality.** The study produces a set of precise, replicable observations that challenge the prevailing self-narrative of the Web3 sector. The top ten DApps in the strict sample account for 80.5% of total market capitalisation and 90.1% of unique active wallets — concentration ratios that match or exceed those documented in Web2 platform markets. The Gaming–DeFi engagement gap, where DeFi processes more than 100 times more economic value per user than Gaming despite comparable user counts, reveals that single-metric evaluation of DApp success is systematically misleading. The multi-chain deployment rate of 70.6% in the strict sample — versus 36.2% in the loose universe — demonstrates that data-quality gating materially changes the strategic picture of blockchain deployment choices.

**A reproducible measurement methodology.** The analytical pipeline — comprising seven Python scripts spanning data preparation, governance analysis, market structure, chain deployment, sector performance, conceptual synthesis, and thesis documentation — is fully documented and publicly available. The composite governance score constructed from governance type, ownership status, and decentralisation label provides a starting point for standardised measurement, and its positive correlation (r = 0.38) with log market capitalisation offers a first empirical signal, warranting further investigation, of whether governance design has competitive consequences.

---

## 6.2 Answers to the Research Questions

**RQ1: How do governance models and ownership structures co-vary across DApp ecosystem sectors?**

The data reveal a strongly non-random distribution of governance archetypes across sectors. DeFi protocols — which constitute 57.4% of the strict sample by application count and 54.3% by active users — show systematically higher governance scores and a greater prevalence of on-chain token governance and DAO structures than any other sector. Gaming applications, which represent 26.5% of the strict sample, cluster toward team-controlled governance and low governance scores. The AI DApp segment, despite the highest token adoption rate (80%), recorded zero fully decentralised applications in the loose universe. These co-variation patterns suggest that governance design is not freely chosen at the application level but is shaped by sector-specific incentives: DeFi's reliance on user trust and composable capital flows creates structural pressure toward credible decentralisation, while Gaming's user-acquisition and entertainment imperatives favour centralised product control.

**RQ2: Does the decentralisation label match actual governance mechanics at the application layer?**

The answer is: only partially, and the gap is substantial. In the strict sample, 13.2% of applications carry the fully decentralised label — a figure three times higher than in the loose universe (4.7%), indicating that data-rich, actively used DApps are more likely to have invested in governance infrastructure. However, even among applications that issue governance tokens, 26.5% of the strict sample retains team-controlled governance processes. Governance token issuance and formal community control are weakly coupled: token design appears to serve fundraising and user-incentive objectives more often than it reflects real shifts in decision-making authority. The co-occurrence of decentralisation labels with company ownership, while rare in absolute terms, illustrates that the label is applied inconsistently. Self-reported decentralisation should be treated as a hypothesis requiring corroboration against on-chain evidence, rather than as a verifiable fact.

**RQ3: What structural patterns emerge in capital and user concentration across blockchain verticals?**

Capital and user concentration follows a power-law distribution consistent with winner-takes-most dynamics. In the strict sample, the top ten DApps by market capitalisation hold 80.5% of total value; the top ten by user count hold 90.1% of all unique active wallets. The market capitalisation distribution exhibits a power-law exponent of approximately α = 0.61, comparable to concentration measures in social media and e-commerce platforms. This pattern persists across sectors: within DeFi, within Gaming, and across the aggregate sample. Permissionless entry — a foundational claim of blockchain infrastructure — does not prevent concentration at the application layer. Network effects, liquidity depth, brand recognition, and composability advantages are sufficient to produce highly concentrated outcomes in an open market.

**RQ4: How does multi-chain deployment correlate with market performance and adoption?**

Multi-chain deployment is positively associated with market valuation. In the loose universe, applications deployed on more than one chain show an average market capitalisation 1.3 times higher than single-chain counterparts. In the strict sample, 70.6% of applications have deployed across multiple chains, compared to 36.2% in the looser data-quality threshold. The directional association is consistent, but causal interpretation requires caution: multi-chain expansion may reflect the success and resources of already-large DApps rather than constituting a growth driver in itself. The data cannot distinguish between multi-chain deployment as a cause of adoption and as a consequence of the funding and engineering capacity that successful DApps accumulate over time. The finding is best read as a correlation that motivates future causal analysis rather than as evidence for a prescription.

---

## 6.3 Theoretical and Practical Implications

**Theoretical implications.** The findings contribute to two adjacent scholarly conversations. First, they extend the governance and institutional design literature on DAOs and token-based organisations (Barbereau et al., 2022; Tan et al., 2023) by providing cross-sectional evidence that community governance is an exception rather than a norm — one concentrated in high-activity, high-value DeFi protocols. The concept of progressive decentralisation (Aramonte et al., 2021) gains empirical texture: governance quality is positively correlated with market maturity, suggesting a lifecycle effect where established applications gradually develop governance infrastructure. Second, the market structure findings contribute to the platform economics literature on open and permissionless markets. Winner-takes-most concentration emerging in the absence of platform gatekeeping — documented here across 77 chains — challenges the intuition that open infrastructure is a sufficient condition for competitive market structure. The sources of concentration in DApp markets (liquidity depth, composability, reputation) are functionally analogous to network effects in traditional digital platform markets, even though the underlying infrastructure is fundamentally different.

**Practical implications for builders.** DApp development teams face a strategic trade-off between the credibility that genuine governance decentralisation provides and the operational agility that centralised control enables. The data suggest that governance token issuance without commensurate community control is a fragile strategy: it creates regulatory and reputational surface without delivering the trust premium that genuinely decentralised DeFi protocols appear to enjoy. Teams planning governance token launches should align token distribution, voting weight, and decision scope before launch rather than treating decentralisation as a deferred upgrade. Multi-chain deployment appears to be associated with higher valuations and should be evaluated as a growth lever early in the product roadmap, particularly for DeFi and marketplace applications where liquidity fragmentation is a primary competitive constraint.

**Practical implications for investors.** Unique active wallet counts, the most commonly cited DApp adoption metric, are an unreliable proxy for economic value at the ecosystem level. The Gaming–DeFi engagement gap — where Gaming attracts 12.67 million users in the strict sample generating low aggregate volume while DeFi processes $299.1 billion — demonstrates that per-sector benchmarks are essential. Investors should evaluate DApp traction using sector-adjusted metrics: volume per user and TVL efficiency for DeFi; retention and monetisation rates for Gaming; governance participation rates and proposal velocity for governance-facing applications. Funding history also proves to be a weak predictor of market performance: the median funded DApp trades below its funding round at 0.11× ROI, while several of the highest-valued applications — including the largest by market capitalisation in the strict sample — raised no external capital.

**Practical implications for regulators.** The gap between decentralisation labels and operational reality has direct regulatory relevance. If governance tokens are issued by team-controlled DApps with no genuine pathway to community control, they function more like equity instruments or promotional assets than governance mechanisms — raising questions about investor protection disclosure requirements. Regulatory frameworks that distinguish between formal token-based governance and substantive community control would be better calibrated to the evidence presented here. Index-based monitoring of governance concentration — using composite scores analogous to the one developed in this thesis — could provide regulators with a lighter-touch, data-driven alternative to entity-by-entity assessment.

---

## 6.4 Limitations

Several limitations bound the conclusions of this study and should be borne in mind when interpreting the findings.

**Temporal snapshot.** The dataset represents a point-in-time cross-section collected in November 2025. DApp governance structures evolve, token distributions shift, and protocol upgrades alter on-chain voting powers continuously. The observed governance distribution reflects a moment in an ongoing process rather than a steady state. The finding that 86.8% of DApps are not fully decentralised does not imply that this proportion is stable or increasing; without longitudinal data it is not possible to determine whether the ecosystem is converging toward or diverging from decentralisation ideals.

**Survivorship and selection bias.** The base sample is drawn from DappRadar's top-500 UAW rankings, augmented by manual additions. DApps that failed, were delisted, or fell below activity thresholds before November 2025 are not represented. The strict universe compounds this by requiring positive market capitalisation and high activity signals, meaning that the N = 68 applications analysed in detail are those that have already demonstrated market success. Findings about governance-performance associations in this sample cannot be generalised to the full population of launched DApps.

**Manual governance coding.** The governance type, ownership status, and level of decentralisation variables are manually coded from publicly available documentation, DAO forum records, and smart contract inspection. This process is subject to coder interpretation, documentation incompleteness, and project self-disclosure. On-chain smart contract analysis — not conducted here — would provide a more objective measure of actual administrative key permissions and upgrade authority.

---

## 6.5 Future Research Directions

The empirical foundation constructed in this thesis opens several productive research directions.

**Longitudinal governance tracking.** The most significant gap left open is the temporal dimension. A panel dataset tracking the same DApps across multiple quarters would allow direct testing of the progressive decentralisation hypothesis: whether team-controlled applications transition toward community governance as they mature, and whether governance maturity correlates with improved economic performance over time. Repeated coding of governance state at six-month intervals would be feasible given the pipeline developed here.

**On-chain governance participation analysis.** The current study codes governance structure from documentation and metadata. A complementary analysis using on-chain vote records — available for all DAO-governed protocols deploying Governor Bravo or comparable frameworks — would quantify actual participation rates, voting concentration, and proposal throughput. This would allow direct measurement of the gap between formal governance rights and exercised governance power: an important second-order dimension of the decentralisation question.

**User behaviour and retention analysis.** The 100× gap in economic value per user between Gaming and DeFi applications suggests radically different user motivation profiles. Wallet-level analysis tracing user retention, switching behaviour, and cross-application engagement across sectors would enrich the adoption picture considerably and shed light on whether high user counts in Gaming translate to durable economic activity.

**Cross-chain interoperability effects.** The multi-chain deployment correlation identified in RQ4 raises a causal question that this dataset cannot resolve. As cross-chain bridging and interoperability infrastructure matures — through protocols such as LayerZero, Wormhole, and native chain abstraction layers — a quasi-experimental analysis exploiting variation in the timing and depth of multichain launches could provide more credible estimates of the causal effect of chain expansion on user growth and market capitalisation.

**Governance design experiments and natural experiments.** Several DApps have undergone governance transitions — from team-controlled to DAO, from off-chain Snapshot voting to on-chain governance, from single-sig to multisig administration — in ways that approximate natural experiments. Event-study methods applied to market capitalisation and user activity around these transitions would provide some of the most direct evidence available on whether governance quality has causal market consequences.

---

*Word count: approximately 1,900 words*

---

### References (Chapter 6 — cited)

Aramonte, S., Huang, W., & Schrimpf, A. (2021). DeFi risks and the decentralisation illusion. *BIS Quarterly Review*, December 2021.

Barbereau, T., Smethurst, R., Papageorgiou, O., Rieger, A., & Fridgen, G. (2022). DeFi, not so decentralized: The measured distribution of voting rights. In *Proceedings of the 55th Hawaii International Conference on System Sciences*.

Tan, J., Shrestha, Y. R., & Schäfer, L. (2023). The governance of decentralized autonomous organizations: A study of voting patterns. *Journal of Strategic Information Systems*, *32*(3), 101774.
