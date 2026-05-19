import numpy as np
import pandas as pd

from analytics_new.config import LIQUIDITY_USD_MULTIPLIER

GOV_TEXT_COLS = (
    "governance_type",
    "ownership_status",
    "level_of_decentralisation",
    "research_comments",
    "tags",
    "sub_category",
)


def _parse_bool_series(s: pd.Series) -> pd.Series:
    if s.dtype == bool:
        return s
    up = s.astype(str).str.upper().str.strip()
    return up.map({"TRUE": True, "FALSE": False, "1": True, "0": False, "NAN": np.nan})


def load_raw_csv(path) -> pd.DataFrame:
    df = pd.read_csv(path)
    for c in ("is_active", "is_multi_chain"):
        if c in df.columns:
            df[c] = _parse_bool_series(df[c])
    numeric_cols = [
        "raised_capital",
        "tvl",
        "tvl_ratio",
        "market_cap",
        "circulating_supply",
        "total_supply",
        "price",
        "users",
        "volume",
        "transactions",
        "total_liquidity_usd",
        "percent_change_1h",
        "percent_change_24h",
        "percent_change_7d",
        "percent_change_30d",
        "percent_change_60d",
        "percent_change_90d",
    ]
    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    if "total_liquidity_usd" in df.columns:
        df["liquidity_usd"] = df["total_liquidity_usd"] * LIQUIDITY_USD_MULTIPLIER
    for c in GOV_TEXT_COLS:
        if c in df.columns:
            df[c] = df[c].replace("", np.nan)
    return df
