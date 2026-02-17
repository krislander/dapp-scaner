"""
Analytics Configuration
=======================
Central configuration for all analytics scripts.
Edit the paths below before each run.
"""

from pathlib import Path

# ── Base directory (analytics/ folder) ──────────────────────────
BASE_DIR = Path(__file__).parent

# ── Input: raw dataset consumed by 01_data_preparation.py ───────
RAW_DATA_PATH = BASE_DIR.parent / "DAPP_Dataset_Nov_2025 - Final.csv"

# ── Output directory for all generated files ────────────────────
OUTPUT_DIR = BASE_DIR / "outputs_feb"

# ── Input: prepared dataset consumed by scripts 02-09 ───────────
DATA_PATH = OUTPUT_DIR / "prepared_data.csv"

# ── Ensure output directory exists on import ────────────────────
OUTPUT_DIR.mkdir(exist_ok=True)
