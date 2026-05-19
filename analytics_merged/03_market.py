"""Market concentration and volatility (analytics/04 style), strict vs loose."""
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


def market_panel(df: pd.DataFrame, suffix: str, title: str) -> None:
    m = df[pd.to_numeric(df["market_cap"], errors="coerce").fillna(0) > 0].copy()
    if len(m) < 5:
        print(f"Skip market panel {suffix}: n={len(m)}")
        return
    m["market_cap"] = pd.to_numeric(m["market_cap"], errors="coerce")
    total = m["market_cap"].sum()
    sorted_m = m.sort_values("market_cap", ascending=False)
    top10 = sorted_m.head(10)["market_cap"].sum() / total * 100
    top50 = sorted_m.head(min(50, len(sorted_m)))["market_cap"].sum() / total * 100

    summary = pd.DataFrame(
        [
            {"metric": "n_with_mcap", "value": len(m)},
            {"metric": "top10_mcap_share_pct", "value": round(top10, 2)},
            {"metric": "top50_mcap_share_pct", "value": round(top50, 2)},
            {"metric": "total_mcap_usd", "value": total},
        ]
    )
    summary.to_csv(OUTPUT_DIR / f"03_market_concentration_{suffix}.csv", index=False)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f"Market cap — {title}", fontsize=12, fontweight="bold")

    ax = axes[0, 0]
    ax.hist(m["market_cap"], bins=40, color="steelblue", edgecolor="black", alpha=0.75)
    ax.set_xscale("log")
    ax.set_xlabel("Market cap (USD, log)")
    ax.set_ylabel("Count")
    ax.set_title("Distribution (log scale)")

    ax = axes[0, 1]
    cum = sorted_m["market_cap"].cumsum() / total * 100
    ax.plot(np.arange(1, len(cum) + 1), cum.values, color="darkgreen")
    ax.set_xlabel("Rank (by market cap)")
    ax.set_ylabel("Cumulative % of total mcap")
    ax.set_title("Concentration curve")
    ax.grid(True, alpha=0.3)

    ax = axes[1, 0]
    log_m = np.log10(m["market_cap"].clip(lower=1))
    log_r = np.log10(np.arange(1, len(m) + 1))
    y = np.sort(log_m.values)[::-1]
    if len(y) == len(log_r):
        coef = np.polyfit(log_r, y, 1)
        ax.scatter(log_r, y, s=12, alpha=0.5)
        ax.plot(log_r, np.polyval(coef, log_r), color="red", lw=2, label="OLS in log-log")
        ax.set_xlabel("log10 rank")
        ax.set_ylabel("log10 market cap")
        ax.set_title("Size vs rank (power-law visual)")
        ax.legend()

    ax = axes[1, 1]
    if "volatility_index" in m.columns:
        ax.hist(m["volatility_index"].clip(0, 200), bins=40, color="coral", edgecolor="black")
        ax.set_title("Volatility index (truncated at 200)")
        ax.set_xlabel("Mean abs % changes")

    fig.tight_layout()
    fig.savefig(FIGURES_DIR / f"03_market_dynamics_{suffix}.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    df = pd.read_csv(PREPARED_PATH)
    df["analysis_eligible"] = _bool(df["analysis_eligible"])
    df["eligible_loose"] = _bool(df["eligible_loose"])
    market_panel(df[df["eligible_loose"]], "loose", "loose eligible universe")
    market_panel(df[df["analysis_eligible"]], "strict", "strict eligible universe")
    print(f"Market outputs -> {OUTPUT_DIR}, {FIGURES_DIR}")


if __name__ == "__main__":
    main()
