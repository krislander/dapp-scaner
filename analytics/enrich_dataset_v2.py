# enrich_dataset_v2.py
import hashlib
import pandas as pd
from datetime import date

V2_VERSION = "v2.0.0"
SNAPSHOT_DATE = str(date.today())  # set explicitly in thesis run log

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def sha256_file(path: str) -> str:
    with open(path, "rb") as f:
        return sha256_bytes(f.read())

def ensure_col(df, col, default=pd.NA):
    if col not in df.columns:
        df[col] = default

def enrich(df: pd.DataFrame) -> pd.DataFrame:
    # --- Priority 1
    for c in ["v2_ecosystem_focus","v2_sustainment_model","v2_go_to_market",
              "v2_main_revenue_generator","v2_funding_type"]:
        ensure_col(df, c)

    # --- Priority 2
    for c in ["v2_has_token","v2_governance_token_flag","v2_fee_switch_or_value_accrual_to_tokenholders",
              "v2_launch_year","v2_primary_chain","v2_open_source_flag","v2_frontend_dependence",
              "v2_admin_key_risk","v2_oracle_or_external_dependency_intensity"]:
        ensure_col(df, c)

    # --- Provenance / reproducibility
    for c in ["v2_dataset_version","v2_source_snapshot_date","v2_row_hash",
              "v2_ecosystem_focus_basis","v2_coding_confidence"]:
        ensure_col(df, c)

    df["v2_dataset_version"] = V2_VERSION
    df["v2_source_snapshot_date"] = SNAPSHOT_DATE

    # Example safe derivations (do not overwrite old fields)
    if "launch_date" in df.columns:
        df["v2_launch_year"] = pd.to_datetime(df["launch_date"], errors="coerce").dt.year

    # Token flags (conservative)
    token_symbol = df.get("token_symbol", pd.Series([""] * len(df))).astype(str).str.strip()
    token_type   = df.get("token_type", pd.Series([""] * len(df))).astype(str).str.upper()
    df["v2_has_token"] = token_symbol.ne("") | token_type.ne("")
    df["v2_governance_token_flag"] = token_type.str.contains("GOVERNANCE", na=False)

    # Row hash (stable ID for auditing changes)
    key_cols = [c for c in ["name","dapp_sector","dapp_category","sub_category","chains","token_symbol"] if c in df.columns]
    def row_hash(row):
        s = "||".join(str(row.get(c,"")) for c in key_cols).encode("utf-8")
        return sha256_bytes(s)
    df["v2_row_hash"] = df.apply(row_hash, axis=1)

    # Leave ecosystem_focus + business-model fields for coding stage (or semi-automation)
    return df

def main(input_path: str, output_path: str, sheet_name: str | None = None):
    file_hash = sha256_file(input_path)
    xls = pd.ExcelFile(input_path)

    # Choose a sheet
    sh = sheet_name or xls.sheet_names[0]
    sheets = {name: pd.read_excel(input_path, sheet_name=name) for name in xls.sheet_names}

    sheets[sh] = enrich(sheets[sh])
    sheets[sh]["v2_file_hash_sha256"] = file_hash  # add after enrichment

    with pd.ExcelWriter(output_path, engine="openpyxl") as w:
        for name, sdf in sheets.items():
            sdf.to_excel(w, sheet_name=name, index=False)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Enrich DAPP dataset with v2_* columns.")
    parser.add_argument("input_path", help="Path to CSV or Excel workbook")
    parser.add_argument("output_path", help="Path for enriched Excel output (.xlsx)")
    parser.add_argument("--sheet", default=None, help="Sheet name to enrich (Excel only; default: first sheet)")
    args = parser.parse_args()
    inp, out = args.input_path, args.output_path
    if inp.lower().endswith(".csv"):
        df = pd.read_csv(inp)
        file_hash = sha256_file(inp)
        enrich(df)
        df["v2_file_hash_sha256"] = file_hash
        with pd.ExcelWriter(out, engine="openpyxl") as w:
            df.to_excel(w, sheet_name="DApps", index=False)
    else:
        main(inp, out, args.sheet)
