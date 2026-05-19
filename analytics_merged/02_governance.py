"""Legacy-style governance distributions and crosstabs (analytics/02) on strict eligible."""
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

from analytics_merged.config import FIGURES_DIR, OUTPUT_DIR, PREPARED_PATH


def _heatmap(ax, ct: pd.DataFrame, title: str) -> None:
    core = ct.drop(index="All", errors="ignore").drop(columns="All", errors="ignore")
    if core.size == 0:
        return
    v = core.values.astype(float)
    im = ax.imshow(v, aspect="auto", cmap="Blues")
    ax.set_xticks(range(len(core.columns)))
    ax.set_xticklabels(core.columns, rotation=45, ha="right", fontsize=7)
    ax.set_yticks(range(len(core.index)))
    ax.set_yticklabels(core.index, fontsize=8)
    ax.set_title(title)
    for i in range(v.shape[0]):
        for j in range(v.shape[1]):
            ax.text(j, i, int(v[i, j]), ha="center", va="center", fontsize=6)
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)


def run(df: pd.DataFrame, suffix: str, label: str) -> None:
    if len(df) < 3:
        print(f"Skip governance plots for {label}: n={len(df)}")
        return
    gov = df["governance_type"].value_counts()
    own = df["ownership_status"].value_counts()
    dec = df["level_of_decentralisation"].value_counts()

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle(f"Governance, ownership, decentralisation ({label})", fontsize=12, fontweight="bold")
    gov.plot(kind="barh", ax=axes[0], color=plt.cm.Set3(np.linspace(0, 1, len(gov))))
    axes[0].set_title("Governance type")
    own.plot(kind="barh", ax=axes[1], color=plt.cm.Pastel1(np.linspace(0, 1, len(own))))
    axes[1].set_title("Ownership")
    dec.plot(kind="barh", ax=axes[2], color=["#d62728", "#ff7f0e", "#2ca02c"][: len(dec)])
    axes[2].set_title("Decentralisation")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / f"02_governance_distribution_{suffix}.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    clean = df.dropna(subset=["governance_type", "ownership_status", "level_of_decentralisation"])
    ct1 = pd.crosstab(clean["level_of_decentralisation"], clean["governance_type"], margins=True)
    ct2 = pd.crosstab(clean["level_of_decentralisation"], clean["ownership_status"], margins=True)
    ct1.to_csv(OUTPUT_DIR / f"crosstab_decentralisation_governance_{suffix}.csv")
    ct2.to_csv(OUTPUT_DIR / f"crosstab_decentralisation_ownership_{suffix}.csv")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    _heatmap(axes[0], ct1, f"Decentralisation × governance ({label})")
    _heatmap(axes[1], ct2, f"Decentralisation × ownership ({label})")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / f"02_governance_heatmaps_{suffix}.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    if "token_type_primary" in clean.columns:
        ct3 = pd.crosstab(clean["governance_type"], clean["token_type_primary"])
        ct3.to_csv(OUTPUT_DIR / f"crosstab_governance_token_{suffix}.csv")
        fig, ax = plt.subplots(figsize=(max(10, 0.35 * ct3.shape[1]), 5))
        im = ax.imshow(ct3.values, aspect="auto", cmap="Greens")
        ax.set_xticks(range(len(ct3.columns)))
        ax.set_xticklabels(ct3.columns, rotation=45, ha="right", fontsize=7)
        ax.set_yticks(range(len(ct3.index)))
        ax.set_yticklabels(ct3.index, fontsize=8)
        ax.set_title(f"Governance × token type ({label})")
        plt.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
        fig.tight_layout()
        fig.savefig(FIGURES_DIR / f"02_governance_token_heatmap_{suffix}.png", dpi=200, bbox_inches="tight")
        plt.close(fig)


def main() -> None:
    df = pd.read_csv(PREPARED_PATH)
    for col in ("is_multi_chain", "analysis_eligible", "in_primary_cohort", "eligible_loose"):
        if col in df.columns:
            if df[col].dtype != bool:
                df[col] = df[col].astype(str).str.upper().isin(["TRUE", "1"])
    elig = df[df["analysis_eligible"]].copy()
    cohort = df[df["in_primary_cohort"]].copy()
    loose = df[df["eligible_loose"]].copy()
    run(loose, "loose_backtest", "loose eligible — legacy-style universe")
    run(elig, "strict", "strict eligible — merged primary analysis")
    run(cohort, "cohort", "primary cohort (top-K within slices)")
    print(f"Governance figures -> {FIGURES_DIR}")


if __name__ == "__main__":
    main()
