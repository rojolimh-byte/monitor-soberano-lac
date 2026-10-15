"""Ingesta histórica IRFCL para episodios de crisis en las Américas.

Este script procesa los archivos IRFCL históricos colocados en
`data/raw/official/<ISO3>/`. Solo procesa los archivos disponibles; el resto
queda registrado como pendiente en el reporte de cobertura.
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/official"
OUT = ROOT / "data/processed/irfcl_history_reserves.csv"
REPORT = ROOT / "data/quality_reports/irfcl_history_coverage.csv"

# Países y años previos requeridos para los episodios de crisis compatibles.
CONFIG = {
    "ARG": {"country_name": "Argentina", "target_years": [2019], "filename": "irfcl_arg.csv"},
    "ECU": {"country_name": "Ecuador", "target_years": [1998, 2007, 2019], "filename": "irfcl_ecu.csv"},
    "MEX": {"country_name": "México", "target_years": [1981, 1993], "filename": "irfcl_mex.csv"},
    "BRA": {"country_name": "Brasil", "target_years": [1982, 1998], "filename": "irfcl_bra.csv"},
    "CHL": {"country_name": "Chile", "target_years": [1981], "filename": "irfcl_chl.csv"},
    "URY": {"country_name": "Uruguay", "target_years": [2001], "filename": "irfcl_ury.csv"},
    "VEN": {"country_name": "Venezuela", "target_years": [2013, 2016], "filename": "irfcl_ven.csv"},
    "DOM": {"country_name": "República Dominicana", "target_years": [2002], "filename": "irfcl_dom.csv"},
    "JAM": {"country_name": "Jamaica", "target_years": [2009], "filename": "irfcl_jam.csv"},
    "BRB": {"country_name": "Barbados", "target_years": [2017], "filename": "irfcl_brb.csv"},
}


def numeric(x):
    if pd.isna(x):
        return float("nan")
    if isinstance(x, (int, float)):
        return float(x)
    text = str(x).strip().replace("\u00a0", "").replace(" ", "")
    if "," in text:
        text = text.replace(".", "").replace(",", ".")
    return pd.to_numeric(text, errors="coerce")


def main():
    blocks, checks = [], []

    for country, config in CONFIG.items():
        path = RAW / country / config["filename"]
        if not path.exists():
            checks.append({
                "country_iso3": country,
                "target_years": ";".join(map(str, config["target_years"])),
                "status": "pending_source_file",
                "observations": 0,
                "years_covered": "",
                "notes": f"Archivo esperado no encontrado: {config['filename']}",
            })
            continue

        raw = pd.read_csv(path)
        dates = pd.to_datetime(raw.iloc[:, 0], errors="coerce")
        values = raw.iloc[:, 1].map(numeric)

        df = pd.DataFrame({"date": dates, "value": values})
        df = df.loc[df["date"].notna()].sort_values("date").reset_index(drop=True)

        if df.empty:
            checks.append({
                "country_iso3": country,
                "target_years": ";".join(map(str, config["target_years"])),
                "status": "empty_series",
                "observations": 0,
                "years_covered": "",
                "notes": "La serie no contiene fechas válidas.",
            })
            continue

        df.insert(0, "country_iso3", country)
        df["country_name"] = config["country_name"]
        df["year"] = df["date"].dt.year
        df["variable_id"] = "official_reserve_assets_musd"
        df["unit"] = "million_usd"
        df["source_file"] = path.relative_to(ROOT).as_posix()
        blocks.append(df)

        covered = sorted(set(df["year"]) & set(config["target_years"]))
        checks.append({
            "country_iso3": country,
            "target_years": ";".join(map(str, config["target_years"])),
            "status": "processed" if covered else "no_target_year_coverage",
            "observations": len(df),
            "years_covered": ";".join(map(str, covered)),
            "notes": "Procesado desde archivo IRFCL histórico.",
        })

    panel = pd.concat(blocks, ignore_index=True) if blocks else pd.DataFrame()
    coverage = pd.DataFrame(checks)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    if not panel.empty:
        panel.to_csv(OUT, index=False, date_format="%Y-%m-%d")
    coverage.to_csv(REPORT, index=False)

    print(coverage.to_string(index=False))
    print("\nProducto:", OUT.relative_to(ROOT) if not panel.empty else "pendiente")
    print("Reporte:", REPORT.relative_to(ROOT))


if __name__ == "__main__":
    main()
