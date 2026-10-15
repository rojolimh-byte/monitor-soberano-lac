"""Indicadores de resiliencia de flujos externos.

Estos indicadores contextualizan la vulnerabilidad de stock, pero no modifican
el ratio base de drenajes netos predeterminados sobre reservas.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class FlowIndicators:
    exports_gdp: float
    export_concentration_hhi: float
    fdi_gdp: float
    remittances_gdp: float


def normalize(value: float, minimum: float, maximum: float) -> float:
    """Normaliza un valor entre 0 y 1."""
    if maximum <= minimum:
        raise ValueError("El máximo debe ser mayor que el mínimo.")
    return max(0.0, min(1.0, (value - minimum) / (maximum - minimum)))


def flow_resilience(
    indicators: FlowIndicators,
    exports_range: tuple[float, float] = (0.0, 1.0),
    hhi_range: tuple[float, float] = (0.0, 1.0),
    fdi_range: tuple[float, float] = (0.0, 0.1),
    remittances_range: tuple[float, float] = (0.0, 0.1),
) -> float:
    """Calcula un índice de resiliencia de flujos entre 0 y 1.

    Mayor apertura exportadora, menor concentración, mayor IED y mayores remesas
    implican mayor resiliencia externa.
    """
    exports = normalize(
        indicators.exports_gdp, exports_range[0], exports_range[1]
    )
    diversification = 1 - normalize(
        indicators.export_concentration_hhi, hhi_range[0], hhi_range[1]
    )
    fdi = normalize(indicators.fdi_gdp, fdi_range[0], fdi_range[1])
    remittances = normalize(
        indicators.remittances_gdp, remittances_range[0], remittances_range[1]
    )

    return (
        0.3 * exports
        + 0.2 * diversification
        + 0.3 * fdi
        + 0.2 * remittances
    )
