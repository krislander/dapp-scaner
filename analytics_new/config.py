"""
analytics_new — configuration and run order
=============================================
Run from repo root:

  python analytics_new/01_prepare_cohorts.py
  python analytics_new/02_ecosystem_analysis.py
  python analytics_new/03_dapp_level_analysis.py
  python analytics_new/04_thesis_report.py

Inputs/outputs are isolated from analytics/.
"""
from pathlib import Path

BASE_DIR = Path(__file__).parent
REPO_ROOT = BASE_DIR.parent

RAW_DATA_PATH = REPO_ROOT / "DAPP_Dataset_Nov_2025 - Final.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
FIGURES_DIR = OUTPUT_DIR / "figures"
PREPARED_DATA_PATH = OUTPUT_DIR / "prepared_data.csv"
COHORT_MANIFEST_PATH = OUTPUT_DIR / "cohort_manifest.json"
ECO_SUMMARY_PATH = OUTPUT_DIR / "ecosystem_summary.csv"
DAPP_ANOMALIES_PATH = OUTPUT_DIR / "dapp_anomalies.csv"
THEME_SUMMARY_PATH = OUTPUT_DIR / "theme_cohort_summary.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# --- Sufficiency / eligibility ---
GOV_COLUMNS = ("governance_type", "ownership_status", "level_of_decentralisation")
ACTIVITY_METRICS = ("users", "volume", "transactions", "tvl", "market_cap")
# Need at least this many of ACTIVITY_METRICS to be present and strictly > 0
MIN_ACTIVITY_SIGNALS = 2
MIN_USERS_FOR_RATIO_OUTLIERS = 1000

# --- Cohort ranking weights (log1p of positive values) ---
SIGNAL_WEIGHTS = {
    "users": 1.0,
    "volume": 1.0,
    "tvl": 0.8,
    "market_cap": 0.8,
    "transactions": 0.6,
}

COHORT_MIN_SIZE = 20
COHORT_MAX_SIZE = 50

# total_liquidity_usd in source is expressed in millions USD; multiply for comparable USD
LIQUIDITY_USD_MULTIPLIER = 1_000_000

# --- Outlier detection ---
ROBUST_Z_THRESHOLD = 3.5
TOP_PERCENTILE = 0.98
