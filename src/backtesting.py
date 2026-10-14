"""Backtesting ampliado del indicador de vulnerabilidad externa.

La evaluación vigente sigue siendo preliminar: solo hay dos episodios positivos
con datos disponibles. El AUC se calculará cuando la muestra incluya suficientes
episodios de crisis en múltiples países.
"""

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SERIES = ROOT / "resultados/serie_tiempo_vulnerabilidad_continua.csv"
METRICS = ROOT / "resultados/backtesting_metrics.csv"
CALIBRATION = ROOT / "resultados/backtesting_threshold_calibration.csv"

COUNTRY_BY_ISO3 = {
    "ARG": "Argentina",
    "BRA": "Brasil",
    "CHL": "Chile",
    "COL": "Colombia",
    "ECU": "Ecuador",
    "MEX": "México",
    "PER": "Perú",
    "PAN": "Panamá",
    "SLV": "El Salvador",
    "URY": "Uruguay",
    "CRI": "Costa Rica",
    "DOM": "República Dominicana",
    "GTM": "Guatemala",
    "HND": "Honduras",
    "NIC": "Nicaragua",
    "PRY": "Paraguay",
}

# Episodios candidatos. Solo se evalúan los que tengan observación del año
# previo en la serie histórica disponible.
CRISIS_EPISODES = [
    {"iso3": "ARG", "year": 2001, "type": "default"},
    {"iso3": "ECU", "year": 1999, "type": "dollarization"},
    {"iso3": "ARG", "year": 2018, "type": "currency"},
    {"iso3": "TUR", "year": 2018, "type": "currency"},
    {"iso3": "LKA", "year": 2022, "type": "default"},
    {"iso3": "BRA", "year": 1999, "type": "devaluation"},
    {"iso3": "BRA", "year": 2002, "type": "electoral"},
    {"iso3": "BRA", "year": 2015, "type": "fiscal"},
    {"iso3": "MEX", "year": 1994, "type": "tequila"},
    {"iso3": "COL", "year": 1999, "type": "banking"},
    {"iso3": "VEN", "year": 2014, "type": "currency"},
    {"iso3": "VEN", "year": 2017, "type": "default"},
    {"iso3": "DOM", "year": 2003, "type": "banking"},
    {"iso3": "JAM", "year": 2010, "type": "default"},
    {"iso3": "BRB", "year": 2018, "type": "restructuring"},
]


def crisis_prior_years() -> set[tuple[str, int]]:
    """Devuelve pares país-año previo para episodios con datos disponibles."""
    pairs = set()
    for episode in CRISIS_EPISODES:
        country = COUNTRY_BY_ISO3.get(episode["iso3"])
        if country is not None:
            pairs.add((country, episode["year"] - 1))
    return pairs


def build_panel() -> pd.DataFrame:
    df = pd.read_csv(SERIES)
    df = df[df["anio"] <= 2023].copy()
    prior_years = crisis_prior_years()
    df["crisis_next_12m"] = [
        int((pais, anio) in prior_years)
        for pais, anio in zip(df["pais"], df["anio"])
    ]
    return df.rename(columns={
        "pais": "country",
        "anio": "year",
        "drenaje": "net_predetermined_flows",
        "reservas": "reserves",
        "ratio_drenaje_reservas": "ratio",
    })


def auc_score(y_true: np.ndarray, scores: np.ndarray) -> float:
    """AUC mediante la estadística U de Mann-Whitney, sin dependencias extra."""
    positives = scores[y_true == 1]
    negatives = scores[y_true == 0]
    if len(positives) == 0 or len(negatives) == 0:
        return np.nan
    greater = sum(
        np.sum(negatives < value) + 0.5 * np.sum(negatives == value)
        for value in positives
    )
    return greater / (len(positives) * len(negatives))


def bootstrap_auc(
    y_true: np.ndarray,
    scores: np.ndarray,
    n_boot: int = 10000,
    seed: int = 42,
) -> dict | None:
    """Calcula AUC y un intervalo bootstrap al 95%.

    Devuelve None si la muestra tiene menos de cinco episodios positivos,
    porque el resultado no sería informativo.
    """
    if int(np.sum(y_true == 1)) < 5:
        return None

    rng = np.random.default_rng(seed)
    n = len(y_true)
    aucs = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        sample_y = y_true[idx]
        if len(np.unique(sample_y)) < 2:
            continue
        aucs.append(auc_score(sample_y, scores[idx]))

    if not aucs:
        return None

    aucs = np.asarray(aucs)
    return {
        "auc": auc_score(y_true, scores),
        "ci_lower": float(np.percentile(aucs, 2.5)),
        "ci_upper": float(np.percentile(aucs, 97.5)),
        "std": float(np.std(aucs)),
        "valid_replicates": int(len(aucs)),
    }


def evaluate_threshold(df: pd.DataFrame, threshold: float) -> dict:
    y_true = df["crisis_next_12m"].astype(bool)
    y_pred = df["ratio"] <= threshold

    tp = int((y_true & y_pred).sum())
    fp = int((~y_true & y_pred).sum())
    fn = int((y_true & ~y_pred).sum())
    tn = int((~y_true & ~y_pred).sum())

    recall = tp / (tp + fn) if tp + fn else np.nan
    precision = tp / (tp + fp) if tp + fp else np.nan
    f1 = (
        2 * recall * precision / (recall + precision)
        if recall and precision
        else np.nan
    )

    return {
        "threshold": threshold,
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "true_negatives": tn,
        "recall": recall,
        "precision": precision,
        "f1": f1,
        "false_positive_rate": fp / (fp + tn) if fp + tn else np.nan,
    }


def walk_forward_validation(
    df: pd.DataFrame,
    thresholds: list[float],
    train_end_years: list[int],
    test_horizon: int = 3,
) -> pd.DataFrame:
    """Validación temporal: entrena hasta un año y evalúa los siguientes."""
    rows = []
    for train_end in train_end_years:
        test = df[
            (df["year"] > train_end)
            & (df["year"] <= train_end + test_horizon)
        ]
        for threshold in thresholds:
            result = evaluate_threshold(test, threshold)
            rows.append({"train_end": train_end, **result})
    return pd.DataFrame(rows)


def calibrate_thresholds(
    df: pd.DataFrame,
    thresholds: np.ndarray | list[float],
) -> pd.DataFrame:
    """Evalúa una grilla de umbrales con recall, precisión y F1."""
    return pd.DataFrame([evaluate_threshold(df, t) for t in thresholds])


def main() -> None:
    df = build_panel()
    thresholds = [-3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0]

    metrics = pd.DataFrame([evaluate_threshold(df, t) for t in thresholds])
    METRICS.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(METRICS, index=False)

    calibration = calibrate_thresholds(
        df, np.arange(-3.0, 0.01, 0.1).round(2)
    )
    calibration.to_csv(CALIBRATION, index=False)

    y_true = df["crisis_next_12m"].to_numpy()
    scores = df["ratio"].to_numpy()
    bootstrap = bootstrap_auc(y_true, scores)

    print(metrics.to_string(index=False))
    print("\nEpisodios positivos:", int(y_true.sum()))
    if bootstrap is None:
        print(
            "AUC no calculado: se requieren al menos cinco episodios positivos "
            "en múltiples países."
        )
    else:
        print(bootstrap)


if __name__ == "__main__":
    main()
