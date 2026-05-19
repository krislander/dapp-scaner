"""
Assemble thesis-oriented Markdown: methodology, insights, anomalies, results/discussion, brief.
Run after 01–03.
"""
import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

import pandas as pd

from analytics_new.config import (
    COHORT_MANIFEST_PATH,
    DAPP_ANOMALIES_PATH,
    ECO_SUMMARY_PATH,
    OUTPUT_DIR,
    PREPARED_DATA_PATH,
    RAW_DATA_PATH,
    THEME_SUMMARY_PATH,
)
from analytics_new.lib.reporting import bullet_list, df_to_markdown_table, write_md
from analytics_new.lib.themes import theme_rulebook


def load_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_methodology(manifest: dict, df: pd.DataFrame) -> list:
    n = len(df)
    elig = int(df["analysis_eligible"].sum())
    lines = [
        "# Methodology",
        "",
        "## 1. Data source and scope",
        f"- **Source file:** `{RAW_DATA_PATH.name}`",
        f"- **Rows:** {n} DApps after load.",
        f"- **Analysis-eligible rows:** {elig} (see eligibility rules below).",
        "- **Units (financial):** `tvl`, `market_cap`, `volume`, `users`, `transactions` are used as provided in the CSV. `total_liquidity_usd` is documented as **millions USD** in the project brief; the pipeline adds `liquidity_usd = total_liquidity_usd × 10⁶` in preparation for like-for-like comparisons.",
        "- **Multi-label `sub_category`:** comma-separated. **Primary sub-tag** for secondary cohorts is the **first** segment after splitting on commas (documented sensitivity: ordering may affect small slices).",
        "",
        "## 2. Eligibility (“sufficient data”)",
        "- **Governance completeness:** non-missing `governance_type`, `ownership_status`, `level_of_decentralisation`.",
        "- **Activity signal:** at least **two** of `{users, volume, transactions, tvl, market_cap}` must be present and **> 0**.",
        "- **Derived fields:** `data_completeness_score` ∈ [0,1] (50% weight on governance completeness, 50% on share of activity metrics populated).",
        "",
        "## 3. Cohort construction (noise reduction)",
        "- **Primary slices:** `(dapp_sector, dapp_category)`. **Secondary slices:** `(dapp_sector, dapp_category, primary_sub_tag)`.",
        "- Within each slice, eligible DApps are ranked by a **signal score** = weighted sum of `log1p(metric)` for users, volume, TVL, market cap, transactions (weights in `analytics_new/config.py`).",
        f"- **Selection:** if eligible count ≥ {manifest.get('parameters', {}).get('COHORT_MIN_SIZE', 20)}, take the top **min(50, n_eligible)**; if eligible count < 20, take **all** eligible in that slice. Manifest records `cohort_size_note` per slice.",
        "",
        "## 4. Ecosystem vs DApp level",
        "- **Ecosystem:** primary grouping is `dapp_sector` (e.g. defi, exchanges, games). Cross-sector similarity (e.g. DEX under `exchanges` vs `defi`) is discussed as a **labelling limitation**, not merged silently.",
        "- **DApp level:** robust modified z-scores (median / MAD) within each sector for `volume_per_user`, `tx_per_user`, `tvl_to_mcap` (requires `users ≥ 1000` for ratio stability). Flags combine high robust-z and top within-sector percentile (see `analytics_new/config.py`).",
        "",
        "## 5. Theme and “strange result” rules",
        "Themes (prediction markets, AI, DePIN/RWA) use documented keyword/category rules in `analytics_new/lib/themes.py`. Hypothesis-style flags (e.g. centralized label but very high users) are precomputed in `01_prepare_cohorts.py`.",
        "",
        "## 6. Reproducibility",
        "```bash",
        "python analytics_new/01_prepare_cohorts.py",
        "python analytics_new/02_ecosystem_analysis.py",
        "python analytics_new/03_dapp_level_analysis.py",
        "python analytics_new/04_thesis_report.py",
        "```",
        "",
        "## 7. Limitations",
        "- Single cross-sectional snapshot; no time series causality.",
        "- Mixed provenance of metrics (see repository `DATABASE_COLUMNS.md`).",
        "- Keyword themes (AI, DePIN) incur false positives/negatives; rule text is versioned in code for audit.",
    ]
    return lines


def build_key_insights(df: pd.DataFrame, eco: pd.DataFrame, themes: pd.DataFrame) -> list:
    lines = ["# Key insights (machine-assisted draft)", ""]
    elig = df[df["analysis_eligible"]]
    cohort = df[df["in_primary_cohort"]]
    gov_mix = elig["governance_type"].value_counts(normalize=True).head(5)
    lines.append("## Governance mix (eligible population)")
    lines.extend(bullet_list([f"{k}: {100*v:.1f}%" for k, v in gov_mix.items()]))
    lines.append("")
    lines.append("## Token types (eligible)")
    tt = elig["token_type"].value_counts(normalize=True).head(6)
    lines.extend(bullet_list([f"{k}: {100*v:.1f}%" for k, v in tt.items()]))
    lines.append("")
    lines.append("## Multi-chain share")
    lines.append(
        f"- Eligible DApps with `is_multi_chain`: **{100*elig['is_multi_chain'].mean():.1f}%**; primary cohort: **{100*cohort['is_multi_chain'].mean():.1f}%**."
    )
    lines.append("")
    lines.append("## Cohort vs full eligible (by sector counts)")
    if len(eco):
        pivot = eco.pivot(index="dapp_sector", columns="slice", values="n").fillna(0)
        lines.append(df_to_markdown_table(pivot.reset_index(), max_rows=30))
    lines.append("")
    lines.append("## Theme cohorts (eligible matches)")
    if len(themes):
        lines.append(df_to_markdown_table(themes, max_rows=20))
    lines.append("")
    lines.append("### Theme rulebook (audit)")
    for tid, desc, _ in theme_rulebook():
        lines.append(f"- **{tid}:** {desc}")
    return lines


def build_anomalies(df: pd.DataFrame, ann: pd.DataFrame) -> list:
    lines = ["# Anomalies and edge cases", ""]
    strange_path = OUTPUT_DIR / "strange_hypothesis_counts.csv"
    if strange_path.exists():
        st = pd.read_csv(strange_path)
        lines.append("## Hypothesis-style cross-checks (eligible)")
        lines.append(df_to_markdown_table(st, max_rows=50))
        lines.append("")
    if len(ann):
        lines.append("## DApp-level statistical flags (sample)")
        top = ann.assign(_az=ann["robust_z"].abs()).sort_values("_az", ascending=False).drop(
            columns="_az"
        ).head(25)
        lines.append(df_to_markdown_table(top, max_rows=25))
    lines.append("")
    lines.append("## Ecosystem-level interpretation")
    lines.extend(
        bullet_list(
            [
                "Review sector medians in `ecosystem_summary.csv` when a DApp flag appears — some sectors (e.g. exchanges) mechanically show higher volume per user.",
                "Compare `eligible_all` vs `primary_cohort` slices to ensure conclusions are not artifacts of the top-K selection.",
            ]
        )
    )
    return lines


def build_results_discussion(df: pd.DataFrame) -> list:
    figs = sorted((OUTPUT_DIR / "figures").glob("*.png"))
    rel_figs = [f"figures/{p.name}" for p in figs]
    lines = [
        "# Results and discussion",
        "",
        "## Key messages (claim → evidence)",
        "",
        "1. **Governance and token design vary systematically by sector** — Evidence: heatmaps `heatmap_gov_token_eligible.png` / cohort variant; crosstab CSVs in `outputs/`.",
        "2. **Cohort selection concentrates signal without dropping governance completeness** — Evidence: `cohort_manifest.json` per-slice notes; sector bar chart `eco_sector_counts_eligible_vs_cohort.png`.",
        "3. **Theme verticals (prediction, AI, DePIN/RWA) are thin but identifiable** — Evidence: `theme_cohort_summary.csv` and scatter plots `theme_*_users_volume.png`.",
        "4. **Ratio-based outliers highlight business-model diversity** — Evidence: `dapp_anomalies.csv` (volume per user, tx per user, TVL/market cap) with sector-relative robust z-scores.",
        "",
        "## Figures generated",
    ]
    lines.extend(bullet_list(rel_figs))
    lines.append("")
    lines.append("## Critical interpretation (thesis core)")
    lines.extend(
        bullet_list(
            [
                "**Labelling assumption:** `dapp_sector` is the operational definition of “ecosystem”; DeFi-like products may appear under `exchanges` — conclusions about “DeFi” must reference the sector filter used.",
                "**Eligibility assumption:** requiring two non-zero activity fields removes silent rows but may retain very large yet thinly documented protocols; sensitivity analysis = compare eligible vs primary cohort charts.",
                "**Snapshot bias:** price and flow metrics reflect one export window; anomalies in returns (`percent_change_*`) are descriptive only.",
                "**Theme keywords:** AI and DePIN/RWA masks are inclusive by design; qualitative read of `research_comments` should validate any single-DApp claim.",
                "**Falsification ideas:** if cohort-expanded analysis (lower K) reverses governance–token associations, the pattern is selection-driven; if outliers disappear when excluding one chain, the driver is chain coverage not governance.",
            ]
        )
    )
    return lines


def build_thesis_brief(df: pd.DataFrame) -> list:
    elig = df[df["analysis_eligible"]]
    lines = [
        "# Thesis brief: relevance and framing",
        "",
        "## Why this dataset matters",
        "- Token-based DApps bundle **product metrics** (users, volume, TVL) with **institutional design** (governance type, ownership, decentralisation).",
        "- The field lacks consistent, comparable labelling; this table merges manual governance coding with market/usage metrics for **cross-sectional mapping**.",
        "",
        "## Research questions supported by the pipeline",
        "",
    ]
    lines.extend(
        bullet_list(
            [
                "How do governance models and token types co-vary across ecosystems (`dapp_sector`)?",
                "Which DApps combine extreme usage with governance labels that look inconsistent (hypothesis flags + robust outliers)?",
                "How concentrated are vertical themes (prediction markets, AI, DePIN/RWA) and do they differ in token/governance mix?",
            ]
        )
    )
    lines.append("")
    lines.append("## Eligible sample size")
    lines.append(f"- **N eligible:** {len(elig)} / {len(df)}")
    lines.append("")
    lines.append("## Suggested outline for presentation")
    lines.extend(
        bullet_list(
            [
                "Relevance (this file)",
                "Methodology (`METHODOLOGY.md`)",
                "Results: figures + `KEY_INSIGHTS.md`",
                "Discussion: assumptions + anomalies (`ANOMALIES.md`, discussion section in `RESULTS_AND_DISCUSSION.md`)",
            ]
        )
    )
    return lines


def main() -> None:
    df = pd.read_csv(PREPARED_DATA_PATH)
    manifest = load_json(COHORT_MANIFEST_PATH)
    eco = pd.read_csv(ECO_SUMMARY_PATH) if ECO_SUMMARY_PATH.exists() else pd.DataFrame()
    themes = pd.read_csv(THEME_SUMMARY_PATH) if THEME_SUMMARY_PATH.exists() else pd.DataFrame()
    ann = pd.read_csv(DAPP_ANOMALIES_PATH) if DAPP_ANOMALIES_PATH.exists() else pd.DataFrame()

    write_md(OUTPUT_DIR / "METHODOLOGY.md", build_methodology(manifest, df))
    write_md(OUTPUT_DIR / "KEY_INSIGHTS.md", build_key_insights(df, eco, themes))
    write_md(OUTPUT_DIR / "ANOMALIES.md", build_anomalies(df, ann))
    write_md(OUTPUT_DIR / "RESULTS_AND_DISCUSSION.md", build_results_discussion(df))
    write_md(OUTPUT_DIR / "THESIS_BRIEF.md", build_thesis_brief(df))
    print(f"Wrote Markdown reports under {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
