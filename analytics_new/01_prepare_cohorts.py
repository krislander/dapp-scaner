"""
Prepare dataset: normalize types, completeness, cohort flags, manifest.
"""
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from analytics_new.config import (
    COHORT_MANIFEST_PATH,
    OUTPUT_DIR,
    PREPARED_DATA_PATH,
    RAW_DATA_PATH,
)
from analytics_new.lib.cohorts import build_cohorts, write_manifest
from analytics_new.lib.completeness import add_eligibility_columns
from analytics_new.lib.io import load_raw_csv
from analytics_new.lib.themes import apply_themes, strange_result_masks


def main() -> None:
    print(f"Loading {RAW_DATA_PATH} ...")
    df = load_raw_csv(RAW_DATA_PATH)
    manifest_pre = {
        "source_file": str(RAW_DATA_PATH),
        "row_count_input": int(len(df)),
        "columns": list(df.columns),
    }
    df = add_eligibility_columns(df)
    df = apply_themes(df)
    df = strange_result_masks(df)
    df, cohort_manifest = build_cohorts(df)
    cohort_manifest["input_metadata"] = manifest_pre
    cohort_manifest["analysis_eligible_count"] = int(df["analysis_eligible"].sum())

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(PREPARED_DATA_PATH, index=False)
    write_manifest(cohort_manifest, COHORT_MANIFEST_PATH)
    print(f"Wrote {PREPARED_DATA_PATH} ({len(df)} rows)")
    print(f"Wrote {COHORT_MANIFEST_PATH}")
    print(f"analysis_eligible: {df['analysis_eligible'].sum()} / {len(df)}")


if __name__ == "__main__":
    main()
