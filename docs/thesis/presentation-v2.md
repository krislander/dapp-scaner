---
title: "Thesis Defense Presentation — v2"
---

# Thesis Defense Presentation — v2

**Thesis Title:** Decentralised Applications in Focus: Governance, Market Structure, and Adoption Patterns

**Institution:** Politecnico di Milano — Master of Science, Digital Innovation Observatory, Blockchain

**Duration:** 10–12 minutes · 11 slides · 5 phases

**Dataset:** 855 DApps · 77 blockchains · 48 variables · November 2025

---

### Slide 1 – Phase 1: Introduction & Relevance

**Descriptive Slide Title:** "The DApp Ecosystem Promises Decentralisation — But Does It Deliver?"

**Visual Layout Description:** Full-slide split composition. Left half: a stylised blockchain network diagram with nodes radiating outward, symbolising the promise of decentralisation. Right half: a funnel graphic narrowing from "855 DApps" at the top to "only 13.2% fully decentralised" at the bottom — creating visual tension between promise and reality. The central research question appears as a single bold statement across the bottom of the slide.

**Key Slide Takeaways (2–3 bullets max):**

- The DApp ecosystem spans 855+ applications across 77 blockchains, yet the fundamental governance claim — that blockchain-based apps redistribute power to users — remains empirically untested at scale (Schär, 2021; Aramonte et al., 2021).
- Retail investors, regulators, and researchers rely on self-reported governance labels with no large-scale benchmark to verify them — this is the governance accountability gap.
- **Research Question:** *Do governance and ownership labels in the DApp ecosystem correspond to observable economic and adoption realities?*

**Speaking Script (~50 seconds):**

"Decentralised applications — DApps — promise to redistribute control from platform owners to their users. By November 2025, this ecosystem had grown to over 855 active applications across 77 blockchains, with 90 million users and 115 billion dollars in locked value. But here is the tension motivating this thesis: decentralisation is simultaneously a technical descriptor and a marketing proposition. Projects announce governance tokens and DAO structures as signals of community control — but does the label match the reality? The empirical evidence for answering that question at scale simply did not exist. This thesis addresses that gap through one central research question: do governance and ownership labels in the DApp ecosystem correspond to observable economic and adoption realities?"

---

### Slide 2 – Phase 1: Introduction & Relevance

**Descriptive Slide Title:** "Four Questions That Frame the Governance Accountability Gap"

**Visual Layout Description:** A clean four-quadrant layout, each quadrant visually self-contained. Each contains one research question as a single plain-language sentence with a small thematic icon: a pie chart for RQ1 (governance distribution), a magnifying glass for RQ2 (label vs. reality), a bar chart for RQ3 (concentration), and a chain-link icon for RQ4 (multi-chain). No bullet lists — each quadrant speaks for itself.

**Key Slide Takeaways (2–3 bullets max):**

- RQ1: How do governance models co-vary across DApp sectors?
- RQ2: Does the "decentralised" label match actual governance mechanics?
- RQ3 & RQ4: What concentration patterns emerge, and how does multi-chain deployment relate to performance?

**Speaking Script (~40 seconds):**

"Four research questions guide the work. First: how are governance models distributed across sectors — do DeFi protocols cluster around different archetypes than gaming or AI applications? Second — the central tension — does the decentralisation label actually match the governance mechanics underneath? Third: does this ecosystem reproduce the winner-takes-most concentration we see in traditional tech? And fourth: does deploying across multiple blockchains correlate with better market performance? Together, these four questions frame a coherent inquiry into the gap between what Web3 claims and what the data show."

---

### Slide 3 – Phase 2: Literature Review

**Descriptive Slide Title:** "Five Research Gaps the Literature Left Open"

**Visual Layout Description:** A horizontal pillar diagram showing five coloured blocks, each representing one research gap. Each block carries a short label and the key supporting citation. Blocks are arranged from the most established gap (left) to the most novel (right). An arrow from all five pillars converges on a single block labelled "This Thesis" at the right edge — visually showing how the study fills all five gaps simultaneously.

**Key Slide Takeaways (2–3 bullets max):**

- No large-scale, cross-category, manually coded governance dataset existed — prior studies examined 4–9 protocols at most (Barbereau et al., 2023; Jensen et al., 2021).
- Governance decentralisation measurement has been confined to the protocol and consensus layer; application-layer governance is "severely understudied" (Ovezik et al., 2025).
- The empirical link between governance structure and market dynamics — TVL, market cap, adoption — has never been quantified at ecosystem scale (Aramonte et al., 2021; Schär, 2021).

**Speaking Script (~1 minute):**

"The literature review identified five systematic gaps. First, no large-scale governance dataset spanning multiple sectors existed — the deepest prior studies examined four to nine protocols. Second, decentralisation measurement has been confined to the consensus layer: who validates blocks, not who controls the application. Ovezik and colleagues in their 2025 Systematization of Knowledge paper explicitly call application-layer governance 'severely understudied.' Third, no one had empirically linked governance structure to market outcomes like TVL or market capitalisation at scale. Fourth, multi-chain dynamics were underexplored. And fifth, no reproducible methodology for large-scale DApp cataloguing with governance dimensions existed in the peer-reviewed literature. This thesis addresses all five."

---

### Slide 4 – Phase 3: Methodology

**Descriptive Slide Title:** "855 DApps, Four Data Sources, and a Manual Governance Coding Layer"

**Visual Layout Description:** A data pipeline flowchart occupying the full slide. Four source boxes across the top — DappRadar (activity data), DeFiLlama (TVL), CoinMarketCap (token market data), CoinGecko (cross-validation) — each with a small logo or icon, feeding via arrows into a central node: "855 DApps · 48 Variables · 77 Chains." Below that node, three branches descend: left branch "Record Linkage & Tag Aggregation," centre branch "Manual Governance Coding — 3 ENUM variables," right branch "Sample Construction" splitting into the loose universe (N=834) and strict universe (N=68). Clean, minimal, no text paragraphs.

**Key Slide Takeaways (2–3 bullets max):**

- Multi-source pipeline integrating on-chain activity data, TVL, and token market data with manual governance annotations across 855 DApps spanning 77 blockchain networks.
- Three governance variables hand-coded per DApp with explicit decision rules: governance type (7 levels), ownership status (6 levels), decentralisation level (3 tiers) — validated with intra-coder reliability κ = 0.79–0.88 (Agresti, 2002).
- Dual-universe design: loose sample (N=834) for broad baseline; strict sample (N=68) with quality gates — at least 4 of 5 activity signals positive, 10,000+ active wallets, positive valuation anchor — for all primary findings.

**Speaking Script (~1 minute 30 seconds):**

"The methodology combines four data sources into a single pipeline. DappRadar provides the seed population — the top 500 DApps by unique active wallets — plus activity metrics. DeFiLlama supplies total value locked. CoinMarketCap and CoinGecko contribute token market data and cross-validation.

But the critical innovation is the manual governance coding layer. For all 855 DApps, I hand-coded three governance variables using explicit decision rules documented in the thesis: governance type — on a seven-level scale from 'no governance' to 'DAO with timelock'; ownership status — six categories from company-owned to DAO-owned; and overall decentralisation level — centralised, semi-decentralised, or decentralised.

To test coding consistency, I re-coded a random 30-DApp sample after a two-week interval. Cohen's kappa ranged from 0.79 to 0.88 — substantial agreement.

The analysis then uses a dual-universe design. A broad loose sample of 834 DApps for baseline sensitivity tests, and a strict sample of 68 DApps passing rigorous quality gates. The strict sample is the primary vehicle for all findings you will see in the next slides."

---

### Slide 5 – Phase 4: Results & Discussion

**Descriptive Slide Title:** "86.8% of High-Signal DApps Are Not Fully Decentralised"

**Visual Layout Description:** A large donut chart dominates the centre of the slide, showing the decentralisation breakdown of the strict sample (N=68): a small green slice for "Fully Decentralised" (13.2%), a large amber slice for "Semi-Decentralised" (77.9%), and a red slice for "Centralised" (8.8%). Percentages only — no raw counts inside the chart. To the right, a compact side-by-side comparison of the loose vs. strict universe on three indicators: % fully decentralised, % company-owned, and median governance score — visually reinforcing how the picture changes with data quality.

**Key Slide Takeaways (2–3 bullets max):**

- Central finding: only 9 of 68 strict-sample DApps qualify as fully decentralised; 86.8% retain meaningful centralisation despite operating on permissionless blockchains.
- The strict sample actually shows better governance than the broad population — median score 0.283 vs. 0.067 — yet remains predominantly company-owned at 52.9% (Atzori, 2017; Aramonte et al., 2021).
- Application-layer centralisation is the norm: blockchain infrastructure decentralisation does not automatically produce decentralised governance at the application layer.

**Speaking Script (~1 minute):**

"This is the headline finding. Of the 68 DApps that passed the strict quality gate, only nine — 13.2 per cent — qualify as fully decentralised. That means 86.8 per cent retain meaningful centralisation, despite being built on permissionless blockchains.

The strict sample actually shows better governance than the broader population — the median governance score quadruples. But even these well-established protocols remain predominantly company-owned at 53 per cent.

This is what I call the decentralisation paradox: the blockchain infrastructure may be technically decentralised, but the applications built on top of it are not. Three explanations emerge: progressive decentralisation as a deliberate lifecycle strategy, commercial incentives to retain operational agility, and — less charitably — decentralisation functioning as a marketing label rather than a governance commitment.

Let me show you how this concentration extends to market structure."

---

### Slide 6 – Phase 4: Results & Discussion

**Descriptive Slide Title:** "Winner-Takes-Most: The Top 10 DApps Control 80% of Market Value"

**Visual Layout Description:** Dual-panel slide. Left panel: two horizontal stacked bars comparing top-10 share vs. the remaining 58 DApps — one bar for market capitalisation (80.5% / 19.5%), one for active users (90.1% / 9.9%). The top-10 portion is coloured boldly; the rest is muted. Right panel: a log-log scatter plot of rank vs. market capitalisation with the power-law fit line (α ≈ 0.61) overlaid, dots colour-coded by governance level (green / amber / red). Clean axis labels, no dense annotations.

**Key Slide Takeaways (2–3 bullets max):**

- Top-10 concentration: 80.5% of market capitalisation and 90.1% of user activity — ratios comparable to or exceeding Web2 platform markets (Parker et al., 2016).
- The power-law exponent (α ≈ 0.61) confirms winner-takes-most dynamics; permissionless entry does not prevent concentration at the application layer.
- Governance quality and market scale co-occur: Spearman r = 0.38 between governance score and log market cap — suggesting protocols that invested in governance are disproportionately those that reached scale.

**Speaking Script (~1 minute):**

"The market structure reinforces this picture. The top ten DApps control 80.5 per cent of total market capitalisation and over 90 per cent of active wallets. The distribution follows a power law — consistent with the winner-takes-most dynamics documented in social media and e-commerce.

So permissionless infrastructure clearly lowers entry barriers — but it does not flatten concentration. Network effects in DeFi liquidity pools are just as powerful as in social networks: deeper liquidity attracts more traders, which deepens liquidity further.

There is also a meaningful co-occurrence between governance quality and market scale — a Spearman correlation of 0.38. Whether markets reward governance, or successful projects simply invest in governance because they can afford to — that is a causal question this cross-sectional design cannot answer. But the association is there.

Now, these aggregate numbers hide a fundamental sector divide."

---

### Slide 7 – Phase 4: Results & Discussion

**Descriptive Slide Title:** "DeFi and Gaming Operate in Fundamentally Different Economic Worlds"

**Visual Layout Description:** A bubble quadrant chart fills the slide. X-axis: user count (low → high). Y-axis: economic throughput / volume (low → high). Four sector bubbles are plotted: DeFi in the upper-left quadrant (high value, moderate users), Gaming in the lower-right (many users, low value), NFT in the centre, Social in the lower-left. Bubble size represents market capitalisation. A bold annotation arrow spans the gap between DeFi and Gaming, labelled ">1,000× value-per-user gap." No tables — the chart tells the entire story.

**Key Slide Takeaways (2–3 bullets max):**

- DeFi dominates by economic value: $299.1B in volume, 57.4% of the strict sample. Gaming leads by user count: 12.67M active wallets, but at dramatically lower per-user throughput (Frontiers in Blockchain, 2023).
- The implied value-per-user gap exceeds 1,000× — a structural divide reflecting different economic architectures, not measurement error.
- Single-metric evaluation is systematically misleading; user count, volume, and TVL produce incompatible success rankings across sector boundaries.

**Speaking Script (~1 minute):**

"When we look at sectors, the averages break down completely. DeFi processes 299 billion dollars in volume. Gaming attracts 12.67 million active wallets — far more users. But the value per user is more than a thousand times higher in DeFi.

This is not noise. A DeFi wallet typically represents someone deploying large capital into liquidity pools. A gaming wallet represents a player earning fractional dollars per session. They are fundamentally different economic architectures.

The practical takeaway: there is no single universal success metric in this ecosystem. A gaming DApp with ten million users and five million dollars in volume would look like a failure by DeFi standards. Sector-specific benchmarks are essential.

But even within sectors, there is a subtler governance illusion worth examining."

---

### Slide 8 – Phase 4: Results & Discussion

**Descriptive Slide Title:** "Governance Tokens Frequently Signal Intent — Not Actual Authority"

**Visual Layout Description:** A Venn diagram as the primary visual element. One circle: "DApps That Issued Governance Tokens" (25% of strict sample). Second overlapping circle: "DApps With Binding On-Chain Governance." The non-overlapping portion of the governance-token circle is highlighted in a warning colour and labelled "Token Without Authority." Below the diagram, a compact three-row comparison table: Row 1 — governance token + on-chain governance (aligned); Row 2 — governance token + Snapshot or team-controlled (decoupled); Row 3 — no token + team-controlled (consistent centralisation).

**Key Slide Takeaways (2–3 bullets max):**

- 25% of the strict sample issued governance tokens, yet a meaningful fraction retains team-controlled or Snapshot-only processes — the token signals democratic intent without transferring decision-making power (Hassan & De Filippi, 2021).
- All 13 DApps with binding on-chain or DAO governance hold governance tokens — but the reverse does not hold, confirming partial decoupling of token design from actual governance authority.
- In the current market phase, governance token issuance functions primarily as a capital formation and community signalling mechanism — not as genuine governance transfer.

**Speaking Script (~1 minute):**

"This finding sharpens the paradox. Twenty-five per cent of the strict sample has issued governance tokens — tokens designed to grant voting power over protocol decisions. And indeed, all thirteen DApps with binding on-chain governance hold such tokens.

But the reverse does not hold. Several DApps issued governance tokens while the actual decision process remains team-controlled or limited to non-binding polls. The token signals democratic intent — but proposal thresholds and execution keys stay in team hands.

Hassan and De Filippi call this the gap between de jure and de facto decentralisation. In practice, the token often functions as a capital formation instrument rather than an effective governance mechanism. For investors and regulators, the implication is clear: governance token ownership is not a reliable proxy for governance rights.

Let me turn now to a strategic dimension — multi-chain deployment."

---

### Slide 9 – Phase 4: Results & Discussion

**Descriptive Slide Title:** "Multi-Chain DApps Show a 1.3× Market Cap Premium — But Causation Is Unclear"

**Visual Layout Description:** Two-panel layout. Left panel: a side-by-side bar chart comparing mean market capitalisation for single-chain DApps ($62.1M) vs. multi-chain DApps ($80.2M), with a "1.3×" label bridging the two bars. Right panel: a simple flow diagram with bidirectional arrows between "Multi-Chain Deployment" and "Higher Market Cap." A solid arrow points forward labelled "Broader market access"; a dashed arrow points backward labelled "Or do successful DApps expand?" The visual makes the correlation-vs.-causation point immediately apparent.

**Key Slide Takeaways (2–3 bullets max):**

- 70.6% of the strict sample deploys across multiple chains, vs. only 36.2% in the loose universe — the most commercially active DApps are disproportionately multi-chain.
- Multi-chain DApps command a 1.3× mean market cap premium, consistent across subsamples — but causal direction is ambiguous: expansion may drive growth, or prior success may fund expansion.
- The cross-sectional design cannot distinguish these mechanisms; the association motivates future longitudinal research on deployment timing.

**Speaking Script (~50 seconds):**

"Seventy per cent of the strict sample operates across multiple blockchains — nearly double the rate in the broader dataset. And multi-chain DApps show a 1.3 times higher market capitalisation.

But I want to be careful: the causal interpretation is open. Does multi-chain deployment drive higher valuations through broader market access? Or do well-capitalised projects simply expand because they can afford to?

The cross-sectional design cannot answer that. What it does show is a clear structural association: the most commercially active DApps are overwhelmingly multi-chain, and this co-occurs with stronger governance scores.

Finally, one finding that challenges a widely held assumption about funding."

---

### Slide 10 – Phase 4: Results & Discussion

**Descriptive Slide Title:** "Venture Capital Does Not Reliably Predict DApp Market Success"

**Visual Layout Description:** A diverging dot plot as the primary visual. On one side: funded DApps (N=13 in the strict sample) plotted by current market capitalisation, with a shaded overlay showing their funding-to-valuation ratio. On the other side: unfunded DApps that outperform the funded median, plotted at the same scale. A bold horizontal annotation line marks the funded median. The 0.11× ratio is displayed prominently as a callout: "For every dollar raised, the median funded DApp is now worth eleven cents."

**Key Slide Takeaways (2–3 bullets max):**

- The median funding-to-valuation ratio for venture-backed DApps in the strict sample is 0.11× — the median funded DApp is valued at roughly one-tenth of the capital invested in it.
- 29.4% of unfunded DApps exceed the market capitalisation of their funded peers — open-source forkability erodes the competitive moats that VC valuations typically price in.
- Capital raised should not be conflated with product validation; the data challenge the claim that venture backing reliably predicts long-term market performance.

**Speaking Script (~50 seconds):**

"One of the most counter-intuitive findings concerns venture capital. Among the thirteen funded DApps in the strict sample, the median funding-to-valuation ratio is 0.11 times. The median venture-backed DApp is currently worth about one-tenth of the capital invested in it.

Meanwhile, nearly thirty per cent of unfunded DApps exceed the market cap of their funded peers. Why? Because the open-source nature of DApps means anyone can fork the protocol — which erodes the competitive moats that institutional valuations typically price in.

Capital is clearly useful. But the data do not support the claim that it reliably predicts market success. This brings us to the conclusions."

---

### Slide 11 – Phase 5: Conclusion & Limitations

**Descriptive Slide Title:** "Decentralisation Is an Aspiration, Not Yet a Reality — And the Path Forward Requires Measurement"

**Visual Layout Description:** Two-column layout. Left column: five headline findings, each as a single-line statement with a small corresponding icon — a lock icon for centralisation, a scale for concentration, split arrows for the engagement gap, chain links for multi-chain, and a coin for funding. Right column: three limitation acknowledgements (snapshot timing, survivorship bias, causal ambiguity) in a muted colour, followed by three future research directions (longitudinal tracking, on-chain participation analysis, cross-chain causal studies) in an accent colour. A final callout bar across the bottom of the slide: "The DApp economy reconfigures traditional market structures under new institutional rules — it does not eliminate them."

**Key Slide Takeaways (2–3 bullets max):**

- Five headline findings: (1) 86.8% not fully decentralised; (2) top-10 hold 80.5% of market value; (3) DeFi–Gaming engagement gap exceeds 1,000×; (4) multi-chain DApps show a 1.3× premium; (5) median funded ROI is 0.11×.
- Limitations: cross-sectional snapshot (November 2025), survivorship bias in the strict sample, causal direction ambiguous for key associations.
- Future directions: longitudinal governance tracking, on-chain voting participation analysis, and quasi-experimental studies of multi-chain deployment timing — moving from correlation to causation.

**Speaking Script (~1 minute):**

"To conclude. This thesis provides an empirical benchmark at a scale not previously attempted — 855 DApps, 77 blockchains, 48 variables with manual governance coding.

Five findings stand out. First, 86.8 per cent of high-signal DApps are not fully decentralised. Second, the top ten DApps control over 80 per cent of market value — concentration ratios comparable to Web2. Third, the DeFi–Gaming value-per-user gap exceeds a thousand times. Fourth, multi-chain deployment correlates with a 1.3 times market cap premium. And fifth, the median venture-backed DApp trades at a tenth of its invested capital.

I want to be transparent about the boundaries: this is a single cross-sectional snapshot, subject to survivorship bias, and it cannot establish causal direction. The most important next step is longitudinal — tracking these same DApps over time to test whether governance matures and whether these correlations reflect causation.

What the data do establish is this: the DApp economy reconfigures traditional market structures under new institutional rules. It does not eliminate them.

Thank you."

---

## Presentation Summary

| Phase | Slides | Time | Allocation |
|-------|:------:|:----:|:----------:|
| **Phase 1:** Introduction & Relevance | 1–2 | ~1 min 30 sec | ~14% |
| **Phase 2:** Literature Review | 3 | ~1 min | ~9% |
| **Phase 3:** Methodology | 4 | ~1 min 30 sec | ~14% |
| **Phase 4:** Results & Discussion | 5–10 | ~5 min 40 sec | ~52% |
| **Phase 5:** Conclusion & Limitations | 11 | ~1 min | ~9% |
| **Total** | **11 slides** | **~10 min 40 sec** | **~100%** |

### Constraint Compliance Checklist

- **No walls of text:** Every slide is visual-first. Takeaways are limited to 2–3 concise bullets.
- **Mandatory visuals (Phase 4):** All six Results & Discussion slides specify a primary visual asset (donut chart, stacked bars + scatter plot, bubble quadrant chart, Venn diagram, bar chart + flow diagram, diverging dot plot).
- **Self-explaining headers:** No slide uses a generic title. Every header summarises the slide's takeaway.
- **Steady flow:** Every speaking script ends with an explicit narrative bridge to the next slide.
- **Citations:** Placed as parenthetical references throughout key takeaways (Schär 2021, Aramonte et al. 2021, Ovezik et al. 2025, Hassan & De Filippi 2021, Parker et al. 2016, Atzori 2017, Barbereau et al. 2023, Jensen et al. 2021, Agresti 2002, Frontiers in Blockchain 2023).
- **Speaking scripts:** Each targets conversational delivery at ~130 words per minute, with natural pauses and no jargon-dense passages.
