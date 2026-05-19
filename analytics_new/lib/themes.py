import re
from typing import Callable, List, Tuple

import numpy as np
import pandas as pd


def _combine_text(row: pd.Series, cols: Tuple[str, ...]) -> str:
    parts: List[str] = []
    for c in cols:
        if c in row.index:
            v = row[c]
            if pd.notna(v):
                parts.append(str(v).lower())
    return " ".join(parts)


def mask_prediction_market(df: pd.DataFrame) -> pd.Series:
    m = df["dapp_category"].astype(str).str.strip() == "Prediction Market"
    text = df.apply(lambda r: _combine_text(r, ("tags", "sub_category", "name")), axis=1)
    m = m | text.str.contains(r"prediction|polymarket|augur|forecast", regex=True, na=False)
    return m


_AI_PATTERN = re.compile(
    r"\bai\b|artificial intelligence|machine learning|\bllm\b|ai gaming|ai-big-data",
    re.IGNORECASE,
)


def mask_ai_dapps(df: pd.DataFrame) -> pd.Series:
    text = df.apply(
        lambda r: _combine_text(r, ("tags", "sub_category", "research_comments", "name")),
        axis=1,
    )
    return pd.Series(text.str.contains(_AI_PATTERN, regex=True, na=False), index=df.index)


def mask_depin_rwa(df: pd.DataFrame) -> pd.Series:
    cat = df["dapp_category"].astype(str)
    m = cat.str.contains("RWA", na=False)
    text = df.apply(lambda r: _combine_text(r, ("tags", "sub_category", "research_comments")), axis=1)
    m = m | text.str.contains(r"\bdepin\b|decentralized physical|tokenized real world|move to earn", regex=True, na=False)
    m = m | text.str.contains(r"\brwa\b", regex=True, na=False)
    return m


def theme_rulebook() -> List[Tuple[str, str, Callable[[pd.DataFrame], pd.Series]]]:
    """(theme_id, description, mask_fn) for documentation."""
    return [
        (
            "prediction_markets",
            "dapp_category == Prediction Market OR text match (prediction, polymarket, augur, forecast)",
            mask_prediction_market,
        ),
        (
            "ai_dapps",
            "regex on tags, sub_category, research_comments, name: ai, llm, machine learning, ai gaming, ai-big-data",
            mask_ai_dapps,
        ),
        (
            "depin_rwa",
            "Payments/RWA category OR tags/text: depin, rwa, move to earn, tokenized real world",
            mask_depin_rwa,
        ),
    ]


def apply_themes(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for tid, _, fn in theme_rulebook():
        out[f"theme_{tid}"] = fn(out)
    return out


def strange_result_masks(df: pd.DataFrame) -> pd.DataFrame:
    """Hypothesis-style boolean columns for cross-analysis."""
    out = df.copy()
    users = pd.to_numeric(out.get("users"), errors="coerce").fillna(0)
    volume = pd.to_numeric(out.get("volume"), errors="coerce").fillna(0)
    mcap = pd.to_numeric(out.get("market_cap"), errors="coerce")
    token_type = out.get("token_type", pd.Series("", index=out.index)).astype(str)
    gov = out.get("governance_type", pd.Series("", index=out.index)).astype(str)
    decent = out.get("level_of_decentralisation", pd.Series("", index=out.index)).astype(str)
    own = out.get("ownership_status", pd.Series("", index=out.index)).astype(str)

    u_hi = users >= users.quantile(0.9)
    out["strange_centralized_high_users"] = (decent == "CENTRALIZED") & u_hi
    out["strange_governance_token_team_control"] = token_type.str.contains(
        "GOVERNANCE", na=False
    ) & (gov == "TEAM_CONTROLLED")
    out["strange_high_volume_low_mcap"] = (volume > volume.quantile(0.85)) & (
        mcap.fillna(0) < mcap.quantile(0.25)
    )
    out["strange_high_volume_missing_mcap"] = (volume > volume.quantile(0.8)) & mcap.isna()
    return out
