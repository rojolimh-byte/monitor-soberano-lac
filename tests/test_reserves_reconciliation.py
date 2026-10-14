import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from reserves_reconciliation import (
    ReserveComponents,
    adjusted_vulnerability_ratio,
    reconcile_components,
)


def test_reconciled_within_tolerance():
    components = ReserveComponents(reserves_irfcl=100, reserves_local=101)
    result = reconcile_components(components)
    assert result["status"] == "reconciled"


def test_documented_gap():
    components = ReserveComponents(
        reserves_irfcl=100,
        reserves_local=72,
        swaps_active=20,
        non_transferable_notes=6,
        valuation_difference=2,
    )
    result = reconcile_components(components)
    assert result["status"] == "documented_gap"
    assert result["difference"] == pytest.approx(-28)


def test_unresolved_gap():
    components = ReserveComponents(reserves_irfcl=100, reserves_local=72)
    result = reconcile_components(components)
    assert result["status"] == "unresolved"


def test_dual_ratio():
    result = adjusted_vulnerability_ratio(-153, 100, 72)
    assert result["ratio_irfcl"] == pytest.approx(-1.53)
    assert result["ratio_local"] == pytest.approx(-2.125)
    assert result["range"] == pytest.approx((-2.125, -1.53))


def test_invalid_reserves():
    with pytest.raises(ValueError):
        adjusted_vulnerability_ratio(-100, 0, None)
