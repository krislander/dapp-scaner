"""TVL and efficiency metrics (analytics/06 style), no sklearn."""
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


def _bool(s: pd.Series) -> pd.Series:
    if s.dtype == bool:
        return s
    return s.astype(str).str.upper().isin(["TRUE", "1"])


def performance_panel(df: pd.DataFrame, suffix: str, title: str) -> None:
    tvl = df[pd.to_numeric(df["tvl"], errors="coerce").fillna(0) > 0].copy()
    tvl["tvl"] = pd.to_numeric(tvl["tvl"], errors="coerce")
    users = pd.to_numeric(tvl["users"], errors="coerce").fillna(0)
    tvl["tvl_per_user"] = np.where(users > 0, tvl["tvl"] / users, np.nan)

    by_sec = (
        tvl.groupby("dapp_sector")["tvl"]
        .agg(["sum", "median", "count"])
        .sort_values("sum", ascending=False)
    )
    by_sec.to_csv(OUTPUT_DIR / f"05_tvl_by_sector_{suffix}.csv")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f"Performance / TVL — {title}", fontsize=12, fontweight="bold")

    ax = axes[0, 0]
    if len(tvl) > 0:
        ax.hist(tvl["tvl"], bins=40, color="steelblue", edgecolor="black", alpha=0.75)
        ax.set_xscale("log")
        ax.set_title("TVL distribution (log)")
        ax.set_xlabel("TVL USD")

    ax = axes[0, 1]
    if len(by_sec) > 0:
        top = by_sec.head(10)
        ax.barh(top.index.astype(str)[::-1], top["sum"].values[::-1], color="navy", alpha=0.8)
        ax.set_title("Total TVL by sector (top 10)")

    ax = axes[1, 0]
    le = pd.to_numeric(df["liquidity_efficiency"], errors="coerce")
    le = le[np.isfinite(le) & (le > 0) & (le < 50)]
    if len(le) > 10:
        ax.hist(le, bins=40, color="darkorange", edgecolor="black")
        ax.set_title("TVL / market cap (0–50 cap)")
        ax.set_xlabel("liquidity_efficiency")

    ax = axes[1, 1]
    vpu = pd.to_numeric(df["volume_per_user"], errors="coerce")
    vpu = vpu[np.isfinite(vpu) & (vpu > 0)]
    vpu = vpu.clip(upper=vpu.quantile(0.99))
    if len(vpu) > 10:
        ax.hist(vpu, bins=40, color="seagreen", edgecolor="black")
        ax.set_title("Volume per user (<= p99)")
        ax.set_xlabel("USD / user")

    fig.tight_layout()
    fig.savefig(FIGURES_DIR / f"05_performance_{suffix}.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    df = pd.read_csv(PREPARED_PATH)
    df["analysis_eligible"] = _bool(df["analysis_eligible"])
    df["eligible_loose"] = _bool(df["eligible_loose"])
    performance_panel(df[df["eligible_loose"]], "loose", "loose eligible")
    performance_panel(df[df["analysis_eligible"]], "strict", "strict eligible")
    print(f"Performance outputs -> {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
