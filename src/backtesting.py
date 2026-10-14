"""Estructura inicial de backtesting del indicador de vulnerabilidad."""

from pathlib import Path

import numpy as np
import pandas as pd

from index import classify_regime, classify_vulnerability, net_predetermined_ratio

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data/processed/backtesting_panel.csv"
DEFAULT_OUTPUT = ROOT / "resultados/backtesting_metrics.csv"

REQUIRED_COLUMNS = [
    "country",
    "year",
    "net_predetermined_flows",
    "reserves",
    "crisis_next_12m",
]


def load_panel(path: Path = DEFAULT_INPUT) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas: {sorted(missing)}")
    return df


def add_scores(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["ratio"] = out.apply(
        lambda row: net_predetermined_ratio(
            row["net_predetermined_flows"], row["reserves"]
        ),
        axis=1,
    )
    out["regime"] = out["country"].apply(classify_regime)
    out["classification"] = out.apply(
        lambda row: classify_vulnerability(row["ratio"], row["country"]), axis=1
    )
    return out


def evaluate_threshold(df: pd.DataFrame, threshold: float) -> dict[str, float]:
    """Evalúa una regla: ratio <= threshold implica alerta."""
    y_true = df["crisis_next_12m"].astype(bool)
    y_pred = df["ratio"] <= threshold

    tp = int((y_true & y_pred).sum())
    fp = int((~y_true & y_pred).sum())
    fn = int((y_true & ~y_pred).sum())
    tn = int((~y_true & ~y_pred).sum())

    recall = tp / (tp + fn) if tp + fn else np.nan
    precision = tp / (tp + fp) if tp + fp else np.nan
    fpr = fp / (fp + tn) if fp + tn else np.nan

    return {
        "threshold": threshold,
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "true_negatives": tn,
        "recall": recall,
        "precision": precision,
        "false_positive_rate": fpr,
    }


def main() -> None:
    df = add_scores(load_panel())
    thresholds = [-2.0, -1.5, -1.0, -0.5, 0.0]
    metrics = pd.DataFrame([evaluate_threshold(df, t) for t in thresholds])
    DEFAULT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(DEFAULT_OUTPUT, index=False)
    print(metrics.to_string(index=False))


if __name__ == "__main__":
    main()
