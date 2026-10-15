"""Conciliación de reservas IRFCL frente a fuentes locales por componentes."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReserveComponents:
    reserves_irfcl: float
    reserves_local: float
    swaps_active: float = 0.0
    non_transferable_notes: float = 0.0
    reserve_requirements: float = 0.0
    public_sector_deposits: float = 0.0
    valuation_difference: float = 0.0


def reconcile_components(components: ReserveComponents) -> dict:
    """Descompone la brecha entre reservas IRFCL y reservas locales.

    Los componentes representan partidas que pueden explicar diferencias de
    cobertura o disponibilidad entre ambas fuentes. No se asume que una brecha
    sea un error: debe documentarse por componente.
    """
    difference = components.reserves_local - components.reserves_irfcl
    explained = (
        components.swaps_active
        + components.non_transferable_notes
        + components.reserve_requirements
        + components.public_sector_deposits
        + components.valuation_difference
    )

    ratio = (
        components.reserves_irfcl / components.reserves_local
        if components.reserves_local > 0
        else None
    )

    if ratio is None:
        status = "unresolved"
    elif abs(ratio - 1) <= 0.02:
        status = "reconciled"
    elif abs(difference - explained) <= 0.01 * max(
        abs(components.reserves_irfcl), 1
    ):
        status = "documented_gap"
    else:
        status = "unresolved"

    return {
        "difference": difference,
        "explained_difference": explained,
        "unexplained_difference": difference - explained,
        "ratio_irfcl_local": ratio,
        "status": status,
    }


def adjusted_vulnerability_ratio(
    net_predetermined_flows: float,
    reserves_irfcl: float,
    reserves_local: float | None,
) -> dict:
    """Calcula el ratio base IRFCL y, si existe, el ratio con reservas locales."""
    if reserves_irfcl <= 0:
        raise ValueError("Las reservas IRFCL deben ser mayores que cero.")

    base_ratio = net_predetermined_flows / reserves_irfcl
    result = {
        "ratio_irfcl": base_ratio,
        "ratio_local": None,
        "range": (base_ratio, base_ratio),
    }

    if reserves_local is not None and reserves_local > 0:
        local_ratio = net_predetermined_flows / reserves_local
        result["ratio_local"] = local_ratio
        result["range"] = (min(base_ratio, local_ratio), max(base_ratio, local_ratio))

    return result
