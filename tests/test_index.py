import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from index import (
    classify_regime,
    classify_vulnerability,
    contingency_adjusted_ratio,
    definition_range,
    net_predetermined_ratio,
)


def test_ratio_negative_means_net_outflows():
    assert net_predetermined_ratio(-247, 100) == pytest.approx(-2.47)


def test_ratio_positive_means_net_inflows():
    assert net_predetermined_ratio(4, 100) == pytest.approx(0.04)


def test_invalid_reserves():
    with pytest.raises(ValueError):
        net_predetermined_ratio(-10, 0)


def test_regime_classification():
    assert classify_regime("Panamá") == "Dolarizada"
    assert classify_regime("Argentina") == "Emisora"


def test_emitter_thresholds():
    assert classify_vulnerability(0.04, "Brasil") == "Holgura o vulnerabilidad baja"
    assert classify_vulnerability(-0.5, "Chile") == "Vulnerabilidad moderada"
    assert classify_vulnerability(-1.5, "Argentina") == "Vulnerabilidad alta"
    assert classify_vulnerability(-2.5, "Perú") == "Vulnerabilidad crítica"


def test_dollarized_thresholds_are_stricter():
    assert classify_vulnerability(-0.75, "Ecuador") == "Vulnerabilidad moderada"
    assert classify_vulnerability(-1.5, "Panamá") == "Vulnerabilidad alta"
    assert classify_vulnerability(-2.5, "El Salvador") == "Emergencia"


def test_definition_range():
    assert definition_range(-100, 100, 80) == pytest.approx((-1.25, -1.0))
    assert definition_range(-100, 100, None) is None


def test_contingency_adjustment():
    assert contingency_adjusted_ratio(-100, 20, 100) == pytest.approx(-1.2)
