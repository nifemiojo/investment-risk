# Inversion of Control: Boundaries and Layer Separation

**Status**: Decisions recorded, not yet implemented  
**Date**: 2026-08-02

---

## Core Principle

> Dependencies point inward. The engine depends on abstractions (protocols). Infrastructure implements them. Nobody in the inner layers knows about files, APIs, or specific algorithms.

This is clean architecture translated to Python. The boundary protocol is the contract. The engine is the consumer. Infrastructure is the supplier. All wiring happens in one place — the Composition Root.

---

## The Layer Diagram

```
┌──────────────────────────────────────────────────┐
│              PRESENTATION                         │
│  src/display/ — consumes domain objects          │
│  Notebooks — imports engine, calls display        │
│                                                    │
│  Knows about: domain objects, renderers           │
│  Knows NOTHING about: computation, data I/O       │
└──────────────────────┬───────────────────────────┘
                       │  depends on
                       ▼
┌──────────────────────────────────────────────────┐
│              APPLICATION / ENGINE                 │
│  src/engine/ — orchestrates computation          │
│                                                    │
│  Knows about: domain objects, boundary protocols  │
│  Knows NOTHING about: display, data I/O,          │
│    specific VaR implementations                   │
└────────┬─────────────────────────────┬───────────┘
         │  depends on                 │  depends on
         ▼                             ▼
┌─────────────────────┐    ┌─────────────────────────┐
│    DOMAIN            │    │    BOUNDARY PROTOCOLS   │
│  src/domain/         │    │  src/boundaries/        │
│  Portfolio           │    │  RiskCalculator         │
│  VaRResult           │    │  ReturnsProvider        │
│  RiskBudget          │    │  RebalanceRule          │
│  Attribution         │    │  VaRInterpretation      │
│  Pure data,          │    │                         │
│  no behaviour        │    │  Contracts, not impl.   │
└─────────────────────┘    └──────────┬──────────────┘
                                      │  implemented by
                                      ▼
                           ┌─────────────────────────┐
                           │    INFRASTRUCTURE        │
                           │  src/infrastructure/     │
                           │  HistoricalVaR           │
                           │  CSVDailyReturnsProvider │
                           │  FixedToleranceRule      │
                           │                          │
                           │  Concrete implementations│
                           │  of boundary protocols   │
                           └─────────────────────────┘
```

---

## Rule: Dependencies Only Point Inward

| Layer | Can import from | Cannot import from |
|---|---|---|
| `domain/` | Standard library only (dataclasses, typing) | `boundaries/`, `engine/`, `infrastructure/`, `display/` |
| `boundaries/` | `domain/`, standard library (`typing.Protocol`) | `engine/`, `infrastructure/`, `display/` |
| `engine/` | `domain/`, `boundaries/` | `infrastructure/`, `display/` |
| `infrastructure/` | `domain/`, `boundaries/` | `engine/`, `display/` |
| `display/` | `domain/` | `boundaries/`, `engine/`, `infrastructure/` |
| Notebooks | Everything (at the edge, wiring is allowed) | N/A — the Composition Root |

---

## Project Structure

```
historical-var/
├── src/
│   ├── boundaries/
│   │   ├── __init__.py
│   │   ├── risk_calculator.py     # RiskCalculator protocol
│   │   ├── returns_provider.py    # ReturnsProvider protocol
│   │   ├── rebalance_rule.py      # RebalanceRule protocol
│   │   └── interpretation.py      # VaRInterpretation protocol
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── portfolio.py           # Portfolio dataclass
│   │   ├── var_result.py          # VaRResult, VaRChange dataclasses
│   │   ├── attribution.py         # Attribution, AttributionEntry
│   │   ├── drift.py               # RiskDrift, DriftEntry
│   │   └── rebalance.py           # RebalanceRecommendation, Decision, DecisionOutcome
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── var_engine.py          # VaREngine — depends on RiskCalculator, VaRInterpretation
│   │   ├── attributor.py          # IncrementalAttributor
│   │   ├── monitor.py             # ChangeDetector, DiversificationMonitor
│   │   └── rebalance_analyzer.py  # RebalanceAnalyzer — depends on RebalanceRule
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── historical_var_adapter.py  # HistoricalVaR implements RiskCalculator
│   │   ├── csv_returns.py            # CSVDailyReturnsProvider implements ReturnsProvider
│   │   └── fixed_tolerance.py        # FixedToleranceRule implements RebalanceRule
│   └── display/
│       ├── __init__.py
│       ├── brief_renderer.py
│       └── review_renderer.py
├── notebooks/
├── data/
├── tests/
├── historical_var.py           # Existing code — wrapped by infrastructure adapters
├── rolling.py                  # Existing code
├── decay.py                    # Existing code
└── ARCHITECTURE-BOUNDARIES-AND-IOC.md
```

Key decisions:
- `src/domain/` — pure data objects (dataclasses). No imports from engine, infrastructure, or boundaries.
- `src/boundaries/` — protocols (interfaces). The contract layer. Depends on nothing except domain types.
- `src/engine/` — orchestration. Depends on boundaries and domain. Never depends on infrastructure.
- `src/infrastructure/` — concrete implementations of boundary protocols. Thin adapters wrapping existing code or external libraries.
- `src/display/` — presentation. Depends on domain types. Never imported by engine or infrastructure.
- Existing `historical_var.py`, `rolling.py`, `decay.py` stay at project root — wrapped by adapters in `src/infrastructure/`, not modified.

---

## Boundary 1: RiskCalculator

The most important boundary. You already have three VaR implementations in the codebase — `historical_var()`, `decay_var()`, `rolling_var()`. V1 uses historical. V2 compares methods. The boundary exists from day one:

```python
# src/boundaries/risk_calculator.py
from typing import Protocol
import numpy as np

class RiskCalculator(Protocol):
    """Contract for computing VaR from a return series."""
    def compute(self, returns: np.ndarray, confidence: float) -> float:
        ...


# src/infrastructure/historical_var_adapter.py
class HistoricalVaR:
    """Wraps the existing function. Thin adapter — no logic duplication."""
    def compute(self, returns: np.ndarray, confidence: float) -> float:
        from historical_var import historical_var
        return historical_var(returns, confidence=confidence)


class DecayWeightedVaR:
    """Wraps the existing decay function."""
    def __init__(self, lam: float = 0.94):
        self.lam = lam
    
    def compute(self, returns: np.ndarray, confidence: float) -> float:
        from decay import decay_var
        return decay_var(returns, lam=self.lam, confidence=confidence)


# src/engine/var_engine.py
class VaREngine:
    """Depends on RiskCalculator protocol, not a concrete implementation."""
    def __init__(self, portfolio: Portfolio, calculator: RiskCalculator, 
                 interpreter: VaRInterpretation):
        self.portfolio = portfolio
        self.calculator = calculator      # protocol — injected
        self.interpreter = interpreter    # protocol — injected
    
    def _compute_portfolio_var(self, returns, date):
        portfolio_returns = self._weighted_returns(returns, date)
        return self.calculator.compute(    # delegates to protocol
            portfolio_returns, 
            self.portfolio.risk_budget.confidence,
        )
```

Why this matters even in v1:
- **Testing**: inject a stub that returns exactly 0.03 — test the percentile logic without real data
- **Comparison (v2)**: same `VaREngine`, two different calculators, one comparison notebook
- **Future methods**: add `ParametricVaR` without touching `VaREngine` at all

---

## Boundary 2: ReturnsProvider

```python
# src/boundaries/returns_provider.py
class ReturnsProvider(Protocol):
    """Contract for loading return data."""
    def load(self, assets: list[str], start: str, end: str) -> pd.DataFrame:
        ...


# src/infrastructure/csv_returns.py
class CSVDailyReturnsProvider:
    """Loads from CSV files in data/prices/."""
    def __init__(self, data_dir: str = "data/prices"):
        self.data_dir = data_dir
    
    def load(self, assets: list[str], start: str, end: str) -> pd.DataFrame:
        # Read SPY.csv, EFA.csv, etc., align dates, return DataFrame
        ...
```

V1 uses CSV. V3 might use an API. The engine never knows.

---

## Boundary 3: RebalanceRule

```python
# src/boundaries/rebalance_rule.py
class RebalanceRule(Protocol):
    """Contract for deciding whether to rebalance."""
    def should_rebalance(self, drift: RiskDrift, portfolio: Portfolio) -> bool:
        ...


# src/infrastructure/fixed_tolerance.py
class FixedToleranceRule:
    """Rebalance if any asset exceeds the tolerance band."""
    def __init__(self, tolerance: float = 0.05):
        self.tolerance = tolerance
    
    def should_rebalance(self, drift: RiskDrift, portfolio: Portfolio) -> bool:
        return any(abs(entry.drift) > self.tolerance for entry in drift.entries)
```

V1 has a fixed band. Future versions might add volatility-adjusted bands or cost-aware thresholds — swap the implementation, zero engine changes.

---

## Boundary 4: VaRInterpretation

```python
# src/boundaries/interpretation.py
class VaRInterpretation(Protocol):
    """Contract for mapping VaR metrics to plain language."""
    def describe_level(self, percentile: float) -> str:
        ...
    def describe_change(self, z_score: float) -> str:
        ...


class StandardInterpretation:
    def describe_level(self, percentile: float) -> str:
        if percentile >= 0.95: return "far beyond this portfolio's norm, escalate"
        if percentile >= 0.90: return "unusually high for this portfolio, investigate"
        if percentile >= 0.80: return "notably above this portfolio's norm, worth a look"
        if percentile >= 0.50: return "about average for this portfolio"
        return "lighter than usual for this portfolio"
```

V1 has one interpretation. V5 might have a "client letter" interpretation that uses softer language. The engine calls `self.interpreter.describe_level(percentile)` — it doesn't know which words come out.

---

## Composition Root: Assembly at the Edge

All wiring happens in one place — a notebook cell or `__main__`. The engine modules never instantiate their own dependencies:

```python
# Composition Root — lives at the edge: notebook cell or __main__
from src.domain.portfolio import Portfolio
from src.engine.var_engine import VaREngine
from src.engine.attributor import IncrementalAttributor
from src.engine.monitor import ChangeDetector, DiversificationMonitor
from src.engine.rebalance_analyzer import RebalanceAnalyzer
from src.boundaries.risk_calculator import RiskCalculator
from src.boundaries.rebalance_rule import RebalanceRule
from src.boundaries.interpretation import VaRInterpretation
from src.infrastructure.historical_var_adapter import HistoricalVaR
from src.infrastructure.csv_returns import CSVDailyReturnsProvider
from src.infrastructure.fixed_tolerance import FixedToleranceRule

# Infrastructure — concrete implementations
calculator: RiskCalculator = HistoricalVaR()
returns_provider = CSVDailyReturnsProvider("data/prices")
rebalance_rule: RebalanceRule = FixedToleranceRule(tolerance=0.05)
interpreter: VaRInterpretation = StandardInterpretation()

# Domain
portfolio = Portfolio(
    assets={'SPY': 0.40, 'EFA': 0.20, 'IEF': 0.25, 'GLD': 0.15},
    nav=10_000_000,
    risk_budget_annual_pct=0.15,
    var_confidence=0.95,
    var_window=252,
    risk_allocation_target={'SPY': 0.40, 'EFA': 0.20, 'IEF': 0.25, 'GLD': 0.15},
)

# Engine — receives dependencies, creates none
engine = VaREngine(portfolio, calculator, interpreter)
attributor = IncrementalAttributor(portfolio, calculator)
detector = ChangeDetector()
monitor = DiversificationMonitor()
rebalance = RebalanceAnalyzer(portfolio, rebalance_rule)

# Data — loaded by the provider, not the engine
returns = returns_provider.load(
    assets=['SPY', 'EFA', 'IEF', 'GLD'],
    start='2020-01-01',
    end='2024-12-31',
)

# Use
brief = engine.daily_brief(returns, '2022-03-31')
```

The engine modules never see `HistoricalVaR` — they only see `RiskCalculator`. The notebook cell is the **Composition Root** — the single place where concrete types are wired to abstractions.

---

## What Gets Injected vs. What's Internal

Not everything needs an interface. The rule: inject things that might change independently. Keep things that are stable implementation details.

| Inject (boundary protocol) | Don't inject (internal to engine) |
|---|---|
| VaR calculation method (`RiskCalculator`) | Weighted return computation (`Σ w × r` — never changes) |
| Data source (`ReturnsProvider`) | Date alignment logic (pandas internals) |
| Rebalance tolerance rule (`RebalanceRule`) | Z-score formula (math doesn't change) |
| Interpretation thresholds/language (`VaRInterpretation`) | Percentile computation (function of sorted data) |
| | Dataclass constructors (they're just data) |

The test: "Would I ever want to swap this for a different implementation?" If yes → boundary. If no → internal.

---

## Why Protocols, Not ABCs

Python's `typing.Protocol` (PEP 544) provides structural subtyping — any object with a `compute` method that matches the signature satisfies `RiskCalculator`. No explicit inheritance needed:

```python
# This works — no class hierarchy required
class HistoricalVaR:
    def compute(self, returns: np.ndarray, confidence: float) -> float:
        ...  # satisfies RiskCalculator by structure, not inheritance

# So does a stub for testing
class StubCalculator:
    def compute(self, returns: np.ndarray, confidence: float) -> float:
        return 0.03

# Both are valid RiskCalculator instances — no implements keyword needed
```

This is Python's duck typing with type-checker support. It's lighter weight than ABCs and doesn't force an inheritance hierarchy.

---

## C# Principles Mapped to Python

| C# concept | Python expression in this codebase |
|---|---|
| Interface / contract | `typing.Protocol` — structural subtyping, no inheritance hierarchy needed |
| Inversion of Control / DI | Engine depends on `RiskCalculator` protocol. Infrastructure implements it. Engine never imports infrastructure. |
| Constructor injection | `VaREngine.__init__(self, portfolio, calculator, interpreter)` — all dependencies passed in |
| Composition Root | A single notebook cell (or `__main__`) wires all concrete types. Nowhere else in the codebase creates dependencies. |
| Adapter pattern | `src/infrastructure/historical_var_adapter.py` wraps existing `historical_var()` behind `RiskCalculator` — no modification to existing code |
| Single responsibility (layered) | Engine doesn't know about display. Infrastructure doesn't know about orchestration. Domain doesn't know about anything. |

---

## Design Decisions Log

| Decision | Rationale |
|---|---|
| Protocols for boundaries, not ABCs | Structural subtyping. Lighter weight. Any object with matching methods satisfies the contract — no inheritance hierarchy forced. |
| `domain/` has zero imports from other layers | Pure data has no reason to know about computation, IO, or display. Keeps domain portable, testable, and reusable. |
| `engine/` depends on `boundaries/`, never `infrastructure/` | Inversion of control. The engine doesn't know which VaR method it's using — just that one was provided. Swap infrastructure without touching engine. |
| Existing code wrapped in adapters, not modified | `historical_var.py`, `rolling.py`, `decay.py` stay as-is. Thin adapters delegate. Zero regression risk on working code. |
| Single Composition Root (notebook cell) | Only one place in the codebase wires concrete types. Nowhere else creates dependencies. Prevents scattered `HistoricalVaR()` calls across the codebase. |
| Stub-friendly boundaries | Every protocol can be replaced with a stub in tests. `RiskCalculator` → `StubCalculator(returns=0.03)`. No mocking framework needed. |
