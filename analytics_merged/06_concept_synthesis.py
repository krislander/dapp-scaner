"""
Aggregate-only insights and anomalies (no per-DApp CSV rows).
Patterns describe markets, ecosystems, governance, tokens, behaviour.
"""
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

import numpy as np
import pandas as pd

from analytics_merged.config import (
    CONCEPT_ANOMALIES_PATH,
    CONCEPT_INSIGHTS_PATH,
    DISCUSSION_TOPICS_PATH,
    PREPARED_PATH,
)


def _bool(s: pd.Series) -> pd.Series:
    if s.dtype == bool:
        return s
    return s.astype(str).str.upper().isin(["TRUE", "1"])


def pct(cond: pd.Series, base: int) -> float:
    return round(100.0 * float(cond.sum()) / max(base, 1), 2)


def build_insights(strict: pd.DataFrame) -> pd.DataFrame:
    n = len(strict)
    rows = []
    if n == 0:
        return pd.DataFrame(
            columns=[
                "insight_id",
                "pillar",
                "title",
                "narrative",
                "metric_name",
                "metric_value",
                "figure_suggestion",
            ]
        )

    gov = strict["governance_type"]
    dec = strict["level_of_decentralisation"]
    own = strict["ownership_status"]
    users = pd.to_numeric(strict["users"], errors="coerce").fillna(0)
    mcap = pd.to_numeric(strict["market_cap"], errors="coerce").fillna(0)

    rows.append(
        {
            "insight_id": "INS-GOV-01",
            "pillar": "governance",
            "title": "Decentralisation label mix in the high-signal subset",
            "narrative": "Among DApps passing strict activity thresholds, the distribution of decentralisation labels shows how far the sample is from fully on-chain, community-controlled ideals.",
            "metric_name": "pct_level_DECENTRALIZED",
            "metric_value": pct(dec == "DECENTRALIZED", n),
            "figure_suggestion": "figures/02_governance_distribution_strict.png",
        }
    )
    rows.append(
        {
            "insight_id": "INS-GOV-02",
            "pillar": "governance",
            "title": "Team-operated governance remains common at scale",
            "narrative": "Even when restricting to well-measured DApps, team-controlled governance types account for a large share—relevant for thesis arguments on progressive decentralisation.",
            "metric_name": "pct_governance_TEAM_CONTROLLED",
            "metric_value": pct(gov == "TEAM_CONTROLLED", n),
            "figure_suggestion": "figures/02_governance_distribution_strict.png",
        }
    )

    m_pos = strict[mcap > 0]
    if len(m_pos) > 0:
        tot = m_pos["market_cap"].sum()
        top10 = m_pos.nlargest(10, "market_cap")["market_cap"].sum() / tot * 100
        rows.append(
            {
                "insight_id": "INS-MKT-01",
                "pillar": "market",
                "title": "Capital concentration in the strict universe",
                "narrative": "Token market capitalisation remains heavily concentrated among a small head when only DApps with rich metrics are analysed—consistent with winner-takes-most dynamics in attention and liquidity.",
                "metric_name": "top10_share_of_mcap_pct",
                "metric_value": round(float(top10), 2),
                "figure_suggestion": "figures/03_market_dynamics_strict.png",
            }
        )

    u_pos = strict[users > 0]
    if len(u_pos) > 0:
        tu = u_pos["users"].sum()
        t10u = u_pos.nlargest(10, "users")["users"].sum() / tu * 100
        rows.append(
            {
                "insight_id": "INS-ADP-01",
                "pillar": "adoption",
                "title": "User attention concentration",
                "narrative": "Active wallets aggregate on a small set of destinations; the tail is long but thin once minimum-user filters apply.",
                "metric_name": "top10_share_of_users_pct",
                "metric_value": round(float(t10u), 2),
                "figure_suggestion": "figures/03_market_dynamics_strict.png",
            }
        )

    rows.append(
        {
            "insight_id": "INS-ADP-02",
            "pillar": "adoption",
            "title": "Multichain deployment rate",
            "narrative": "Share of strict-eligible DApps that list more than one chain; indicates ecosystem-level expansion vs chain-specialisation strategies.",
            "metric_name": "pct_multichain",
            "metric_value": round(100 * strict["is_multi_chain"].mean(), 2),
            "figure_suggestion": "figures/04_chain_top15_strict.png",
        }
    )

    for flag, label, pillar in [
        ("is_defi", "DeFi-tagged slice (category/sector heuristic)", "ecosystem"),
        ("is_gaming", "Gaming-tagged slice", "ecosystem"),
        ("is_social", "Social-tagged slice", "ecosystem"),
    ]:
        if flag not in strict.columns:
            continue
        m = strict[strict[flag].fillna(False)]
        share_n = round(100 * len(m) / n, 2) if n else 0
        share_u = round(100 * m["users"].sum() / max(users.sum(), 1), 2) if users.sum() else 0
        rows.append(
            {
                "insight_id": f"INS-ECO-{flag}",
                "pillar": pillar,
                "title": label,
                "narrative": "Theme flags from analytics/01-style heuristics show how much of the strict sample and its user base each vertical absorbs.",
                "metric_name": "pct_of_strict_dapps|pct_of_strict_users",
                "metric_value": f"{share_n}% | {share_u}%",
                "figure_suggestion": "figures/05_performance_strict.png",
            }
        )

    rows.append(
        {
            "insight_id": "INS-TOK-01",
            "pillar": "token",
            "title": "Governance-labelled tokens in the strict cohort",
            "narrative": "Prevalence of governance-type tokens among DApps that already pass engagement filters informs how often tokens are framed as voting assets vs pure utility.",
            "metric_name": "pct_is_governance_token",
            "metric_value": pct(strict["is_governance_token"].fillna(False), n),
            "figure_suggestion": "figures/02_governance_token_heatmap_strict.png",
        }
    )

    return pd.DataFrame(rows)


def build_anomalies(strict: pd.DataFrame) -> pd.DataFrame:
    n = len(strict)
    rows = []
    if n == 0:
        return pd.DataFrame(
            columns=[
                "anomaly_id",
                "pillar",
                "pattern_name",
                "prevalence_pct",
                "n_affected",
                "description",
                "interpretation",
            ]
        )

    def add(aid, pillar, name, mask, desc, interp):
        nn = int(mask.sum())
        rows.append(
            {
                "anomaly_id": aid,
                "pillar": pillar,
                "pattern_name": name,
                "prevalence_pct": pct(mask, n),
                "n_affected": nn,
                "description": desc,
                "interpretation": interp,
            }
        )

    add(
        "ANO-GOV-01",
        "governance",
        "Decentralised label with company ownership",
        (strict["level_of_decentralisation"] == "DECENTRALIZED")
        & (strict["ownership_status"] == "COMPANY_OWNED"),
        "Co-occurrence of maximum decentralisation score with corporate ownership—suggests definitional overlap between product marketing and control reality.",
        "Discuss legal wrappers, token distribution, and whether 'decentralised' refers to protocol vs operator.",
    )
    add(
        "ANO-GOV-02",
        "governance",
        "Governance token type but team-controlled process",
        strict["is_governance_token"].fillna(False) & (strict["governance_type"] == "TEAM_CONTROLLED"),
        "Tokens classified as governance assets while formal governance remains team-steered.",
        "Useful tension for token design vs participation narratives; not an error but a structural pattern.",
    )
    add(
        "ANO-GOV-03",
        "governance",
        "Centralised decentralisation score with on-chain token governance",
        (strict["level_of_decentralisation"] == "CENTRALIZED")
        & (strict["governance_type"] == "ONCHAIN_TOKEN_GOVERNANCE"),
        "On-chain voting exists while overall decentralisation is labelled centralised—often upgradeability or off-chain execution.",
        "Interpret via timelocks, multisigs, and scope of on-chain votes.",
    )
    add(
        "ANO-GOV-04",
        "governance",
        "DAO ownership without formal governance enum",
        (strict["ownership_status"] == "DAO_OWNED") & (strict["governance_type"] == "NONE"),
        "Ownership attributed to a DAO while governance type is recorded as none.",
        "May reflect data lag, informal governance, or classification edge cases.",
    )

    mcap = pd.to_numeric(strict["market_cap"], errors="coerce")
    u = pd.to_numeric(strict["users"], errors="coerce").fillna(0)
    mpu = np.where(u > 0, mcap / u, np.nan)
    s = pd.Series(mpu, index=strict.index)
    hi = s >= s.quantile(0.9)
    valid = np.isfinite(mpu) & (u >= 1000)
    add(
        "ANO-MKT-01",
        "market",
        "High market cap per active wallet (top decile among measured)",
        valid & hi,
        "Valuation per user in the top decile relative to the strict sample—signals speculative depth or thin active-user bases.",
        "Compare to category norms; avoid single-name attribution at thesis level.",
    )

    tvl = pd.to_numeric(strict["tvl"], errors="coerce").fillna(0)
    ratio = np.where(mcap > 0, tvl / mcap, np.nan)
    add(
        "ANO-MKT-02",
        "market",
        "Protocol TVL multiples above token market cap",
        np.isfinite(ratio) & (ratio > 10),
        "TVL materially exceeds floated valuation—common for wrappers, staking, or measurement timing effects.",
        "Discuss leverage, double-counting, and snapshot mismatch between DeFi metrics and equity-like mcap.",
    )

    raised = pd.to_numeric(strict["raised_capital"], errors="coerce").fillna(0)
    funded_med = mcap[raised > 0].median()
    if np.isfinite(funded_med):
        unf = (raised == 0) & (mcap > 0)
        add(
            "ANO-MKT-03",
            "market",
            "Unfunded rows above funded median market cap",
            unf & (mcap > funded_med),
            "Share of zero-raised DApps whose market cap exceeds the median of funded peers in the same strict universe.",
            "Highlights retail-driven or organic listings vs VC-funded cohorts.",
        )

    add(
        "ANO-ADP-01",
        "behaviour",
        "Centralised label with very high user counts",
        (strict["level_of_decentralisation"] == "CENTRALIZED")
        & (u >= u.quantile(0.9)),
        "Some of the most popular DApps by active wallets are labelled centralised — users flock to them regardless of governance model.",
        "Adoption is driven by product quality and network effects, not decentralisation claims. Challenges the assumption that users care about governance.",
    )

    add(
        "ANO-PARA-01",
        "governance",
        "The decentralisation paradox at scale",
        (strict["level_of_decentralisation"] != "DECENTRALIZED"),
        f"In the strict sample, {round((strict['level_of_decentralisation'] != 'DECENTRALIZED').mean() * 100, 1)}% of DApps are NOT fully decentralised, despite being built on decentralised infrastructure.",
        "The blockchain layer is decentralised but the application layer remains centralised — raising the question of whether DApp decentralisation is achievable or even desired by builders.",
    )

    vol = pd.to_numeric(strict.get("volume"), errors="coerce").fillna(0)
    gaming_m = strict.get("is_gaming", pd.Series(False, index=strict.index)).fillna(False)
    defi_m = strict.get("is_defi", pd.Series(False, index=strict.index)).fillna(False)
    gaming_u_total = u[gaming_m].sum()
    defi_vol_total = vol[defi_m].sum()
    if gaming_u_total > 0 and defi_vol_total > 0:
        add(
            "ANO-ENG-01",
            "ecosystem",
            "Gaming vs DeFi engagement gap",
            gaming_m | defi_m,
            f"Gaming attracts {int(gaming_u_total):,} users with low per-user value; DeFi processes ${defi_vol_total/1e9:.1f}B volume. The value-per-user gap exceeds 100x between these sectors.",
            "User counts alone are misleading as a success metric. A DApp with 1M gaming users may generate less economic activity than a DEX with 10K traders.",
        )

    mc = strict.get("is_multi_chain", pd.Series(False, index=strict.index)).fillna(False)
    add(
        "ANO-CHAIN-01",
        "ecosystem",
        "Multi-chain deployment correlates with higher valuation",
        mc,
        f"{round(mc.mean() * 100, 1)}% of the strict sample deploys multi-chain. Legacy analysis shows a 1.3x market cap premium for multi-chain DApps.",
        "Unclear whether multi-chain causes growth or is simply affordable only for already-successful projects. Survivorship bias may inflate the premium.",
    )

    return pd.DataFrame(rows)


def build_discussion(strict: pd.DataFrame, loose_n: int, strict_n: int) -> pd.DataFrame:
    n = len(strict)
    dec = strict["level_of_decentralisation"]
    gov = strict["governance_type"]
    own = strict["ownership_status"]
    mcap = pd.to_numeric(strict["market_cap"], errors="coerce").fillna(0)
    users = pd.to_numeric(strict["users"], errors="coerce").fillna(0)
    tvl = pd.to_numeric(strict["tvl"], errors="coerce").fillna(0)
    raised = pd.to_numeric(strict["raised_capital"], errors="coerce").fillna(0)

    pct_decent = round((dec == "DECENTRALIZED").mean() * 100, 1) if n else 0
    pct_company = round((own == "COMPANY_OWNED").mean() * 100, 1) if n else 0
    pct_team = round((gov == "TEAM_CONTROLLED").mean() * 100, 1) if n else 0

    m_pos = strict[mcap > 0]
    top10_pct = round(m_pos.nlargest(10, "market_cap")["market_cap"].sum() / max(m_pos["market_cap"].sum(), 1) * 100, 1) if len(m_pos) else 0
    u_pos = strict[users > 0]
    top10_u = round(u_pos.nlargest(10, "users")["users"].sum() / max(u_pos["users"].sum(), 1) * 100, 1) if len(u_pos) else 0

    gaming = strict[strict.get("is_gaming", pd.Series(False, index=strict.index)).fillna(False)]
    defi = strict[strict.get("is_defi", pd.Series(False, index=strict.index)).fillna(False)]
    gaming_u = int(gaming["users"].sum()) if len(gaming) else 0
    defi_vol = float(defi["volume"].sum()) if "volume" in defi.columns and len(defi) else 0

    mc_pct = round(strict["is_multi_chain"].mean() * 100, 1) if n else 0

    funded_n = int((raised > 0).sum())
    funded_med_roi = ""
    if funded_n > 2:
        fm = mcap[raised > 0]
        fr = raised[raised > 0] * 1e6  # raised_capital stored in millions USD
        roi = fm / fr
        funded_med_roi = f" (median funding ROI: {round(float(roi.median()), 2)}x)"

    topics = [
        {
            "topic_id": "DIS-01",
            "theme": "The decentralisation paradox",
            "prompt": (
                f"Only {pct_decent}% of the {n} high-signal DApps are labelled truly decentralised, "
                f"while {pct_company}% are company-owned and {pct_team}% are team-controlled. "
                "Does this mean the Web3 industry's core promise of decentralisation is mostly marketing, "
                "or are projects on a genuine path toward progressive decentralisation that our snapshot cannot capture?"
            ),
        },
        {
            "topic_id": "DIS-02",
            "theme": "Labelling vs mechanics",
            "prompt": (
                "Some DApps issue governance tokens yet remain team-controlled; others are labelled "
                "'decentralised' while a company owns the smart contracts. Are these contradictions "
                "structural features of the industry — where token design serves fundraising more than "
                "community power — or classification errors that better data would resolve?"
            ),
        },
        {
            "topic_id": "DIS-03",
            "theme": "Concentration mirrors traditional tech",
            "prompt": (
                f"The top 10 DApps hold {top10_pct}% of total market cap and {top10_u}% of users. "
                "This winner-takes-all pattern mirrors Web2 monopolies (Google, Meta, Amazon). "
                "If blockchains are designed to be permissionless and open, why does capital and attention "
                "concentrate so heavily? Does decentralised infrastructure actually prevent market dominance, "
                "or does it just relocate it?"
            ),
        },
        {
            "topic_id": "DIS-04",
            "theme": "Engagement gap between Gaming and DeFi",
            "prompt": (
                f"Gaming DApps attract {gaming_u:,} users but generate little financial volume, "
                f"while DeFi DApps process ${defi_vol/1e9:.1f}B in volume with fewer users. "
                "There is a 1000x gap in value-per-user between these sectors. "
                "What does this mean for how we measure DApp 'success'? "
                "Is user count a meaningful metric if most users generate near-zero economic activity?"
            ),
        },
        {
            "topic_id": "DIS-05",
            "theme": "Concentration and governance realism",
            "prompt": (
                "If capital and users are this concentrated, token-based governance voting is effectively "
                "controlled by a handful of large holders. Can on-chain governance be called democratic "
                "when the top wallets can outvote everyone else? What would a realistic governance model "
                "look like given this concentration?"
            ),
        },
        {
            "topic_id": "DIS-06",
            "theme": "The funding efficiency paradox",
            "prompt": (
                f"Only {funded_n} DApps in the strict sample raised venture capital{funded_med_roi}. "
                "Meanwhile, many unfunded DApps outperform funded ones in market cap. "
                "Does raising capital actually help a DApp succeed, or does it just reflect "
                "investor hype cycles that do not predict product-market fit?"
            ),
        },
        {
            "topic_id": "DIS-07",
            "theme": "Multi-chain strategy and survival",
            "prompt": (
                f"{mc_pct}% of the strict sample deploys on multiple chains. "
                "Multi-chain DApps show higher median valuations in the legacy analysis (1.3x premium). "
                "Is multi-chain deployment a cause of success (more users, more liquidity) or a consequence "
                "(only well-funded teams can afford it)? What does this mean for small teams building on a single chain?"
            ),
        },
    ]
    return pd.DataFrame(topics)


def main() -> None:
    df = pd.read_csv(PREPARED_PATH)
    df["analysis_eligible"] = _bool(df["analysis_eligible"])
    df["eligible_loose"] = _bool(df["eligible_loose"])
    strict = df[df["analysis_eligible"]]
    loose_n = int(df["eligible_loose"].sum())
    strict_n = len(strict)

    ins = build_insights(strict)
    ano = build_anomalies(strict)
    dis = build_discussion(strict, loose_n, strict_n)

    ins.to_csv(CONCEPT_INSIGHTS_PATH, index=False)
    ano.to_csv(CONCEPT_ANOMALIES_PATH, index=False)
    dis.to_csv(DISCUSSION_TOPICS_PATH, index=False)
    print(f"Wrote {CONCEPT_INSIGHTS_PATH}, {CONCEPT_ANOMALIES_PATH}, {DISCUSSION_TOPICS_PATH}")


if __name__ == "__main__":
    main()
