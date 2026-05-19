"""
DApp-level outliers: robust z-scores within dapp_sector; named anomaly table.
Theme-specific mini charts.
"""
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from typing import Dict, List

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from analytics_new.config import (
    DAPP_ANOMALIES_PATH,
    FIGURES_DIR,
    MIN_USERS_FOR_RATIO_OUTLIERS,
    OUTPUT_DIR,
    PREPARED_DATA_PATH,
    ROBUST_Z_THRESHOLD,
    TOP_PERCENTILE,
)
from analytics_new.lib.themes import mask_ai_dapps, mask_depin_rwa, mask_prediction_market


def robust_z(x: np.ndarray) -> np.ndarray:
    """Modified z-score using median and MAD; 0 for degenerate series."""
    med = np.nanmedian(x)
    mad = np.nanmedian(np.abs(x - med))
    if mad == 0 or np.isnan(mad):
        return np.zeros_like(x, dtype=float)
    return 0.6745 * (x - med) / mad


def add_ratio_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    u = pd.to_numeric(out["users"], errors="coerce").clip(lower=0)
    vol = pd.to_numeric(out["volume"], errors="coerce")
    tx = pd.to_numeric(out["transactions"], errors="coerce")
    tvl = pd.to_numeric(out["tvl"], errors="coerce")
    mcap = pd.to_numeric(out["market_cap"], errors="coerce")
    out["volume_per_user"] = np.where(u >= MIN_USERS_FOR_RATIO_OUTLIERS, vol / u, np.nan)
    out["tx_per_user"] = np.where(u >= MIN_USERS_FOR_RATIO_OUTLIERS, tx / u, np.nan)
    out["tvl_to_mcap"] = np.where(mcap > 0, tvl / mcap, np.nan)
    return out


def flag_sector_outliers_fixed(df: pd.DataFrame, col: str, reason_prefix: str) -> List[Dict]:
    flags: List[Dict] = []
    for sector, g in df.groupby("dapp_sector"):
        s = pd.to_numeric(g[col], errors="coerce")
        valid = s[np.isfinite(s)]
        if len(valid) < 8:
            continue
        z_series = pd.Series(index=g.index, dtype=float)
        z_vals = robust_z(valid.values)
        z_series.loc[valid.index] = z_vals
        pct_rank = s.rank(pct=True)
        q = s.quantile(TOP_PERCENTILE)
        for ix in g.index:
            v = s.loc[ix]
            if not np.isfinite(v):
                continue
            z = z_series.loc[ix]
            if not np.isfinite(z):
                z = 0.0
            if abs(z) >= ROBUST_Z_THRESHOLD or v >= q:
                row = g.loc[ix]
                flags.append(
                    {
                        "reason": f"{reason_prefix} (sector={sector})",
                        "dapp_sector": sector,
                        "name": row.get("name", ""),
                        "dapp_category": row.get("dapp_category", ""),
                        col: float(v),
                        "robust_z": float(z),
                        "governance_type": row.get("governance_type", ""),
                        "token_type": row.get("token_type", ""),
                        "users": row.get("users", np.nan),
                        "volume": row.get("volume", np.nan),
                        "research_comments_excerpt": str(row.get("research_comments", ""))[:240],
                    }
                )
    return flags


def strange_flags_summary(df: pd.DataFrame) -> pd.DataFrame:
    cols = [c for c in df.columns if c.startswith("strange_")]
    rows = []
    for c in cols:
        m = df[c].fillna(False).astype(bool) & df["analysis_eligible"].fillna(False)
        rows.append({"flag": c, "n_eligible": int(m.sum())})
    return pd.DataFrame(rows)


def plot_theme_scatter(df: pd.DataFrame, mask: pd.Series, title: str, fname: str) -> None:
    sub = df[mask & df["analysis_eligible"]]
    if len(sub) < 3:
        return
    fig, ax = plt.subplots(figsize=(7, 5))
    u = pd.to_numeric(sub["users"], errors="coerce").fillna(0)
    v = pd.to_numeric(sub["volume"], errors="coerce").fillna(0)
    ax.scatter(np.log1p(u), np.log1p(v), alpha=0.7)
    ax.set_xlabel("log1p(users)")
    ax.set_ylabel("log1p(volume)")
    ax.set_title(title)
    for _, r in sub.iterrows():
        if pd.notna(r.get("users")) and float(r["users"] or 0) > sub["users"].quantile(0.85):
            ax.annotate(
                str(r.get("name", ""))[:22],
                (np.log1p(max(r.get("users", 0), 0)), np.log1p(max(r.get("volume", 0), 0))),
                fontsize=6,
                alpha=0.85,
            )
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / fname, dpi=150)
    plt.close(fig)


def main() -> None:
    df = pd.read_csv(PREPARED_DATA_PATH)
    df = add_ratio_columns(df)

    flags: List[Dict] = []
    for col, reason in [
        ("volume_per_user", "high_volume_per_user"),
        ("tx_per_user", "high_tx_per_user"),
        ("tvl_to_mcap", "extreme_tvl_to_mcap"),
    ]:
        base = df[df["analysis_eligible"]].copy()
        flags.extend(flag_sector_outliers_fixed(base, col, reason))

    ann = pd.DataFrame(flags)
    if len(ann):
        ann = ann.drop_duplicates(subset=["name", "reason"])
    ann.to_csv(DAPP_ANOMALIES_PATH, index=False)

    strange_flags_summary(df).to_csv(OUTPUT_DIR / "strange_hypothesis_counts.csv", index=False)

    plot_theme_scatter(
        df,
        mask_prediction_market(df),
        "Prediction-market theme (eligible): users vs volume",
        "theme_prediction_users_volume.png",
    )
    plot_theme_scatter(
        df,
        mask_ai_dapps(df),
        "AI-tagged cohort (eligible): users vs volume",
        "theme_ai_users_volume.png",
    )
    plot_theme_scatter(
        df,
        mask_depin_rwa(df),
        "DePIN / RWA theme (eligible): users vs volume",
        "theme_depin_rwa_users_volume.png",
    )

    print(f"Wrote {DAPP_ANOMALIES_PATH} ({len(ann)} rows), theme figures, strange_hypothesis_counts.csv")


if __name__ == "__main__":
    main()
