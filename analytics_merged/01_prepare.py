"""Load Final CSV, derived features (analytics/01 style), strict eligibility, cohorts."""
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from analytics_merged.config import (
    COHORT_MANIFEST_PATH,
    OUTPUT_DIR,
    PREPARED_PATH,
    RAW_DATA_PATH,
)
from analytics_merged.lib.cohorts import build_cohorts, write_manifest
from analytics_merged.lib.completeness import add_eligibility_columns
from analytics_merged.lib.derived import add_derived_features
from analytics_merged.lib.io import load_raw_csv


def main() -> None:
    print(f"Loading {RAW_DATA_PATH} ...")
    df = load_raw_csv(RAW_DATA_PATH)
    meta = {"source_file": str(RAW_DATA_PATH), "row_count_input": len(df)}
    df = add_derived_features(df)
    df = add_eligibility_columns(df)
    df, manifest = build_cohorts(df)
    manifest["input_metadata"] = meta
    manifest["eligible_loose_n"] = int(df["eligible_loose"].sum())
    manifest["analysis_eligible_n"] = int(df["analysis_eligible"].sum())

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(PREPARED_PATH, index=False)
    write_manifest(manifest, COHORT_MANIFEST_PATH)
    print(f"Wrote {PREPARED_PATH}")
    print(f"eligible_loose: {df['eligible_loose'].sum()} | strict analysis_eligible: {df['analysis_eligible'].sum()}")


if __name__ == "__main__":
    main()
