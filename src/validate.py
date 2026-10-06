from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data/processed/macro_panel_wdi.csv"
OUTPUT_DIR = ROOT / "data/quality_reports"

RANGES = {
    "real_gdp_growth_yoy": (-30, 30),
    "inflation_cpi_yoy": (-10, 500),
    "fx_reserves_usd": (0, None),
    "central_gov_debt_gdp": (0, 300),
    "official_exchange_rate": (0, None),
    "current_account_gdp": (-50, 50),
}

KEY = [
    "country_iso3", "year", "variable_id",
    "source_dataset", "source_series_code",
]

def flag_row(row):
    if pd.isna(row["value"]):
        return "warning_missing"
    lower, upper = RANGES.get(row["variable_id"], (None, None))
    if lower is not None and row["value"] < lower:
        return "warning_review_range"
    if upper is not None and row["value"] > upper:
        return "warning_review_range"
    return "pass_structural_checks"

def main():
    df = pd.read_csv(INPUT_FILE)

    required = set(KEY + ["value"])
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas: {sorted(missing)}")

    original_values = df["value"]
    numeric_values = pd.to_numeric(original_values, errors="coerce")
    invalid_numeric = original_values.notna() & numeric_values.isna()
    if invalid_numeric.any():
        raise ValueError("Hay valores no vacíos que no son numéricos.")

    df["value"] = numeric_values
    flags = df.apply(flag_row, axis=1)

    duplicates = df.duplicated(KEY, keep=False)
    invalid_key = df[KEY].isna().any(axis=1)
    flags.loc[duplicates] = "fail_duplicate"
    flags.loc[invalid_key] = "fail_missing_key"

    detail = df.copy()
    detail["validation_flag"] = flags

    coverage = (
        df.assign(non_missing=df["value"].notna())
        .groupby(["country_iso3", "variable_id"], as_index=False)
        .agg(
            observations=("year", "size"),
            non_missing=("non_missing", "sum"),
            first_year=("year", "min"),
            last_year=("year", "max"),
        )
    )
    coverage["coverage_pct"] = (
        100 * coverage["non_missing"] / coverage["observations"]
    ).round(1)

    summary = (
        detail.groupby("validation_flag", as_index=False)
        .size().rename(columns={"size": "observations"})
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    coverage.to_csv(OUTPUT_DIR / "wdi_validation_coverage.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "wdi_validation_summary.csv", index=False)
    detail.loc[
        detail["validation_flag"] != "pass_structural_checks"
    ].to_csv(OUTPUT_DIR / "wdi_validation_issues.csv", index=False)

    print("Entrada:", INPUT_FILE.relative_to(ROOT))
    print("Filas revisadas:", len(df))
    print(summary.to_string(index=False))
    print("\nEl CSV de entrada no se modificó.")
    print("Los rangos son alertas de revisión, no pruebas de error económico.")

    if duplicates.any() or invalid_key.any():
        raise ValueError("Se detectaron problemas estructurales; revisar informes.")

if __name__ == "__main__":
    main()
