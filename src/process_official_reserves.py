from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/official"
OUT = ROOT / "data/processed/reserves_official_native.csv"
REPORT = ROOT / "data/quality_reports/reserves_official_coverage.csv"

CONFIG = {
    "ARG": {
        "country_name": "Argentina",
        "filename": "reservas-internacionales-del-bcra-20100101-20260930.csv",
        "frequency": "daily",
        "source_org": "Banco Central de la República Argentina",
        "source_series_code": "",
        "notes": "Millones de USD; cifras provisorias. Fecha original conservada.",
    },
    "CHL": {
        "country_name": "Chile",
        "filename": "F062A5STOPFUSDM.xlsx",
        "frequency": "quarterly",
        "source_org": "Banco Central de Chile",
        "source_series_code": "F062.A5.STO.PF.USD.M",
        "notes": (
            "Frecuencia observada trimestral; metadatos declaran Mensual. "
            "Fecha original conservada; sin interpolación ni cambio a fin de trimestre."
        ),
    },
    "COL": {
        "country_name": "Colombia",
        "filename": "graficador_series.xlsx",
        "frequency": "monthly",
        "source_org": "Banco de la República",
        "source_series_code": "",
        "notes": (
            "Reservas internacionales brutas, dato fin de mes. "
            "Conservar las notas metodológicas del original."
        ),
    },
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
        if country == "ARG":
            raw = pd.read_csv(path)
            dates = pd.to_datetime(
                raw.iloc[:, 0], format="%Y-%m-%d", errors="coerce"
            )
        elif country == "CHL":
            raw = pd.read_excel(path, sheet_name="Cuadro", header=2)
            dates = pd.to_datetime(raw.iloc[:, 0], errors="coerce")
        else:
            raw = pd.read_excel(path, sheet_name="Datos", header=0)
            dates = pd.to_datetime(
                raw.iloc[:, 0].astype(str).str.strip(),
                format="%d/%m/%Y", errors="coerce"
            )

        values = raw.iloc[:, 1].map(numeric)
        invalid_dates = dates.isna()

        if (invalid_dates & values.notna()).any():
            raise ValueError(
                f"{country}: fila con valor numérico y fecha inválida."
            )

        df = pd.DataFrame({"date": dates, "value": values})
        df = df.loc[~invalid_dates].sort_values("date").reset_index(drop=True)

        if df.empty:
            raise ValueError(f"{country}: serie vacía.")
        if df["date"].duplicated().any():
            raise ValueError(f"{country}: fechas duplicadas.")
        if df["value"].isna().any():
            raise ValueError(f"{country}: valores no interpretables.")
        if (df["value"] < 0).any():
            raise ValueError(f"{country}: revisar valores negativos.")

        df.insert(0, "country_iso3", country)
        df["country_name"] = config["country_name"]
        df["year"] = df["date"].dt.year
        df["frequency"] = config["frequency"]
        df["variable_id"] = "official_reserve_assets_musd"
        df["variable_name"] = "Reservas internacionales: fuente oficial nacional"
        df["unit"] = "million_usd"
        df["source_org"] = config["source_org"]
        df["source_dataset"] = "national_official_reserves"
        df["source_series_code"] = config["source_series_code"]
        df["source_file"] = path.relative_to(ROOT).as_posix()
        df["quality_flag"] = (
            "warning_frequency_metadata" if country == "CHL"
            else "pass_structural_checks"
        )
        df["notes"] = config["notes"]
        blocks.append(df)

        checks.append({
            "country_iso3": country,
            "observations": len(df),
            "first_date": df["date"].min().strftime("%Y-%m-%d"),
            "last_date": df["date"].max().strftime("%Y-%m-%d"),
            "non_observation_rows_excluded": int(invalid_dates.sum()),
            "missing_values": int(df["value"].isna().sum()),
            "duplicate_dates": int(df["date"].duplicated().sum()),
            "frequency_observed": config["frequency"],
            "quality_flag": df["quality_flag"].iloc[0],
        })

    panel = pd.concat(blocks, ignore_index=True)
    panel = panel.sort_values(["country_iso3", "date"]).reset_index(drop=True)
    coverage = pd.DataFrame(checks)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    panel.to_csv(OUT, index=False, date_format="%Y-%m-%d")
    coverage.to_csv(REPORT, index=False)

    saved = pd.read_csv(OUT)
    if len(saved) != len(panel):
        raise ValueError("El número de filas guardadas no coincide.")

    print("Producto:", OUT.relative_to(ROOT))
    print("Filas verificadas:", len(saved))
    print(coverage.to_string(index=False))

if __name__ == "__main__":
    main()
