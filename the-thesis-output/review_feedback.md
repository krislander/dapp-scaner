# Thesis Review Feedback — POL-13
**Reviewer:** Thesis Reviewer (POL)  
**Date:** 2026-05-20  
**Scope:** Full thesis draft — Chapters 1–6  
**Overall Assessment:** **Adequate / Needs targeted fixes before submission**

---

## Executive Summary

This thesis makes a genuine and timely empirical contribution to the DApp governance literature. The dataset construction (855 DApps, 77 chains, 48 variables, dual-universe design) is ambitious and methodologically defensible; the writing is clear and academic throughout; and the "decentralisation paradox" framing is analytically compelling. The quantified findings — 86.8% of strict-sample DApps are not fully decentralised, top-10 market cap share of 80.5%, 1,000× engagement gap between DeFi and Gaming — are striking and well-supported.

However, five critical issues must be resolved before submission, including two outright citation errors (a misidentified paper cited in Ch 1 and a phantom AI DApp segment introduced only in the Conclusions), a structural omission (RQ4 dropped from Ch 4's summary), and three missing references cited in Ch 5. Eight major issues — including a methodological terminology error (intra- vs inter-coder reliability), unjustified governance score weights, missing statistical test results that the methodology promises, and figure placeholders throughout Ch 4 — must also be fixed. None of these are fatal to the thesis argument, but several are precisely the kind of error that attracts examiner attention.

**Submission readiness:** Not yet ready. Estimated revision scope: targeted corrections across all chapters, no new empirical work required.

---

## Categorised Findings

### CRITICAL — Must fix before submission

---

**CRIT-01 | Ch 1, §1.2, line 29 — Citation error: Chen et al. (2020) misidentified**

*What was found:* RQ3's framing cites "(Chen et al., 2020)" for "power-law patterns documented in other digital platform markets." The Ch 1 reference list identifies Chen et al. (2020) as: "Exploiting blockchain data to detect smart Ponzi schemes on Ethereum. *IEEE Access*, 8, 37575–37586." This paper is about Ponzi scheme detection on Ethereum, not power-law distributions in digital platform markets.

*Recommended change:* Replace Chen et al. (2020) with an appropriate citation for power-law/winner-takes-most dynamics in digital platform markets (e.g., Clauset, Shalizi & Newman, 2009, on power-law distributions in empirical data; or a platform economics source such as Evans & Schmalensee on market tipping). Remove or correct the Chen et al. (2020) entry accordingly. If the Chen et al. paper is cited elsewhere in the thesis for a legitimate purpose, retain it with a corrected description.

---

**CRIT-02 | Ch 1 & Ch 6 — Two different papers cited as "Tan et al. (2023)"**

*What was found:* The thesis uses the same in-text citation format "Tan et al. (2023)" for two different papers in different chapters:
- Ch 1 reference list: *Tan, J., Allen, D., Berg, C., Lane, A., & Potter, T. (2023). The DAO that launched a thousand DAOs. Journal of Financial Regulation.*
- Ch 6 reference list: *Tan, J., Shrestha, Y. R., & Schäfer, L. (2023). The governance of decentralized autonomous organizations. Journal of Strategic Information Systems.*

Additionally, Ch 2 cites a third 2023 Tan paper ("Tan, L., & Shi, J. (2023)"), disambiguated as "Tan and Shi (2023)" — which is handled correctly. But "Tan et al. (2023)" is ambiguous between the Ch 1 and Ch 6 papers.

*Recommended change:* Both papers must be disambiguated in in-text citations. APA convention appends lowercase letters: "Tan et al., 2023a" and "Tan et al., 2023b." Update both the body citations and both reference lists consistently throughout all chapters.

---

**CRIT-03 | Ch 6, §6.2, RQ1 — "AI DApp segment" introduced without prior definition**

*What was found:* Ch 6 §6.2 (RQ1 answer, line 21) states: "The AI DApp segment, despite the highest token adoption rate (80%), recorded zero fully decentralised applications in the loose universe." The term "AI DApp" appears nowhere in Ch 1 (scope), Ch 2 (literature), Ch 3 (methodology), or Ch 4 (results). No AI sector is included in the taxonomy defined in §1.3 (DeFi, Gaming, NFT, Social, Infrastructure). There is no corresponding finding in Ch 4 to support this claim.

*Recommended change:* Either (a) remove this sentence entirely if the AI DApp segment was not analysed as part of the thesis, or (b) if AI DApps were part of the dataset and analysis, add the segment definition to §1.3, include it in the §3.4.2 theme flags, and report the finding in §4.5. Option (a) is strongly preferred unless there is substantive unreported analysis.

---

**CRIT-04 | Ch 4, §4.8 — RQ4 (multi-chain) omitted from chapter summary**

*What was found:* Section 4.8 "Cross-Sectional Summary" opens: "The results presented in this chapter address the thesis's three research questions: (RQ1)…(RQ2)…and (RQ3)…" The thesis defines four research questions in Ch 1. RQ4 (multi-chain deployment and market performance) is substantively addressed in §4.4 but does not appear as a labelled RQ4 entry in the 4.8 summary. Additionally, the RQ2 paragraph in §4.8 conflates findings from RQ2 (governance-label alignment), RQ3 (capital concentration), and RQ4 (multi-chain premium) into a single paragraph.

*Recommended change:* Revise §4.8 to include four clearly labelled RQ paragraphs (RQ1 through RQ4). Separate the existing "RQ2" paragraph's multi-chain material into a standalone "RQ4" paragraph. The opening sentence should read "four research questions" not "three."

---

**CRIT-05 | Ch 5 — Three in-text citations with no reference list entries**

*What was found:*
- §5.2: "Dixon, 2021" (progressive decentralisation concept) — not in Ch 5 reference list or any chapter reference list.
- §5.4: "Clauset, Shalizi, and Newman, 2009" (power-law exponent interpretation) — not in any reference list.
- §5.9.1: "Rochet and Tirole, 2003" (two-sided market theory) — not in any reference list.

*Recommended change:* Add the three missing references to Ch 5's reference list:
- Dixon, C. (2021). *Progressive decentralization: A playbook for building crypto applications*. Andreessen Horowitz blog, a16z.com.
- Clauset, A., Shalizi, C. R., & Newman, M. E. J. (2009). Power-law distributions in empirical data. *SIAM Review*, *51*(4), 661–703.
- Rochet, J.-C., & Tirole, J. (2003). Platform competition in two-sided markets. *Journal of the European Economic Association*, *1*(4), 990–1029.

If a consolidated bibliography is used (see SUGG-01), add there instead.

---

### MAJOR — Should fix before submission

---

**MAJ-01 | Ch 3, §3.5.4 — Incorrect methodology label: "inter-coder" vs "intra-coder"**

*What was found:* Section 3.5.4 is titled "Reliability and Inter-Coder Consistency" and reports Cohen's kappa values. However, the procedure described is: "All governance coding was performed by a single researcher (the thesis author). To test consistency, a random sample of 30 DApps was **re-coded independently after a two-week interval**." A single researcher re-coding their own work after a delay is *intra-coder reliability* (also called test-retest reliability), not inter-coder reliability. Inter-coder reliability requires two independent coders. This distinction is methodologically significant and will attract examiner scrutiny.

*Recommended change:* Rename the section to "§3.5.4 Intra-Coder Reliability." Change "inter-coder" to "intra-coder" or "test-retest" throughout the section. Add a sentence acknowledging the limitation: a single-coder design cannot provide inter-rater reliability estimates, which would require an independent second coder.

---

**MAJ-02 | Ch 3, §3.6.1 — Governance score weights (0.50 / 0.35 / 0.15) not justified**

*What was found:* The composite governance score assigns weights of 0.50 to decentralisation level, 0.35 to governance type, and 0.15 to ownership. The rationale given is that "weights reflect the theoretical primacy of the overall decentralisation assessment." No citation, sensitivity analysis, or validation exercise is provided for this weighting. The weights are consequential: they determine the governance score distribution, the governance-performance correlation (r = 0.38), and the K-means cluster assignments.

*Recommended change:* Add a brief justification grounded in the literature (e.g., cite Rahimian & Hassan, 2023 — already in Ch 2 — on multi-dimensional decentralisation). Alternatively, run a weight-sensitivity analysis showing that results are robust to plausible alternative weighting schemes (e.g., equal weights 1/3, 1/3, 1/3 vs. the chosen scheme). Report the sensitivity outcome in a footnote or appendix.

---

**MAJ-03 | Ch 4 — Figures are placeholder references, not embedded**

*What was found:* All 15 figure references in Ch 4 (Figures 4.1–4.15) use the format "[Figure X.X: Title] *File: figures/filename.png*" — bracketed placeholders rather than embedded images. A submitted thesis must have figures embedded in-line. This is the most operationally urgent issue for final submission.

*Recommended change:* Embed all figure images at the placeholder locations. Confirm that caption text, figure numbering, and filename references are consistent with the actual figure files in the `figures/` directory. Check that each figure is explicitly referenced (not just placed) in the surrounding text before or at first mention.

---

**MAJ-04 | Ch 5, §5.6 — Incorrect author in in-text citation**

*What was found:* Section 5.6 cites "Fritsch, Fritsch, and Wattenhofer (2022)." The Ch 2 reference list entry for this paper is: *Fritsch, R., Müller, M., & Wattenhofer, R. (2022).* The second author is Müller, not Fritsch. The in-text citation incorrectly repeats "Fritsch" for the second author.

*Recommended change:* Correct the in-text citation in §5.6 to "Fritsch, Müller, and Wattenhofer (2022)." Check for any other instances of this citation across all chapters.

---

**MAJ-05 | Ch 3 — No references section**

*What was found:* Chapter 3 (Methodology) ends without a references section. Chapters 1, 2, 5, and 6 each include per-chapter reference lists. Chapter 4 results refers back to prior chapters. Chapter 3 cites DappRadar, DeFiLlama, CoinMarketCap, CoinGecko and references `analytics/01_data_preparation.py` by filename — but provides no formal references for methodological choices (e.g., K-means literature, PCA literature, Cohen's kappa). The missing reference section creates an inconsistency and omits methodological citations.

*Recommended change:* Add a references section to Ch 3 covering: (a) K-means and PCA primary citations; (b) Cohen (1960) for kappa; (c) any API/platform documentation cited by URL. If a consolidated bibliography is added to the thesis (SUGG-01), ensure Ch 3 sources are included there.

---

**MAJ-06 | Ch 4, §4.7.2 — K-means cluster description lacks N counts and data coverage**

*What was found:* The K-means clustering in §4.7.2 describes four clusters ("Struggling ~30%, Emerging ~25%, Growing ~23%, Leading ~22%") applied to the "full 855-DApp dataset using K-means (k=4)." Two gaps: (1) "DApps with complete performance data" — the exact number of DApps included in this analysis is not stated. (2) Cluster sizes are described as approximations ("approximately 30 per cent") without exact counts. These omissions prevent independent verification and undermine the reproducibility claim.

*Recommended change:* State the exact N of DApps with complete data entering the clustering. Report exact cluster counts (e.g., "Struggling: N=87, Emerging: N=71..."). Add a sentence referencing the cluster output file in the analytics pipeline for reproducibility.

---

**MAJ-07 | Ch 3, §3.7.2 & §3.7.5 — Promised analyses not reported in Ch 4**

*What was found:* Section 3.7.2 states chi-squared tests, exact Fisher tests, and Cramér's V effect sizes will be reported for cross-tabulations. Section 3.7.5 describes PCA visualisation of cluster separation. Neither the chi-squared/Fisher/Cramér's V results nor PCA plots appear in Chapter 4. No figure reference for PCA visualisation exists in Ch 4.

*Recommended change:* Either (a) report the statistical test results in §4.2 where cross-tabulations are presented (adding chi-squared statistic, degrees of freedom, p-value, and Cramér's V for each key cross-tab), and add the PCA figure as Figure 4.16 with a brief interpretation, or (b) remove the promises from §3.7.2 and §3.7.5 and acknowledge these as not pursued in this study. Option (a) is strongly preferred as PCA cluster visualisation is a standard complement to K-means.

---

**MAJ-08 | Ch 5 — §5.4 concentration comparison with traditional platforms unsupported**

*What was found:* Section 5.4 claims "These figures are broadly comparable to — and in the user dimension more severe than — the concentration ratios observed in traditional platform markets." No specific comparison figures for traditional platform markets are provided and no citation is given at this claim. The power-law exponent comparison "(Clauset, Shalizi, and Newman, 2009)" is already flagged as missing (CRIT-05), but the comparison to traditional platforms also needs substantive numbers.

*Recommended change:* Add a sentence with concrete comparison figures: for example, citing documented concentration ratios from digital advertising, social media, or app store markets (e.g., Google/Facebook share of digital ad spend, App Store/Google Play duopoly). If the thesis cannot source appropriate comparison figures quickly, soften the claim to "consistent with" rather than "comparable to" and remove the "more severe" assertion.

---

### MINOR — Should fix, lower priority

---

**MIN-01 | Ch 4, §4.3.2 vs Ch 6, §6.2 — N inconsistency for market cap concentration**

*What was found:* Section 4.3.2 states the top-10 concentration figure is calculated over "the 63 strict-eligible DApps for which market cap data are available." Chapter 6 §6.2 presents the same 80.5% figure without the N=63 caveat, implying it applies to the full N=68. This is a minor but real inconsistency.

*Recommended change:* Add a parenthetical in Ch 6: "the top ten DApps by market capitalisation account for 80.5% of total market cap (calculated over the 63 of 68 strict-sample DApps for which market cap data are available)."

---

**MIN-02 | Ch 4, §4.3 — Power-law regression methodology undocumented**

*What was found:* A power-law exponent of α ≈ 0.61 is cited in §4.3.1 and again in Ch 5 and Ch 6 as a characterisation of market concentration. No reference is provided for the regression methodology (OLS on log-log? MLE as per Clauset et al.?), nor is the fit quality reported (R², goodness-of-fit test). A power-law claim without goodness-of-fit is methodologically incomplete.

*Recommended change:* Add one sentence specifying the estimation method (e.g., "Estimated via OLS regression on log-transformed market cap values; R² = X") or cite the Clauset et al. (2009) methodology for proper power-law fitting (and add it to the reference list — already required by CRIT-05). A footnote is acceptable here.

---

**MIN-03 | Ch 4, §4.3.3 ANO-MKT-03 — ROI comparison conflates stock and flow**

*What was found:* The "unfunded DApps outperform funded peers" anomaly computes "median return on investment as current market cap divided by total capital raised." Market cap is a stock value (point in time); capital raised is cumulative. This comparison is not ROI in any conventional sense (which would require the cost basis of investment, not total protocol funding). The figure "0.11×" is striking but methodologically non-standard.

*Recommended change:* Rename the metric (e.g., "funding-to-valuation ratio" or "capital-to-market-cap ratio") and add a sentence in §3.6 or a footnote in §4.3.3 acknowledging that this is a descriptive comparison, not a conventional ROI calculation, and noting its limitations (no account for timing of funding tranches, dilution, or token emissions post-funding).

---

**MIN-04 | Ch 2 — "Frontiers in Blockchain (2023)" citation uses journal as author**

*What was found:* Reference: "Frontiers in Blockchain. (2023). A statistical examination of utilization trends in decentralized applications. *Frontiers in Blockchain*." The journal name is used as both the author and the journal. This formatting is used when no author is identified on a journal article — but for an academic thesis, an unattributed journal article is grey literature at best and a formatting error at worst.

*Recommended change:* Identify the actual authors of this article and add them as the citation author. If the article has no identified author, the citation should note "[Author unknown]" or the source should be reconsidered as a reference.

---

**MIN-05 | Ch 1, §1.4 vs Ch 6, §6.1 — Contribution count inconsistency**

*What was found:* Ch 1 §1.4 describes "three interconnected contributions." Ch 6 §6.1 also describes "three principal contributions." These are consistent in count but the framing differs: Ch 1 uses "cross-sectional governance benchmark," "concrete quantified observations," and "multi-source measurement methodology"; Ch 6 uses "empirical governance benchmark," "quantified observations about governance reality," and "reproducible measurement methodology." The parallel is good but the terminological mismatch is unnecessary.

*Recommended change:* Align the contribution labels precisely between Ch 1 and Ch 6 so that the narrative arc closes cleanly. Readers checking Ch 6 against Ch 1 should see exact correspondence.

---

**MIN-06 | Ch 4 / Ch 5 — ANO and DIS cross-reference codes not consistently introduced**

*What was found:* Chapter 4 uses codes like "ANO-MKT-02," "ANO-ADP-01," "INS-GOV-01" without ever explaining this coding system. Chapter 5 uses "DIS-01" through "DIS-07." Readers encounter these labels without guidance on what the prefixes mean or where to find a code manifest.

*Recommended change:* Add a brief explanatory note at first occurrence (e.g., in §4.2.1 introducing "INS-GOV-01"): "Findings are labelled with prefix codes (INS = insight, ANO = anomaly, DIS = discussion point) to facilitate cross-referencing between chapters." Alternatively, add a 3-line note in §3.1 on the coding convention.

---

### SUGGESTIONS — Nice to have

---

**SUGG-01 — Add a consolidated bibliography**

Per-chapter reference lists create redundancy (several papers are cited in multiple chapters) and make cross-referencing difficult. A single consolidated bibliography at the end of the thesis, replacing or supplementing per-chapter lists, would improve usability and reduce the risk of inconsistent formatting between chapters.

---

**SUGG-02 — Add an RQ–to–chapter cross-reference table**

A simple table in §1.5 (or in Ch 3) mapping RQ1–RQ4 to the specific sections and figures that address each question would substantially improve thesis navigation. Format:

| Research Question | Primary section | Supporting sections |
|---|---|---|
| RQ1 | §4.2 | §4.6.3, §4.7.3 |
| RQ2 | §4.2.1, §4.2.3 | §5.2, §5.3 |
| RQ3 | §4.3 | §5.4 |
| RQ4 | §4.4.2 | §5.8 |

---

**SUGG-03 — Governance score construct validity note**

The composite governance score is novel — no published benchmark exists to validate it against. Consider a brief note acknowledging this, and propose a validity test: if DeFiLlama, Defisafety.com, or similar governance rating tools cover any of the 68 strict-sample DApps, a rank-correlation between the thesis score and external ratings would provide convergent validity evidence. This strengthens the measurement methodology contribution.

---

**SUGG-04 — Strengthen the "progressive decentralisation" literature base**

Section 5.2 references only "Dixon, 2021" (a practitioner blog post) for the progressive decentralisation concept. This theoretical pivot point deserves more scholarly grounding. Consider also citing: Hassan & De Filippi (2021) — already in the reference list — on de jure vs de facto decentralisation trajectories; and/or relevant DAO lifecycle literature (Tan & Shi, 2023 on DAO survival rates — already cited).

---

## Chapter-by-Chapter Strengths Summary

| Chapter | Key strengths |
|---|---|
| Ch 1 Introduction | Clear problem framing; specific RQs; honest scope boundaries; concrete contribution claims |
| Ch 2 Literature Review | Comprehensive coverage; strong 5-gap analysis; direct positioning relative to prior work; high-quality citation of Ovezik et al. (2025) and Rahimian & Hassan (2023) |
| Ch 3 Methodology | Detailed coding decision rules; dual-universe design; kappa reliability reporting; honest limitations section |
| Ch 4 Results | Strong dual-universe comparison table; cross-tabulation confirms internal coding consistency; anomaly flagging adds transparency |
| Ch 5 Discussion | Memorable "decentralisation paradox" framing; 7-paradox structure holds together; specific actionable implications for builders/regulators |
| Ch 6 Conclusions | Clean RQ-by-RQ answers; future research directions are specific and feasible |

---

## Priority Fix List (Ordered for the Student)

1. **CRIT-03** — Remove or properly introduce the AI DApp segment in Ch 6 (15 min fix)
2. **CRIT-04** — Fix the "three research questions" error in §4.8 and add RQ4 paragraph (30 min)
3. **CRIT-02** — Disambiguate Tan et al. (2023a/b) across Ch 1 and Ch 6 (20 min)
4. **CRIT-01** — Replace the Chen et al. (2020) citation in §1.2 (20 min)
5. **CRIT-05** — Add three missing references to Ch 5 reference list (15 min)
6. **MAJ-01** — Correct "inter-coder" to "intra-coder" in §3.5.4 (10 min)
7. **MAJ-04** — Correct "Fritsch, Fritsch, Wattenhofer" to "Fritsch, Müller, Wattenhofer" (5 min)
8. **MAJ-03** — Embed figures in Ch 4 (varies; depends on figure preparation)
9. **MAJ-07** — Add statistical test results to Ch 4 cross-tabs, or remove promises from Ch 3 (60 min)
10. **MAJ-02** — Add governance score weight justification (30 min)
11. **MAJ-05** — Add references section to Ch 3 (20 min)
12. **MAJ-06** — Add N counts to K-means cluster description (10 min)
13. **MAJ-08** — Add comparison figures for traditional platform concentration claim (20 min)
14. **MIN-01 through MIN-06** — Address as time permits

---

*Review completed: 2026-05-20. Next action: return to the Student for revisions. Suggest re-review of §4.8, §5.4, §6.2, and all reference lists after fixes are applied.*
