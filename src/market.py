"""Indicadores de mercado para validar divergencias entre fundamentos y percepción.

Los CDS y las calificaciones no modifican el ratio base: sirven como capa de
validación externa.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class MarketIndicators:
    cds_spread_5y: float
    credit_rating: str


def cds_risk_level(cds_spread_5y: float) -> str:
    """Clasifica el CDS a 5 años en puntos básicos."""
    if cds_spread_5y < 300:
        return "Riesgo de mercado bajo o moderado"
    if cds_spread_5y < 600:
        return "Riesgo elevado"
    return "Riesgo crítico"


def is_investment_grade(credit_rating: str) -> bool:
    """Determina si una calificación en moneda extranjera es grado de inversión."""
    investment_grades = {
        "AAA", "AA+", "AA", "AA-", "A+", "A", "A-",
        "BBB+", "BBB", "BBB-",
    }
    return credit_rating.upper() in investment_grades


def market_divergence(
    vulnerability_ratio: float,
    indicators: MarketIndicators,
) -> str:
    """Identifica divergencias entre vulnerabilidad fundamental y percepción."""
    high_fundamental_risk = vulnerability_ratio <= -1.0
    high_market_risk = indicators.cds_spread_5y >= 600

    if high_fundamental_risk and not high_market_risk:
        return "Posible complacencia de mercado"
    if not high_fundamental_risk and high_market_risk:
        return "Posible prima de riesgo adicional no explicada por el ratio"
    if high_fundamental_risk and high_market_risk:
        return "Fundamentos y percepción de mercado alineados"
    return "Sin divergencia relevante"
