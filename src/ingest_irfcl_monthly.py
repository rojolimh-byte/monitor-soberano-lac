"""Ingesta mensual IRFCL 2025-2026.

Convierte los CSV descargados por src/download_irfcl.py en una serie mensual
lista para el dashboard y el backtesting:

    data/raw/irfcl/irfcl_<iso3>_2025_2026.csv
        -> resultados/serie_tiempo_vulnerabilidad_mensual.csv

Uso:
    python src/ingest_irfcl_monthly.py
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "irfcl"
OUT = ROOT / "resultados" / "serie_tiempo_vulnerabilidad_mensual.csv"

COUNTRY_NAMES = {
    "ARG": "Argentina", "BRA": "Brasil", "CHL": "Chile",
    "COL": "Colombia", "CRI": "Costa Rica", "DOM": "República Dominicana",
    "ECU": "Ecuador", "SLV": "El Salvador", "GTM": "Guatemala",
    "HND": "Honduras", "MEX": "México", "NIC": "Nicaragua",
    "PAN": "Panamá", "PRY": "Paraguay", "PER": "Perú", "URY": "Uruguay",
}

INDICATORS = {"RAPFA_USD": "drenaje", "RAFA_USD": "reservas"}


def numeric(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def main():
    blocks = []
    for iso3, country in COUNTRY_NAMES.items():
        path = RAW / f"irfcl_{iso3.lower()}_2025_2026.csv"
        if not path.exists():
            print(f"{iso3}: archivo no encontrado, se omite")
            continue

        raw = pd.read_csv(path)
        raw["value"] = raw["value"].map(numeric)
        pivot = raw.pivot_table(
            index="date", columns="indicator", values="value", aggfunc="last"
        ).reset_index()

        if "RAPFA_USD" not in pivot.columns or "RAFA_USD" not in pivot.columns:
            print(f"{iso3}: indicadores incompletos, se omite")
            continue

        pivot = pivot.rename(columns={
            "RAPFA_USD": "drenaje", "RAFA_USD": "reservas", "date": "fecha"
        })
        pivot.insert(0, "pais", country)
        pivot.insert(1, "iso3", iso3)
        pivot["anio"] = pd.to_datetime(pivot["fecha"]).dt.year
        pivot["mes"] = pd.to_datetime(pivot["fecha"]).dt.month
        pivot["ratio_drenaje_reservas"] = pivot.apply(
            lambda row: (
                row["drenaje"] / row["reservas"]
                if row["reservas"] and row["reservas"] != 0
                else float("nan")
            ),
            axis=1,
        )
        blocks.append(pivot)

    if not blocks:
        print("No hay archivos IRFCL mensuales para ingestar.")
        return

    panel = pd.concat(blocks, ignore_index=True)
    panel = panel.sort_values(["pais", "fecha"]).reset_index(drop=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    panel.to_csv(OUT, index=False, date_format="%Y-%m-%d")
    print(f"Producto: {OUT.relative_to(ROOT)}")
    print(f"Filas: {len(panel)}")


if __name__ == "__main__":
    main()
