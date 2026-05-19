"""Derived features aligned with analytics/01_data_preparation.py."""
import numpy as np
import pandas as pd


def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    e = df.copy()

    governance_map = {
        "NONE": 0,
        "TEAM_CONTROLLED": 1,
        "SNAPSHOT_OFFCHAIN": 2,
        "HYBRID": 3,
        "MULTISIG_WITH_COMMUNITY_INPUT": 4,
        "ONCHAIN_TOKEN_GOVERNANCE": 5,
        "DAO_WITH_TIMELOCK": 6,
    }
    ownership_map = {
        "COMPANY_OWNED": 0,
        "FOUNDATION_OWNED": 1,
        "MIXED": 2,
        "DAO_OWNED": 3,
    }
    decentralization_map = {"CENTRALIZED": 0, "SEMI_DECENTRALIZED": 1, "DECENTRALIZED": 2}

    e["gov_numeric"] = e["governance_type"].map(governance_map)
    e["own_numeric"] = e["ownership_status"].map(ownership_map)
    e["decent_numeric"] = e["level_of_decentralisation"].map(decentralization_map)

    e["governance_score"] = (
        (e["gov_numeric"].fillna(0) / 6 * 0.4)
        + (e["own_numeric"].fillna(0) / 3 * 0.3)
        + (e["decent_numeric"].fillna(0) / 2 * 0.3)
    )

    e["chain_count"] = e["chains"].fillna("").apply(
        lambda x: len([c.strip() for c in str(x).split(",") if c.strip()])
    )
    e["is_multi_chain"] = e["chain_count"] > 1

    e["market_cap_norm"] = np.log1p(pd.to_numeric(e["market_cap"], errors="coerce").fillna(0))
    e["users_norm"] = np.log1p(pd.to_numeric(e["users"], errors="coerce").fillna(0))
    e["tvl_norm"] = np.log1p(pd.to_numeric(e["tvl"], errors="coerce").fillna(0))
    mx = e["market_cap_norm"].max() or 1
    ux = e["users_norm"].max() or 1
    tx = e["tvl_norm"].max() or 1
    e["market_maturity"] = (
        e["market_cap_norm"] / mx * 0.4 + e["users_norm"] / ux * 0.3 + e["tvl_norm"] / tx * 0.3
    )

    volatility_cols = [
        "percent_change_1h",
        "percent_change_24h",
        "percent_change_7d",
        "percent_change_30d",
        "percent_change_60d",
        "percent_change_90d",
    ]
    for c in volatility_cols:
        if c not in e.columns:
            e[c] = np.nan
    e["volatility_index"] = e[volatility_cols].fillna(0).abs().mean(axis=1)

    mcap = pd.to_numeric(e["market_cap"], errors="coerce").fillna(0)
    tvl = pd.to_numeric(e["tvl"], errors="coerce").fillna(0)
    e["liquidity_efficiency"] = np.where(mcap > 0, tvl / mcap, np.nan)

    users = pd.to_numeric(e["users"], errors="coerce").fillna(0)
    txc = pd.to_numeric(e["transactions"], errors="coerce").fillna(0)
    vol = pd.to_numeric(e["volume"], errors="coerce").fillna(0)
    e["tx_per_user"] = np.where(users > 0, txc / users, np.nan)
    e["volume_per_user"] = np.where(users > 0, vol / users, np.nan)
    e["market_cap_per_user"] = np.where(users > 0, mcap / users, np.nan)

    e["has_token"] = e["token_symbol"].notna() & (e["token_symbol"].astype(str).str.strip() != "")
    e["token_type_clean"] = e["token_type"].fillna("NONE")
    e["token_type_primary"] = e["token_type_clean"].apply(
        lambda x: x.split(",")[0].strip() if x != "NONE" else "NONE"
    )
    e["is_governance_token"] = e["token_type_clean"].str.contains("GOVERNANCE", na=False)
    e["is_utility_token"] = e["token_type_clean"].str.contains("UTILITY", na=False)
    e["is_reward_token"] = e["token_type_clean"].str.contains("REWARD", na=False)
    e["is_multi_type_token"] = e["token_type_clean"].str.contains(",", na=False)

    tags_lower = e["tags"].fillna("").str.lower()
    sub_cat = e["sub_category"].fillna("")
    defi_categories = ["DEX", "Lending", "Derivatives", "Yield Aggregator"]
    e["is_defi"] = e["dapp_category"].isin(defi_categories) | (e["dapp_sector"] == "defi")
    e["is_prediction_market"] = (e["dapp_category"] == "Prediction Market") | sub_cat.str.contains(
        "Prediction Market", case=False, na=False
    )
    e["is_rwa"] = (e["dapp_category"] == "Payments/RWA") | tags_lower.str.contains("rwa", na=False)
    e["is_ai"] = sub_cat.str.contains("AI", case=False, na=False) | tags_lower.str.contains(
        r"\bai\b", na=False, regex=True
    )
    e["is_depin"] = tags_lower.str.contains("depin", na=False)
    e["is_gaming"] = (
        e["dapp_category"].isin(["NFT Gaming", "Metaverse"]) | (e["dapp_sector"] == "games")
    )
    e["is_social"] = (
        e["dapp_category"].isin(["Social Network", "SocialFi"]) | (e["dapp_sector"] == "social")
    )
    return e
