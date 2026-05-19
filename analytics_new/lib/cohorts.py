import json
from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd

from analytics_new.config import (
    COHORT_MANIFEST_PATH,
    COHORT_MAX_SIZE,
    COHORT_MIN_SIZE,
    SIGNAL_WEIGHTS,
)


def primary_sub_tag(sub_category: Any) -> str:
    if pd.isna(sub_category) or not str(sub_category).strip():
        return "(none)"
    first = str(sub_category).split(",")[0].strip()
    return first if first else "(none)"


def signal_strength_score(df: pd.DataFrame) -> pd.Series:
    score = np.zeros(len(df), dtype=float)
    for col, w in SIGNAL_WEIGHTS.items():
        if col not in df.columns:
            continue
        x = pd.to_numeric(df[col], errors="coerce").fillna(0.0).clip(lower=0.0)
        score += w * np.log1p(x.values)
    return pd.Series(score, index=df.index)


def select_cohort_for_slice(
    slice_df: pd.DataFrame,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Return selected rows and manifest entry."""
    if slice_df.empty:
        return slice_df.iloc[:0], {}
    ranked = slice_df.copy()
    ranked["_signal"] = signal_strength_score(ranked)
    ranked = ranked.sort_values(["_signal", "name"], ascending=[False, True])
    n = len(ranked)
    if n < COHORT_MIN_SIZE:
        k = n
        note = f"eligible_n={n} (<{COHORT_MIN_SIZE}): all eligible DApps included"
    else:
        k = min(COHORT_MAX_SIZE, n)
        note = f"eligible_n={n}; selected top {k} by signal score"
    chosen = ranked.head(k).drop(columns=["_signal"], errors="ignore")
    names = chosen["name"].astype(str).tolist()
    meta = {
        "n_eligible": n,
        "n_selected": len(chosen),
        "cohort_size_note": note,
        "selected_names": names,
    }
    return chosen, meta


def build_cohorts(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Add in_primary_cohort / in_secondary_cohort flags and cohort_id columns.
    """
    eligible = df[df["analysis_eligible"]].copy()
    manifest: Dict[str, Any] = {
        "parameters": {
            "COHORT_MIN_SIZE": COHORT_MIN_SIZE,
            "COHORT_MAX_SIZE": COHORT_MAX_SIZE,
            "SIGNAL_WEIGHTS": SIGNAL_WEIGHTS,
        },
        "primary_slices": [],
        "secondary_slices": [],
    }

    df = df.copy()
    df["primary_sub_tag"] = df["sub_category"].map(primary_sub_tag)
    df["in_primary_cohort"] = False
    df["in_secondary_cohort"] = False
    df["primary_cohort_id"] = ""
    df["secondary_cohort_id"] = ""

    # Primary: (sector, category)
    for (sector, cat), g in eligible.groupby(["dapp_sector", "dapp_category"], dropna=False):
        key = f"{sector}::{cat}"
        chosen, meta = select_cohort_for_slice(g)
        manifest["primary_slices"].append(
            {
                "cohort_id": key,
                "dapp_sector": str(sector),
                "dapp_category": str(cat),
                **meta,
            }
        )
        if chosen.empty:
            continue
        idx = chosen.index
        df.loc[idx, "in_primary_cohort"] = True
        df.loc[idx, "primary_cohort_id"] = key

    # Secondary: (sector, category, primary_sub_tag)
    eligible = df[df["analysis_eligible"]].copy()
    eligible["primary_sub_tag"] = eligible["sub_category"].map(primary_sub_tag)
    for (sector, cat, sub), g in eligible.groupby(
        ["dapp_sector", "dapp_category", "primary_sub_tag"], dropna=False
    ):
        key = f"{sector}::{cat}::{sub}"
        chosen, meta = select_cohort_for_slice(g)
        manifest["secondary_slices"].append(
            {
                "cohort_id": key,
                "dapp_sector": str(sector),
                "dapp_category": str(cat),
                "primary_sub_tag": str(sub),
                **meta,
            }
        )
        if chosen.empty:
            continue
        idx = chosen.index
        df.loc[idx, "in_secondary_cohort"] = True
        df.loc[idx, "secondary_cohort_id"] = key

    return df, manifest


def write_manifest(manifest: Dict[str, Any], path=None) -> None:
    p = path or COHORT_MANIFEST_PATH
    with open(p, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
