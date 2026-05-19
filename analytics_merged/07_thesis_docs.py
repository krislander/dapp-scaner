"""Backtest headline metrics + Markdown documentation (methodology, insights, anomalies, discussion)."""
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

import pandas as pd

from analytics_merged.config import (
    BACKTEST_METRICS_PATH,
    CONCEPT_ANOMALIES_PATH,
    CONCEPT_INSIGHTS_PATH,
    DISCUSSION_TOPICS_PATH,
    OUTPUT_DIR,
    PREPARED_PATH,
    RAW_DATA_PATH,
)
from analytics_merged.lib.reporting import bullet_list, df_to_markdown_table, write_md


def _bool(s: pd.Series) -> pd.Series:
    if s.dtype == bool:
        return s
    return s.astype(str).str.upper().isin(["TRUE", "1"])


def headline_metrics(df: pd.DataFrame) -> dict:
    n = len(df)
    if n == 0:
        return {"n": 0}
    g = df.dropna(subset=["level_of_decentralisation"])
    mcap = pd.to_numeric(df["market_cap"], errors="coerce")
    m = df[mcap.fillna(0) > 0].copy()
    m["market_cap"] = mcap.loc[m.index]
    top10 = float("nan")
    if len(m) > 0:
        tot = m["market_cap"].sum()
        top10 = m.nlargest(10, "market_cap")["market_cap"].sum() / tot * 100
    return {
        "n": n,
        "pct_decentralized": round((g["level_of_decentralisation"] == "DECENTRALIZED").mean() * 100, 2)
        if len(g)
        else float("nan"),
        "pct_team_controlled_gov": round((df["governance_type"] == "TEAM_CONTROLLED").mean() * 100, 2),
        "pct_company_owned": round((df["ownership_status"] == "COMPANY_OWNED").mean() * 100, 2),
        "top10_mcap_share_pct": round(top10, 2) if top10 == top10 else float("nan"),
        "pct_multichain": round(df["is_multi_chain"].mean() * 100, 2),
        "median_governance_score": round(float(df["governance_score"].median()), 4)
        if "governance_score" in df.columns
        else float("nan"),
    }


def build_backtest(df: pd.DataFrame) -> pd.DataFrame:
    loose = df[df["eligible_loose"]]
    strict = df[df["analysis_eligible"]]
    cohort = df[df["in_primary_cohort"].fillna(False)] if "in_primary_cohort" in df.columns else strict.iloc[:0]
    rows = []
    for label, sub in [("loose_universe_analytics_new_style", loose), ("strict_high_signal", strict), ("primary_cohort_topK", cohort)]:
        m = headline_metrics(sub)
        m["universe"] = label
        rows.append(m)
    out = pd.DataFrame(rows)
    out.to_csv(BACKTEST_METRICS_PATH, index=False)
    return out


def methodology_md(df: pd.DataFrame, backtest: pd.DataFrame) -> list:
    from analytics_merged.config import (
        MIN_ACTIVITY_SIGNALS_LOOSE,
        MIN_ACTIVITY_SIGNALS_STRICT,
        MIN_USERS_STRICT,
        REQUIRE_MARKET_OR_TVL,
    )

    lines = [
        "# Methodology (analytics_merged)",
        "",
        "## Purpose",
        "Merge **analytics_new** cohort discipline (ranked slices, manifest) with **analytics/** empirical feature engineering and chart idioms, evaluated on `DAPP_Dataset_Nov_2025 - Final.csv`.",
        "",
        "## Eligibility",
        f"- **Loose universe** (`eligible_loose`): governance fields complete + ≥{MIN_ACTIVITY_SIGNALS_LOOSE} positive activity signals — mirrors analytics_new for **backtest** comparison.",
        f"- **Strict universe** (`analysis_eligible`): loose rules **plus** ≥{MIN_ACTIVITY_SIGNALS_STRICT} signals, users ≥ {MIN_USERS_STRICT:,}, and "
        + ("`market_cap>0` OR `tvl>0`." if REQUIRE_MARKET_OR_TVL else "no extra market gate."),
        "- Derived columns follow `analytics/01_data_preparation.py` (governance_score, theme flags, efficiency ratios).",
        "",
        "## Cohorts",
        "Primary/secondary cohorts rank strict-eligible DApps per slice by weighted log signal; manifest in `cohort_manifest.json`.",
        "",
        "## Outputs philosophy",
        "- **Insights and anomalies** are stored as **conceptual rows** (patterns, prevalence, interpretation) — not DApp-level anomaly lists.",
        "",
        "## Backtest vs legacy approach",
        "The loose row approximates the older analytics pipeline universe; the strict row shows how headlines change under tighter measurement gates.",
        "",
        "### Headline comparison",
        df_to_markdown_table(backtest),
        "",
        "## Reproducibility",
        "```bash",
        "python3 analytics_merged/01_prepare.py",
        "python3 analytics_merged/02_governance.py",
        "python3 analytics_merged/03_market.py",
        "python3 analytics_merged/04_chains.py",
        "python3 analytics_merged/05_performance.py",
        "python3 analytics_merged/06_concept_synthesis.py",
        "python3 analytics_merged/07_thesis_docs.py",
        "```",
        "",
        f"**Source:** `{RAW_DATA_PATH.name}` — **rows:** {len(df)} — **strict N:** {int(df['analysis_eligible'].sum())} — **loose N:** {int(df['eligible_loose'].sum())}.",
    ]
    return lines


def main() -> None:
    df = pd.read_csv(PREPARED_PATH)
    df["analysis_eligible"] = _bool(df["analysis_eligible"])
    df["eligible_loose"] = _bool(df["eligible_loose"])
    if "in_primary_cohort" in df.columns:
        df["in_primary_cohort"] = _bool(df["in_primary_cohort"])

    backtest = build_backtest(df)

    ins = pd.read_csv(CONCEPT_INSIGHTS_PATH) if CONCEPT_INSIGHTS_PATH.exists() else pd.DataFrame()
    ano = pd.read_csv(CONCEPT_ANOMALIES_PATH) if CONCEPT_ANOMALIES_PATH.exists() else pd.DataFrame()
    dis = pd.read_csv(DISCUSSION_TOPICS_PATH) if DISCUSSION_TOPICS_PATH.exists() else pd.DataFrame()

    write_md(OUTPUT_DIR / "METHODOLOGY.md", methodology_md(df, backtest))

    ki = ["# Key insights (ecosystem and market level)", ""]
    ki.append("Conceptual statements derived from the strict eligible universe. See `conceptual_insights.csv` for structured fields.")
    ki.append("")
    if len(ins):
        for _, r in ins.iterrows():
            ki.append(f"## {r.get('insight_id', '')} — {r.get('title', '')}")
            ki.append(f"*{r.get('pillar', '')}*")
            ki.append(str(r.get("narrative", "")))
            ki.append(f"- **Metric:** `{r.get('metric_name', '')}` = `{r.get('metric_value', '')}`")
            if pd.notna(r.get("figure_suggestion")):
                ki.append(f"- **Figure:** `{r.get('figure_suggestion')}`")
            ki.append("")
    write_md(OUTPUT_DIR / "KEY_INSIGHTS.md", ki)

    am = ["# Structural anomalies and tensions (not DApp-level)", ""]
    am.append("Each entry is a **recurring pattern** observed across the strict sample. Use for thesis discussion, not as individual DApp callouts.")
    am.append("")
    if len(ano):
        for _, r in ano.iterrows():
            am.append(f"### {r.get('anomaly_id', '')} — {r.get('pattern_name', '')}")
            am.append(f"*Pillar: {r.get('pillar', '')} | Prevalence: {r.get('prevalence_pct', '')}% ({r.get('n_affected', '')} DApps)*")
            am.append("")
            am.append(f"**What:** {r.get('description', '')}")
            am.append("")
            am.append(f"**So what:** {r.get('interpretation', '')}")
            am.append("")
    write_md(OUTPUT_DIR / "ANOMALIES.md", am)

    rd = [
        "# Results and discussion",
        "",
        "## Claims supported by merged analytics",
    ]
    rd.extend(
        bullet_list(
            [
                "Strict gating shifts concentration and governance percentages versus the loose universe — see `backtest_headline_metrics.csv`.",
                "Governance heatmaps and token cross-tabs show systematic co-structure between labels and token types (`figures/02_*`).",
                "Market and TVL panels illustrate fat tails and capital concentration (`figures/03_*`, `figures/05_*`).",
                "Conceptual anomaly table encodes interpretable tensions for thesis discussion (`conceptual_anomalies.csv`).",
            ]
        )
    )
    rd.append("")
    rd.append("## Discussion prompts")
    rd.append("")
    if len(dis):
        for _, r in dis.iterrows():
            rd.append(f"### {r.get('topic_id', '')} — {r.get('theme', '')}")
            rd.append("")
            rd.append(str(r.get("prompt", "")))
            rd.append("")
    rd.append("")
    rd.append("## Figure index")
    figs = sorted((OUTPUT_DIR / "figures").glob("*.png"))
    rd.extend(bullet_list([f"`figures/{p.name}`" for p in figs]))
    write_md(OUTPUT_DIR / "RESULTS_AND_DISCUSSION.md", rd)

    brief = [
        "# Thesis brief (relevance)",
        "",
        "This merged pipeline answers whether **design labels** (governance, ownership, decentralisation, token type) align with **economic and adoption structure** when only statistically informative DApps are retained.",
        "",
        "## Why strict eligibility",
        "The loose sample supports continuity with earlier analytics scripts; the strict sample reduces noise from sparse metrics so ecosystem-level statements are defensible.",
        "",
        "## Suggested narrative arc",
    ]
    brief.extend(
        bullet_list(
            [
                "Show backtest table: same metrics, two universes.",
                "Present 2–3 figures from governance + market + performance.",
                "Move from insights (structural facts) to anomalies (interpretive tensions) to discussion prompts.",
            ]
        )
    )
    write_md(OUTPUT_DIR / "THESIS_BRIEF.md", brief)

    print(f"Wrote Markdown + {BACKTEST_METRICS_PATH}")


if __name__ == "__main__":
    main()
