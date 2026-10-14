"""Backtesting del indicador usando la serie histórica disponible."""

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SERIES = ROOT / "resultados/serie_tiempo_vulnerabilidad_continua.csv"
OUTPUT = ROOT / "resultados/backtesting_metrics.csv"

# Episodios de países del continente americano cuyo año previo está disponible.
CRISIS_PRIOR_YEARS = {
    ("Argentina", 2000),  # crisis de 2001
    ("Argentina", 2017),  # crisis de 2018
}


def build_panel() -> pd.DataFrame:
    df = pd.read_csv(SERIES)
    df = df[df["anio"] <= 2023].copy()
    df["crisis_next_12m"] = [
        int((pais, anio) in CRISIS_PRIOR_YEARS)
        for pais, anio in zip(df["pais"], df["anio"])
    ]
    df = df.rename(columns={
        "pais": "country",
        "anio": "year",
        "drenaje": "net_predetermined_flows",
        "reservas": "reserves",
        "ratio_drenaje_reservas": "ratio",
    })
    return df


def evaluate_threshold(df: pd.DataFrame, threshold: float) -> dict:
    y_true = df["crisis_next_12m"].astype(bool)
    y_pred = df["ratio"] <= threshold

    tp = int((y_true & y_pred).sum())
    fp = int((~y_true & y_pred).sum())
    fn = int((y_true & ~y_pred).sum())
    tn = int((~y_true & ~y_pred).sum())

    return {
        "threshold": threshold,
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "true_negatives": tn,
        "recall": tp / (tp + fn) if tp + fn else np.nan,
        "precision": tp / (tp + fp) if tp + fp else np.nan,
        "false_positive_rate": fp / (fp + tn) if fp + tn else np.nan,
    }


def main() -> None:
    df = build_panel()
    thresholds = [-3.0, -2.0, -1.5, -1.0, -0.5, 0.0]
    metrics = pd.DataFrame([evaluate_threshold(df, t) for t in thresholds])
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(OUTPUT, index=False)
    print(metrics.to_string(index=False))
    print("\nAdvertencia: la muestra contiene solo dos episodios positivos disponibles.")


if __name__ == "__main__":
    main()
