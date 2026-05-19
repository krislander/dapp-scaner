"""
Ecosystem-level aggregates (dapp_sector) and category breakdowns.
Compares full eligible set vs primary cohort. Writes figures + ecosystem_summary.csv.
"""
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from analytics_new.config import (
    ECO_SUMMARY_PATH,
    FIGURES_DIR,
    OUTPUT_DIR,
    PREPARED_DATA_PATH,
    THEME_SUMMARY_PATH,
)
from analytics_new.lib.themes import theme_rulebook


def sector_summary(df: pd.DataFrame, eligible_mask: pd.Series, cohort_mask: pd.Series) -> pd.DataFrame:
    rows = []
    sub_elig = df[eligible_mask]
    sub_coh = df[cohort_mask]
    for label, sub in [("eligible_all", sub_elig), ("primary_cohort", sub_coh)]:
        for sector, g in sub.groupby("dapp_sector"):
            rows.append(
                {
                    "slice": label,
                    "dapp_sector": sector,
                    "n": len(g),
                    "pct_multichain": float(g["is_multi_chain"].mean()) if len(g) else 0.0,
                    "median_users": float(g["users"].median()) if len(g) else np.nan,
                    "median_volume": float(g["volume"].median()) if len(g) else np.nan,
                    "median_tvl": float(g["tvl"].median()) if len(g) else np.nan,
                    "median_mcap": float(g["market_cap"].median()) if len(g) else np.nan,
                }
            )
    return pd.DataFrame(rows)


def governance_crosstab_counts(df: pd.DataFrame, rowkey: str, colkey: str) -> pd.DataFrame:
    return pd.crosstab(df[rowkey], df[colkey], margins=True)


def plot_sector_counts(summary: pd.DataFrame, fname: str) -> None:
    elig = summary[summary["slice"] == "eligible_all"].sort_values("n", ascending=False)
    coh = summary[summary["slice"] == "primary_cohort"].sort_values("n", ascending=False)
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(elig))
    w = 0.35
    ax.bar(x - w / 2, elig["n"].values, width=w, label="eligible")
    # align cohort bars to same sector order
    c_map = dict(zip(coh["dapp_sector"], coh["n"]))
    c_ns = [c_map.get(s, 0) for s in elig["dapp_sector"]]
    ax.bar(x + w / 2, c_ns, width=w, label="primary cohort")
    ax.set_xticks(x)
    ax.set_xticklabels(elig["dapp_sector"], rotation=35, ha="right")
    ax.set_ylabel("DApp count")
    ax.set_title("DApps by ecosystem (sector): eligible vs primary cohort")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / fname, dpi=150)
    plt.close(fig)


def plot_heatmap(ct: pd.DataFrame, title: str, fname: str) -> None:
    core = ct.drop(index="All", errors="ignore").drop(columns="All", errors="ignore")
    if core.size == 0:
        return
    fig, ax = plt.subplots(figsize=(max(8, 0.35 * len(core.columns)), max(5, 0.25 * len(core))))
    im = ax.imshow(core.values, aspect="auto", cmap="Blues")
    ax.set_xticks(range(len(core.columns)))
    ax.set_xticklabels(core.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(core.index)))
    ax.set_yticklabels(core.index)
    ax.set_title(title)
    for i in range(len(core.index)):
        for j in range(len(core.columns)):
            ax.text(j, i, int(core.values[i, j]), ha="center", va="center", fontsize=7)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / fname, dpi=150)
    plt.close(fig)


def theme_summary_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for tid, desc, fn in theme_rulebook():
        m = fn(df)
        sub = df[m & df["analysis_eligible"]]
        rows.append(
            {
                "theme": tid,
                "description": desc,
                "n_all_matched": int(m.sum()),
                "n_eligible_matched": int(len(sub)),
                "pct_governance_token": float(
                    sub["token_type"].astype(str).str.contains("GOVERNANCE", na=False).mean()
                )
                if len(sub)
                else 0.0,
                "top_governance_type": (
                    str(sub["governance_type"].dropna().mode().iloc[0])
                    if len(sub) and sub["governance_type"].notna().any()
                    else ""
                ),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    df = pd.read_csv(PREPARED_DATA_PATH)
    eligible = df["analysis_eligible"].fillna(False).astype(bool)
    cohort = df["in_primary_cohort"].fillna(False).astype(bool)

    summary = sector_summary(df, eligible, cohort)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    summary.to_csv(ECO_SUMMARY_PATH, index=False)

    plot_sector_counts(summary, "eco_sector_counts_eligible_vs_cohort.png")

    sub_e = df[eligible]
    ct = governance_crosstab_counts(sub_e, "governance_type", "token_type")
    ct.to_csv(OUTPUT_DIR / "crosstab_governance_token_eligible.csv")
    plot_heatmap(ct, "Governance type × token type (eligible)", "heatmap_gov_token_eligible.png")

    sub_c = df[cohort]
    if len(sub_c) > 5:
        ct_c = governance_crosstab_counts(sub_c, "governance_type", "token_type")
        ct_c.to_csv(OUTPUT_DIR / "crosstab_governance_token_cohort.csv")
        plot_heatmap(ct_c, "Governance type × token type (primary cohort)", "heatmap_gov_token_cohort.png")

    # Decentralisation by sector (stacked share)
    dec = (
        sub_e.groupby(["dapp_sector", "level_of_decentralisation"])
        .size()
        .unstack(fill_value=0)
    )
    dec_pct = dec.div(dec.sum(axis=1), axis=0)
    dec_pct.to_csv(OUTPUT_DIR / "decentralisation_share_by_sector.csv")
    fig, ax = plt.subplots(figsize=(10, 5))
    dec_pct.plot(kind="bar", stacked=True, ax=ax, colormap="viridis")
    ax.set_title("Decentralisation level mix by sector (eligible)")
    ax.set_xlabel("dapp_sector")
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "eco_decentralisation_stacked_by_sector.png", dpi=150)
    plt.close(fig)

    themes = theme_summary_table(df)
    themes.to_csv(THEME_SUMMARY_PATH, index=False)

    print(f"Wrote {ECO_SUMMARY_PATH}, figures in {FIGURES_DIR}, {THEME_SUMMARY_PATH}")


if __name__ == "__main__":
    main()
