"""Descarga IRFCL 2025-2026 (mensual) vía API del FMI.

Descarga RAPFA_USD (drenajes netos predeterminados) y RAFA_USD (reservas
oficiales totales) para los 16 países de la muestra, en frecuencia mensual,
usa la API JSON del FMI y guarda un CSV por país en data/raw/irfcl/.

Uso:
    python src/download_irfcl.py
"""

import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "raw" / "irfcl"

# 16 países de la muestra: ISO3 -> ISO2 (código que usa la API del FMI)
COUNTRIES = {
    "ARG": "AR", "BRA": "BR", "CHL": "CL", "COL": "CO",
    "CRI": "CR", "DOM": "DO", "ECU": "EC", "SLV": "SV",
    "GTM": "GT", "HND": "HN", "MEX": "MX", "NIC": "NI",
    "PAN": "PA", "PRY": "PY", "PER": "PE", "URY": "UY",
}

INDICATORS = ["RAPFA_USD", "RAFA_USD"]
BASE = (
    "https://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/IRFCL/"
    "M.{iso2}.{indicators}?startPeriod=2025-01&endPeriod=2026-12"
)


def fetch(iso2: str) -> dict:
    url = BASE.format(iso2=iso2, indicators="+".join(INDICATORS))
    with urllib.request.urlopen(url, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def parse(data: dict) -> list[dict]:
    series = data.get("CompactData", {}).get("DataSet", {}).get("Series", [])
    if isinstance(series, dict):
        series = [series]
    rows = []
    for entry in series:
        indicator = entry.get("@INDICATOR", "")
        obs = entry.get("Obs", [])
        if isinstance(obs, dict):
            obs = [obs]
        for o in obs:
            rows.append({
                "date": o.get("@TIME_PERIOD"),
                "value": o.get("@OBS_VALUE"),
                "indicator": indicator,
            })
    return rows


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for iso3, iso2 in COUNTRIES.items():
        try:
            data = fetch(iso2)
            rows = parse(data)
        except Exception as exc:
            print(f"{iso3}: ERROR {exc}")
            continue

        path = OUT / f"irfcl_{iso3.lower()}_2025_2026.csv"
        with path.open("w", encoding="utf-8") as handle:
            handle.write("date,indicator,value\n")
            for row in rows:
                handle.write(
                    f"{row['date']},{row['indicator']},{row['value']}\n"
                )
        print(f"{iso3}: {len(rows)} observaciones -> {path.name}")


if __name__ == "__main__":
    main()
