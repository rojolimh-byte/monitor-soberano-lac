from datetime import datetime, timezone
from pathlib import Path
import json
import time

import pandas as pd
import requests

BASE_URL = "https://api.worldbank.org/v2"

COUNTRIES = ["ARG", "BRA", "CHL", "COL", "PER"]

START_YEAR = 2010
END_YEAR = 2025

INDICATORS = {
    "NY.GDP.MKTP.KD.ZG": {
        "variable_id": "real_gdp_growth_yoy",
        "variable_name": "Crecimiento real del PIB",
        "unit": "percent",
    },
    "FP.CPI.TOTL.ZG": {
        "variable_id": "inflation_cpi_yoy",
        "variable_name": "Inflación IPC",
        "unit": "percent",
    },
    "FI.RES.TOTL.CD": {
        "variable_id": "fx_reserves_usd",
        "variable_name": "Reservas internacionales",
        "unit": "current_usd",
    },
    "GC.DOD.TOTL.GD.ZS": {
        "variable_id": "central_gov_debt_gdp",
        "variable_name": "Deuda del gobierno central",
        "unit": "percent_gdp",
    },
    "PA.NUS.FCRF": {
        "variable_id": "official_exchange_rate",
        "variable_name": "Tipo de cambio oficial",
        "unit": "local_currency_per_usd",
    },
    "BN.CAB.XOKA.GD.ZS": {
        "variable_id": "current_account_gdp",
        "variable_name": "Cuenta corriente",
        "unit": "percent_gdp",
    },
}

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw" / "world_bank"
PROCESSED_DIR = ROOT / "data" / "processed"

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def get_indicator_data(country, indicator_code, max_attempts=4):
    url = (
        f"{BASE_URL}/country/{country}/indicator/{indicator_code}"
        f"?date={START_YEAR}:{END_YEAR}&format=json&per_page=1000"
    )

    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(url, timeout=90)
            response.raise_for_status()
            payload = response.json()

            if len(payload) < 2 or payload[1] is None:
                return [], payload

            return payload[1], payload

        except requests.exceptions.RequestException as error:
            if attempt == max_attempts:
                raise RuntimeError(
                    f"Unable to download {country} / {indicator_code} "
                    f"after {max_attempts} attempts."
                ) from error

            wait_seconds = attempt * 5
            print(
                f"Attempt {attempt} failed for {country} / {indicator_code}. "
                f"Retrying in {wait_seconds} seconds..."
            )
            time.sleep(wait_seconds)


def main():
    extracted_at = datetime.now(timezone.utc).isoformat()
    records = []

    for country in COUNTRIES:
        for indicator_code, metadata in INDICATORS.items():
            observations, raw_payload = get_indicator_data(country, indicator_code)

            raw_file = RAW_DIR / f"{country}_{indicator_code}_{extracted_at[:10]}.json"
            raw_file.write_text(
                json.dumps(raw_payload, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

            for obs in observations:
                records.append(
                    {
                        "country_iso3": country,
                        "country_name": obs["country"]["value"],
                        "date": f"{obs['date']}-12-31",
                        "year": int(obs["date"]),
                        "frequency": "annual",
                        "variable_id": metadata["variable_id"],
                        "variable_name": metadata["variable_name"],
                        "value": obs["value"],
                        "unit": metadata["unit"],
                        "source_org": "World Bank",
                        "source_dataset": "WDI",
                        "source_series_code": indicator_code,
                        "source_url": (
                            f"{BASE_URL}/country/{country}/indicator/{indicator_code}"
                        ),
                        "retrieved_at": extracted_at,
                        "last_updated_source": None,
                        "vintage": "WDI API extraction",
                        "observation_status": "actual",
                        "quality_flag": "pending",
                        "notes": None,
                    }
                )

            time.sleep(0.2)

    df = pd.DataFrame(records)
    df = df.sort_values(["country_iso3", "variable_id", "year"])

    parquet_file = PROCESSED_DIR / "macro_panel_wdi.parquet"
    csv_file = PROCESSED_DIR / "macro_panel_wdi.csv"

    df.to_parquet(parquet_file, index=False)
    df.to_csv(csv_file, index=False)

    print(f"Observaciones descargadas: {len(df):,}")
    print(f"Archivo Parquet: {parquet_file}")
    print(f"Archivo CSV: {csv_file}")


if __name__ == "__main__":
    main()
