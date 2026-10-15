import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from flows import FlowIndicators, flow_resilience
from market import MarketIndicators, cds_risk_level, is_investment_grade, market_divergence


def test_flow_resilience_bounds():
    indicators = FlowIndicators(
        exports_gdp=0.5,
        export_concentration_hhi=0.5,
        fdi_gdp=0.05,
        remittances_gdp=0.05,
    )
    assert 0 <= flow_resilience(indicators) <= 1


def test_higher_flows_increase_resilience():
    low = FlowIndicators(0.1, 0.9, 0.01, 0.01)
    high = FlowIndicators(0.9, 0.1, 0.09, 0.09)
    assert flow_resilience(high) > flow_resilience(low)


def test_cds_levels():
    assert cds_risk_level(200) == "Riesgo de mercado bajo o moderado"
    assert cds_risk_level(400) == "Riesgo elevado"
    assert cds_risk_level(700) == "Riesgo crítico"


def test_investment_grade():
    assert is_investment_grade("BBB-")
    assert not is_investment_grade("BB+")


def test_market_divergence():
    indicators = MarketIndicators(cds_spread_5y=200, credit_rating="BBB-")
    assert market_divergence(-1.5, indicators) == "Posible complacencia de mercado"
