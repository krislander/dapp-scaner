"""
analytics_merged — strict cohort + legacy-style empirical analytics
===================================================================
Run from repo root (see analytics_merged/README.md).

Uses Final CSV, analytics_new-style cohort ranking, and analytics/-style
derived features and charts. Eligibility is **stricter** than analytics_new.
"""
from pathlib import Path

BASE_DIR = Path(__file__).parent
REPO_ROOT = BASE_DIR.parent

RAW_DATA_PATH = REPO_ROOT / "DAPP_Dataset_Nov_2025 - Final.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
FIGURES_DIR = OUTPUT_DIR / "figures"
PREPARED_PATH = OUTPUT_DIR / "prepared_merged.csv"
COHORT_MANIFEST_PATH = OUTPUT_DIR / "cohort_manifest.json"
BACKTEST_METRICS_PATH = OUTPUT_DIR / "backtest_headline_metrics.csv"
CONCEPT_INSIGHTS_PATH = OUTPUT_DIR / "conceptual_insights.csv"
CONCEPT_ANOMALIES_PATH = OUTPUT_DIR / "conceptual_anomalies.csv"
DISCUSSION_TOPICS_PATH = OUTPUT_DIR / "discussion_topics.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# --- Strict eligibility (reduces N vs analytics_new) ---
GOV_COLUMNS = ("governance_type", "ownership_status", "level_of_decentralisation")
ACTIVITY_METRICS = ("users", "volume", "transactions", "tvl", "market_cap")
MIN_ACTIVITY_SIGNALS_STRICT = 4
MIN_USERS_STRICT = 10_000
REQUIRE_MARKET_OR_TVL = True

# --- Loose eligibility (mirrors analytics_new for backtest comparison) ---
MIN_ACTIVITY_SIGNALS_LOOSE = 2

# --- Cohort (same logic as analytics_new) ---
SIGNAL_WEIGHTS = {
    "users": 1.0,
    "volume": 1.0,
    "tvl": 0.8,
    "market_cap": 0.8,
    "transactions": 0.6,
}
COHORT_MIN_SIZE = 20
COHORT_MAX_SIZE = 50
LIQUIDITY_USD_MULTIPLIER = 1_000_000
