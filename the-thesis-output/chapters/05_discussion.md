# Chapter 5: Discussion

## 5.1 Overview

The results presented in Chapter 4 reveal a set of structural tensions that resist easy resolution. This chapter interprets those findings in light of the broader Web3 and blockchain governance literature, examining seven interlocking paradoxes that emerge from the strict-eligible sample of 68 high-signal DApps. The discussion proceeds from governance structure to market concentration, from engagement asymmetry to capital efficiency, before arriving at the multi-chain deployment question. It concludes with the implications these patterns carry for theory and practice, and with an honest account of the study's limitations.

The overarching argument is this: the blockchain layer is technically decentralised, but the application layer built on top of it is not. This disjunction — infrastructure decentralisation coexisting with application-layer centralisation — is not incidental. It reflects deliberate design choices, commercial incentives, and the practical constraints of early-stage product development. Whether it represents a failure of the Web3 promise or an expected phase in progressive decentralisation is the central question this chapter attempts to answer.

---

## 5.2 The Decentralisation Paradox (DIS-01)

The most arresting finding of the analysis is the gap between the infrastructure promise of Web3 and the governance reality of the DApps built on that infrastructure. Among the 68 DApps that pass strict eligibility criteria — requiring meaningful user bases, measured market activity, and complete governance fields — only 13.2 per cent carry a fully decentralised label. A further 52.9 per cent are company-owned and 26.5 per cent are team-controlled. The remaining share occupies intermediate governance categories that fall short of community ownership.

This is the decentralisation paradox at scale: 86.8 per cent of high-signal DApps are *not* fully decentralised, despite being deployed on permissionless blockchains. The Ethereum Virtual Machine, Solana's runtime, or BNB Chain's validator network may be genuinely decentralised by any technical measure, yet the contracts they execute and the interfaces through which users interact with them remain under concentrated control.

Several explanations are available. The first is developmental: nascent projects rationally retain control while iterating toward product–market fit, with the intention of transferring governance to a community once the protocol is sufficiently mature and the token distribution sufficiently broad. This "progressive decentralisation" pathway is explicitly articulated by influential practitioners in the field (Dixon, 2021) and is not inherently dishonest. The snapshot character of this dataset cannot distinguish a genuinely transitioning project from one that will remain centralised indefinitely.

The second explanation is commercial: governance retention allows founding teams to respond quickly to exploits, pivot product direction, and negotiate regulatory compliance — advantages that pure on-chain governance cannot easily replicate. From this perspective, centralisation is not a betrayal of Web3 ideals but an engineering trade-off that larger, more mature protocols can afford to abandon.

The third explanation is less charitable: the decentralisation label functions as a marketing asset rather than a governance commitment. It grants projects the rhetorical benefits of the Web3 movement — censorship resistance, trustlessness, community ownership — without the operational costs of actually distributing power. The data cannot adjudicate between these explanations at the aggregate level, but the co-occurrence patterns described in DIS-02 below lend support to the third.

What the data do establish is that the Web3 ecosystem, measured at the application layer, is structurally far more centralised than its public narrative acknowledges. This should inform how researchers, regulators, and users evaluate DApp governance claims.

---

## 5.3 Labelling Versus Mechanics (DIS-02)

The decentralisation paradox is sharpened by a second observation: governance labels and governance mechanics frequently diverge. Two patterns stand out in the cross-tabulation analysis.

First, some DApps issue tokens classified as governance assets while the operational governance process remains team-controlled. The token design — voting rights, delegation mechanisms, proposal thresholds — signals democratic intent, while the actual decision flow runs through a founding team or a small committee. This is not a classification error; the token may genuinely carry voting rights on paper, yet the combination of token concentration (discussed in DIS-05), high quorum requirements, and team veto powers renders those rights effectively inactive.

Second, certain DApps are labelled "decentralised" in their marketing while a company entity retains ownership of the smart contracts. The company can, in principle, upgrade the contracts, pause the protocol, or redirect funds. This is governance by company decision, not community consensus — regardless of the label applied.

These patterns suggest that token design, in a significant share of cases, serves capital formation more than community empowerment. Initial token offerings and liquidity programmes attract capital and generate network effects; the governance framing justifies the token's existence within regulatory grey zones. Once the capital is secured and the protocol gains traction, the incentive to transfer genuine governance authority weakens. Founding teams that have built something valuable are not eager to cede control of it.

The analytical implication is that governance labels alone are an unreliable proxy for governance reality. Future research and regulatory frameworks should focus on governance mechanics — upgrade key holders, multisig composition, timelock durations, token distribution among non-team addresses — rather than governance self-descriptions.

---

## 5.4 Concentration Mirrors Traditional Technology (DIS-03)

One of the foundational claims of the blockchain movement is that permissionless infrastructure prevents the monopolistic concentration that defines Web2 platforms. If anyone can fork a protocol, deploy a competitor, and attract users without seeking permission from an incumbent, winner-takes-all outcomes should be self-limiting. The results of this study challenge that claim.

In the strict sample, the top ten DApps by market capitalisation account for 80.5 per cent of total market cap. By user base, concentration is even more extreme: the top ten DApps attract 90.1 per cent of active wallets. These figures are broadly comparable to — and in the user dimension more severe than — the concentration ratios observed in traditional platform markets. The power law exponent estimated across the full 855-DApp dataset (α ≈ 0.61) is consistent with winner-takes-most dynamics in social media and digital marketplaces (Clauset, Shalizi, and Newman, 2009).

Permissionless infrastructure, it appears, does not flatten winner-takes-most dynamics; it merely relocates them. Several mechanisms explain this. Network effects are as powerful in DeFi liquidity pools as in social networks: a DEX with deeper liquidity offers better prices, attracting more traders, which deepens liquidity further. The same self-reinforcing dynamic applies to user attention: protocols with large user bases generate more fee revenue, fund more marketing and developer relations, and attract more integrations — all of which reinforce their lead.

Trust is a further amplifier. In an environment characterised by smart contract exploits, rug pulls, and oracle manipulation, users concentrate on protocols with established track records, audited codebases, and high TVL — precisely because size functions as a credibility signal. Newcomers face not only technical competition but a trust deficit that takes years to overcome.

The implication is that decentralised infrastructure is a necessary but not sufficient condition for a decentralised application economy. Without active intervention — whether through protocol design, regulatory constraint, or shifts in user behaviour — the DApp economy reproduces the concentration patterns of the industries it set out to disrupt.

---

## 5.5 The Engagement Gap (DIS-04)

The strict sample reveals a striking discontinuity between user volume and economic value across application verticals. Gaming DApps attract approximately 12,670,611 active users while generating modest financial throughput. DeFi DApps, by contrast, process $299.1 billion in volume with a smaller user base. The value-per-user gap between these two verticals exceeds 1,000 times.

This disparity exposes the inadequacy of user count as a universal success metric. In the gaming context, active wallets often represent players engaged in play-to-earn mechanics, NFT transactions, or in-game economies with real but modest monetary value. The act of counting a wallet as "active" may correspond to a user earning fractional dollars per session. In DeFi, a single wallet might represent an institutional participant cycling tens of millions of dollars through liquidity positions. The aggregation of these two populations into a single "DApp user" category obscures more than it reveals.

This has direct implications for how DApp performance should be measured and reported. Academic and industry research frequently cites active wallet counts as the primary adoption indicator, implicitly treating a gaming wallet and a DeFi wallet as equivalent units of economic engagement. The results here suggest this equivalence is false by several orders of magnitude.

A more defensible measurement framework would differentiate between engagement volume (wallet count), economic throughput (volume, TVL), and capital efficiency (volume per user, TVL per user, revenue per transaction). A DApp strategy optimised for user count — as many gaming and social DApps appear to be — is targeting a fundamentally different objective than one optimised for capital deployment. Neither objective is inherently superior, but conflating them produces misleading league tables and misallocates analytical attention.

The engagement gap also raises questions about the sustainability of user-acquisition strategies in gaming. If a high user count does not translate into proportionate economic activity, the business model depends on mechanisms other than direct financial value — token speculation, NFT appreciation, or advertising revenue — that may prove fragile.

---

## 5.6 Governance Realism Under Concentration (DIS-05)

Token-based governance is frequently presented as a mechanism for aligning the incentives of diverse stakeholders in decentralised protocols. The principle is straightforward: token holders vote on protocol parameters, fee structures, treasury allocations, and upgrades, with voting power proportional to tokens held. In practice, the market concentration described in DIS-03 interacts with token distribution to produce outcomes that resemble plutocracy more than democracy.

If the top ten DApps by market capitalisation hold 80.5 per cent of value, and if governance token distribution within those projects is similarly concentrated — as the literature on token distribution consistently suggests (Fritsch, Fritsch, and Wattenhofer, 2022) — then effective voting control rests with a small number of large holders. These may include founding teams, early investors, protocol treasuries, and a handful of large funds. Retail token holders, though formally enfranchised, face a coordination problem that renders their participation practically irrelevant on contested votes.

The on-chain voting records of major DeFi governance systems support this picture. Proposals frequently pass with participation rates below five per cent of eligible tokens, with the decisive votes concentrated in three to five wallets (Barbereau et al., 2022). The governance mechanism is real but the democratic property it is purported to deliver is largely fictive.

This does not mean governance tokens are without value. They provide a coordination mechanism, a dispute resolution channel, and a legitimising narrative for protocol decisions. But researchers and practitioners should be clear-eyed about what on-chain governance achieves in a concentrated token environment. The relevant question is not whether token voting is technically possible but whether the distribution of voting power is compatible with the community-governance narrative attached to it.

A realistic governance model for the current concentration reality would acknowledge that large holders will dominate contentious votes, design delegation mechanisms that allow liquid democracy across smaller holders, and invest in coordination infrastructure — forums, working groups, temperature checks — that gives non-dominant token holders meaningful input before formal votes are called.

---

## 5.7 Funding Efficiency (DIS-06)

Venture capital has been a defining feature of the Web3 ecosystem since at least 2017. The implicit model is straightforward: VCs identify promising protocols, provide capital for development and market entry, and profit from token appreciation as the protocol grows. The results of this analysis challenge the efficacy of this model.

Among the strict-eligible sample, only 13 DApps raised venture capital. The median funding return on investment for those DApps is 0.1x, meaning that the median funded DApp is trading at a tenth of its aggregate funding value. More striking still is the prevalence of unfunded DApps that exceed the market capitalisation of their venture-backed peers: 29.4 per cent of unfunded DApps in the strict sample outperform the median funded DApp by market cap (ANO-MKT-03).

Several interpretations are available. The first is that VC participation in DApps is a lagging indicator of hype cycles rather than a forward indicator of product quality. Funding rounds in Web3 frequently follow token price appreciation rather than precede it; projects are valued on speculative momentum at the time of investment, and the multiple is then compressed as token prices revert.

The second is that the operational characteristics of a successful DApp — open source codebase, permissionless access, community-driven distribution — are less amenable to the value-appropriation mechanisms that make VC backing valuable in traditional startups. If any developer can fork the protocol, the competitive moat that justifies a high entry valuation may quickly erode.

The third interpretation emphasises selection bias in VC targeting: funds may systematically favour projects with compelling founders and high-profile ecosystems over those with genuine product–market fit, and the market is capable of identifying genuine utility independently of institutional endorsement.

Whatever the causal mechanism, the implication for DApp builders is that raising venture capital should not be treated as a prerequisite for success, nor should it be confused with validation of the underlying product. Capital is useful for hiring, security audits, and market access, but the data do not support the hypothesis that it reliably predicts long-term market performance.

---

## 5.8 Multi-Chain Strategy: Correlation or Causation? (DIS-07)

The final structural pattern to examine concerns deployment strategy. Among the strict sample, 70.6 per cent of DApps are deployed on multiple blockchains. Legacy analysis within the same dataset indicates that multi-chain DApps command a 1.3x median market capitalisation premium over single-chain peers. This is a substantial and persistent premium.

The causal interpretation of this premium is, however, unclear. Two competing narratives exist.

The first is that multi-chain deployment *causes* superior performance through expanded addressable market, access to chain-specific liquidity pools, and reduced dependency on any single chain's ecosystem health. Under this view, the decision to deploy across chains is a genuine value driver that small teams should emulate.

The second is that multi-chain deployment is an *effect* of prior success rather than its cause. Deploying across multiple chains requires security audits for each deployment, bridge infrastructure, chain-specific developer relations, and ongoing maintenance overhead. These are non-trivial costs that well-capitalised, high-revenue protocols can absorb but that early-stage projects cannot. Under this view, the observed premium reflects survivorship bias: only protocols that have already achieved significant market positions can afford multi-chain expansion, and those protocols command higher valuations for reasons independent of their deployment strategy.

The data in this study cannot discriminate between these mechanisms. What the analysis does establish is that the association between multi-chain deployment and market capitalisation is robust across both the loose and strict samples. Practitioners should treat this as a plausible growth lever while remaining alert to the reverse-causality and survivorship-bias explanations. Longitudinal data tracking deployment timing relative to valuation milestones would be required to establish directionality.

For small, single-chain teams, the implication is pragmatic: the multi-chain premium, if causal, may require a scale of resources that is not yet available to them. A well-executed single-chain product likely provides a better foundation for eventual multi-chain expansion than a prematurely distributed architecture that strains limited engineering capacity.

---

## 5.9 Implications for Theory and Practice

### 5.9.1 Blockchain Governance Literature

This study contributes to a growing body of empirical work that challenges the conceptual frameworks inherited from cypherpunk and libertarian political philosophy, in which decentralisation is treated as both technically inevitable and normatively desirable. The findings suggest that neither property holds at the application layer.

Decentralisation is not technically inevitable: the same permissionless infrastructure that enables censorship-resistant computation also enables centralised applications, and developers systematically choose the latter in commercially sensitive contexts. This should prompt governance scholars to shift their unit of analysis from the protocol layer — where decentralisation is structurally enforced by consensus mechanisms — to the application layer, where it is a design choice.

The normative question is equally complicated. The engagement gap between gaming and DeFi suggests that users flock to centralised DApps (ANO-ADP-01) and to high-volume, low-decentralisation protocols without apparent regard for governance structure. If user demand does not reward decentralisation, the governance literature must account for why decentralisation should be pursued as a design goal beyond its symbolic value for regulatory positioning.

The concentration findings align with network economics scholarship on platform markets (Rochet and Tirole, 2003; Parker, Van Alstyne, and Choudary, 2016) and suggest that the DApp economy is best understood through the lens of two-sided markets rather than through the lens of open-source software ecosystems, which is how it is typically framed. Liquidity, users, and developer attention are multi-sided goods that exhibit the same tipping dynamics in DApp markets as in search, social media, and e-commerce.

### 5.9.2 Practical Implications for DApp Builders

For practitioners, five actionable observations emerge from this analysis.

First, the success of a DApp cannot be measured by a single metric. User count, volume, TVL, market capitalisation, and governance score capture different dimensions of performance that trade off against one another depending on the application vertical. Builders should define success metrics appropriate to their economic model before seeking external validation.

Second, governance design should precede token issuance. The pattern of governance tokens issued before governance mechanics are operational — and team control retained long after token distribution — creates a credibility deficit that is difficult to recover. Projects that intend to transfer governance should design the transfer pathway into the protocol from the outset.

Third, capital efficiency matters more than capital raised. Unfunded DApps regularly outperform VC-backed peers in market capitalisation. Builders should be sceptical of the implicit narrative that raising a funding round constitutes validation or guarantees competitive advantage.

Fourth, multi-chain expansion should be sequenced, not simultaneous. Given the cost structure of multi-chain deployment and the evidence that the premium may reflect selection rather than causation, early-stage teams should achieve protocol stability on a primary chain before incurring the overhead of additional deployments.

Fifth, on-chain governance is a long-term project, not a launch feature. Given token concentration realities, meaningful governance requires sustained investment in coordination infrastructure — grants, forums, working groups, delegation tooling — that most early-stage projects are not equipped to maintain. Treating governance as an operational commitment rather than a marketing claim would improve the credibility of the Web3 ecosystem overall.

---

## 5.10 Limitations

This study is subject to several limitations that constrain the generalisability of its findings and should guide interpretation.

**Snapshot timing.** The dataset reflects a single cross-sectional export from November 2025. Market capitalisation, TVL, user counts, and governance scores are volatile metrics that can shift substantially over weeks. Findings regarding concentration, funding ROI, and multi-chain premium should be understood as characterising the ecosystem at one point in time rather than as stable structural properties. Longitudinal replication would be required to establish the durability of these patterns.

**Survivorship bias.** The strict eligibility criteria — requiring ≥4 positive activity signals, ≥10,000 users, and positive market cap or TVL — systematically exclude failed projects, abandoned protocols, and early-stage DApps that never achieved measurable traction. The 68-DApp strict sample represents the observable, successful tail of a much larger population that includes many non-starters. Concentration ratios, governance patterns, and funding ROI figures are therefore calculated over a sample that has already survived a stringent selection process. The true state of the ecosystem — including all projects that attempted and failed — is likely more concentrated and less capital-efficient than the strict sample suggests.

**Manual coding subjectivity.** Governance labels (decentralised, team-controlled, company-owned, DAO) and token type classifications (governance, utility, none) were assigned through a combination of automated heuristics and manual review. These categories are not crisply defined in the industry, and the same DApp might be coded differently by two careful analysts depending on how they weight different governance indicators. Sensitivity analysis on coding decisions was not conducted for this study; future work should apply inter-rater reliability testing to governance classification.

**Data source coverage.** The dataset integrates data from DappRadar, CoinGecko, and DeFiLlama, supplemented by manual enrichment. Each source applies its own eligibility, coverage, and measurement conventions. DappRadar's user count methodology, for instance, counts unique active wallets within a rolling window; this definition may differ from what other researchers mean by "active users." Protocols that are not indexed by these platforms — particularly those operating on newer or less-covered chains — are absent from the analysis.

**Reverse causality.** Several findings in the discussion involve relationships where causal direction is ambiguous — most clearly in the multi-chain deployment premium but also in the governance-score/market-cap correlation reported in the legacy analysis (r = 0.38). These associations are descriptive. Drawing causal inferences from them would require instrumental variable approaches or natural experiments that are beyond the scope of this cross-sectional study.

---

## 5.11 Summary

The discussion has traced seven structural tensions through the lens of blockchain governance theory, market economics, and practitioner reality. The decentralisation paradox, the divergence of governance labels from governance mechanics, the reproduction of traditional tech concentration patterns, the 1,000-fold engagement gap between verticals, the limits of on-chain democracy under concentrated token ownership, the failure of venture capital as a reliable performance predictor, and the ambiguous causal status of the multi-chain premium — each of these findings challenges a widely held assumption about how DApp markets work.

Taken together, they suggest that the DApp ecosystem is best understood not as a technological disruption of traditional market structures but as a reconfiguration of those structures under new institutional rules. Permissionless infrastructure lowers entry barriers without flattening winner-takes-most dynamics. Governance tokens distribute formal rights without redistributing effective power. Decentralisation is more frequently a design aspiration or a regulatory posture than an operational reality.

None of this is to say the Web3 ecosystem is without distinctive properties or meaningful innovations. The possibility of verifiable, composable, and non-custodial financial infrastructure is genuinely novel. But the application layer sitting atop that infrastructure, as measured in this study, has not yet made good on its most ambitious governance and distribution claims. Whether it does so in future iterations is an empirical question that longitudinal research is better positioned to answer than this snapshot can.
