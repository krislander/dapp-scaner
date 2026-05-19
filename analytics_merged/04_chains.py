"""Chain distribution and multichain share (analytics/09 style)."""
import sys
from collections import Counter
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from analytics_merged.config import FIGURES_DIR, OUTPUT_DIR, PREPARED_PATH


def _bool(s: pd.Series) -> pd.Series:
    if s.dtype == bool:
        return s
    return s.astype(str).str.upper().isin(["TRUE", "1"])


def chain_analysis(df: pd.DataFrame, suffix: str, title: str) -> None:
    chains_flat: list = []
    for s in df["chains"].dropna():
        chains_flat.extend([c.strip() for c in str(s).split(",") if c.strip()])
    ctr = Counter(chains_flat)
    top = ctr.most_common(15)
    multichain_pct = float(df["is_multi_chain"].mean() * 100) if len(df) else 0.0

    out = pd.DataFrame(top, columns=["chain", "deployment_count"])
    out["share_of_chain_rows_pct"] = (out["deployment_count"] / max(len(chains_flat), 1) * 100).round(2)
    out.to_csv(OUTPUT_DIR / f"04_top_chains_{suffix}.csv", index=False)

    pd.DataFrame(
        [
            {"metric": "unique_chains", "value": len(ctr)},
            {"metric": "multichain_dapp_pct", "value": round(multichain_pct, 2)},
            {"metric": "n_dapps", "value": len(df)},
        ]
    ).to_csv(OUTPUT_DIR / f"04_chain_summary_{suffix}.csv", index=False)

    fig, ax = plt.subplots(figsize=(10, 5))
    names = [t[0][:18] for t in top]
    vals = [t[1] for t in top]
    ax.barh(names[::-1], vals[::-1], color="teal", alpha=0.85)
    ax.set_title(f"Top chains by deployment count — {title}")
    ax.set_xlabel("Deployments (rows may multi-count multichain DApps)")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / f"04_chain_top15_{suffix}.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    df = pd.read_csv(PREPARED_PATH)
    for c in ("is_multi_chain", "analysis_eligible", "eligible_loose"):
        if c in df.columns:
            df[c] = _bool(df[c])
    chain_analysis(df[df["eligible_loose"]], "loose", "loose eligible")
    chain_analysis(df[df["analysis_eligible"]], "strict", "strict eligible")
    print(f"Chain outputs -> {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
