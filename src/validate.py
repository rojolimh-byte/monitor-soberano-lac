from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data" / "processed" / "macro_panel_wdi.parquet"
OUTPUT_DIR = ROOT / "data" / "quality_reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RANGES = {
    "real_gdp_growth_yoy": (-30, 30),
    "inflation_cpi_yoy": (-10, 500),
    "fx_reserves_usd": (0, None),
    "central_gov_debt_gdp": (0, 300),
    "official_exchange_rate": (0, None),
    "current_account_gdp": (-50, 50),
}


def flag_row(row):
    if pd.isna(row["value"]):
        return "warning_missing"

    lower, upper = RANGES.get(row["variable_id"], (None, None))

    if lower is not None and row["value"] < lower:
        return "fail_out_of_range"

    if upper is not None and row["value"] > upper:
        return "fail_out_of_range"

    return "pass"


def main():
    df = pd.read_parquet(INPUT_FILE)

    duplicate_mask = df.duplicated(
        subset=[
            "country_iso3",
            "year",
            "variable_id",
            "source_dataset",
            "source_series_code",
        ],
        keep=False,
    )

    df["quality_flag"] = df.apply(flag_row, axis=1)
    df.loc[duplicate_mask, "quality_flag"] = "fail_duplicate"

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

    quality_summary = (
        df.groupby(["quality_flag"], as_index=False)
        .size()
        .rename(columns={"size": "observations"})
    )

    df.to_parquet(INPUT_FILE, index=False)
    coverage.to_csv(OUTPUT_DIR / "coverage_report.csv", index=False)
    quality_summary.to_csv(OUTPUT_DIR / "quality_summary.csv", index=False)

    report_date = datetime.now(timezone.utc).isoformat()

    print(f"Validación completada: {report_date}")
    print(quality_summary.to_string(index=False))


if __name__ == "__main__":
    main()
