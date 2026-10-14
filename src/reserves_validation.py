"""Validación y conciliación de reservas IRFCL frente a fuentes locales."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "data/validation/reconciliation_template.csv"
OUTPUT = ROOT / "data/quality_reports/reserves_reconciliation.csv"

REQUIRED_COLUMNS = [
    "country",
    "country_iso3",
    "irfcl_date",
    "local_date",
    "reserves_irfcl_usd_mn",
    "reserves_local_usd_mn",
]


def load_reconciliation(path: Path = TEMPLATE) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas obligatorias: {sorted(missing)}")
    return df


def reconcile(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["reserves_irfcl_usd_mn"] = pd.to_numeric(
        out["reserves_irfcl_usd_mn"], errors="coerce"
    )
    out["reserves_local_usd_mn"] = pd.to_numeric(
        out["reserves_local_usd_mn"], errors="coerce"
    )

    out["difference_usd_mn"] = (
        out["reserves_local_usd_mn"] - out["reserves_irfcl_usd_mn"]
    )
    out["ratio_irfcl_local"] = (
        out["reserves_irfcl_usd_mn"] / out["reserves_local_usd_mn"]
    )

    out["status"] = "unresolved"
    has_local = out["reserves_local_usd_mn"].notna() & (out["reserves_local_usd_mn"] > 0)
    documented = out.get("explanation", pd.Series(index=out.index, dtype="object")).notna()
    out.loc[has_local & documented, "status"] = "documented_gap"
    out.loc[
        has_local & out["ratio_irfcl_local"].between(0.98, 1.02),
        "status",
    ] = "reconciled"
    return out


def main() -> None:
    df = reconcile(load_reconciliation())
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT, index=False)
    print(f"Reporte generado: {OUTPUT}")
    print(df[["country", "ratio_irfcl_local", "status"]].to_string(index=False))


if __name__ == "__main__":
    main()
