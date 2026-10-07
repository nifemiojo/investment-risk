from dataclasses import dataclass
from math import isclose
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class Mandate:
    """Immutable portfolio policy, including asset-level risk budgets."""

    risk_budget_by_asset: Mapping[str, float]

    def __post_init__(self) -> None:
        budgets = dict(self.risk_budget_by_asset)
        if not budgets:
            raise ValueError("Mandate must define at least one risk budget.")
        if any(budget < 0.0 for budget in budgets.values()):
            raise ValueError("Mandate risk budgets must be non-negative.")
        if not isclose(sum(budgets.values()), 1.0, abs_tol=1e-9):
            raise ValueError("Mandate risk budgets must sum to 100%.")
        object.__setattr__(self, "risk_budget_by_asset", MappingProxyType(budgets))


__all__ = ["Mandate"]


