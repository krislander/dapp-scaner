import numpy as np
import pandas as pd

from analytics_new.config import (
    ACTIVITY_METRICS,
    GOV_COLUMNS,
    MIN_ACTIVITY_SIGNALS,
)


def _activity_signal_count(row: pd.Series) -> int:
    n = 0
    for c in ACTIVITY_METRICS:
        v = row.get(c)
        if pd.notna(v) and float(v) > 0:
            n += 1
    return n


def governance_complete(row: pd.Series) -> bool:
    for c in GOV_COLUMNS:
        v = row.get(c)
        if pd.isna(v) or (isinstance(v, str) and not str(v).strip()):
            return False
    return True


def completeness_score(row: pd.Series) -> float:
    """0–1: governance (0.5) + activity signals normalized (0.5)."""
    gov = 0.5 if governance_complete(row) else 0.0
    sig = _activity_signal_count(row)
    act = 0.5 * min(1.0, sig / len(ACTIVITY_METRICS))
    return round(gov + act, 4)


def add_eligibility_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["activity_signal_count"] = out.apply(_activity_signal_count, axis=1)
    out["governance_complete"] = out.apply(governance_complete, axis=1)
    out["data_completeness_score"] = out.apply(completeness_score, axis=1)
    out["analysis_eligible"] = out["governance_complete"] & (
        out["activity_signal_count"] >= MIN_ACTIVITY_SIGNALS
    )
    return out
