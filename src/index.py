"""Cálculo del indicador central y clasificación de vulnerabilidad."""

from dataclasses import dataclass


DOLLARIZED_COUNTRIES = {"Panamá", "Ecuador", "El Salvador"}


@dataclass(frozen=True)
class Thresholds:
    moderate: float
    high: float
    critical: float


EMITTER_THRESHOLDS = Thresholds(moderate=0.0, high=-1.0, critical=-2.0)
DOLLARIZED_THRESHOLDS = Thresholds(moderate=-0.5, high=-1.0, critical=-2.0)


def net_predetermined_ratio(net_predetermined_flows: float, reserves: float) -> float:
    """Calcula el saldo neto predeterminado sobre reservas.

    Args:
        net_predetermined_flows: entradas contractuales menos salidas contractuales.
        reserves: reservas oficiales totales en la misma moneda y unidad.

    Returns:
        Ratio cardinal. Un valor negativo implica presión potencial sobre reservas.

    Raises:
        ValueError: si las reservas no son positivas.
    """
    if reserves <= 0:
        raise ValueError("Las reservas deben ser mayores que cero.")
    return net_predetermined_flows / reserves


def classify_regime(country: str) -> str:
    """Clasifica un país como emisora o dolarizada."""
    return "Dolarizada" if country in DOLLARIZED_COUNTRIES else "Emisora"


def classify_vulnerability(ratio: float, country: str) -> str:
    """Clasifica el ratio con umbrales absolutos según régimen monetario."""
    thresholds = (
        DOLLARIZED_THRESHOLDS
        if classify_regime(country) == "Dolarizada"
        else EMITTER_THRESHOLDS
    )

    if ratio >= thresholds.moderate:
        return "Holgura o vulnerabilidad baja"
    if ratio > thresholds.high:
        return "Vulnerabilidad moderada"
    if ratio > thresholds.critical:
        return "Vulnerabilidad alta"
    return "Vulnerabilidad crítica" if classify_regime(country) == "Emisora" else "Emergencia"


def definition_range(
    net_predetermined_flows: float,
    reserves_irfcl: float,
    reserves_local: float | None,
) -> tuple[float, float] | None:
    """Devuelve el rango del ratio por definición de reservas."""
    base = net_predetermined_ratio(net_predetermined_flows, reserves_irfcl)
    if reserves_local is None or reserves_local <= 0:
        return None
    alternative = net_predetermined_ratio(net_predetermined_flows, reserves_local)
    return (min(base, alternative), max(base, alternative))


def contingency_adjusted_ratio(
    net_predetermined_flows: float,
    contingent_drains: float,
    reserves: float,
) -> float:
    """Calcula un ratio alternativo que incorpora drenajes contingentes.

    Los contingentes se suman como salidas potenciales, por lo que reducen el saldo neto.
    """
    if reserves <= 0:
        raise ValueError("Las reservas deben ser mayores que cero.")
    return (net_predetermined_flows - contingent_drains) / reserves
