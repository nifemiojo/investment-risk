# Portfolio Configuration and Case-Study Setup

## Purpose

The portfolio should be supplied by the caller rather than being permanently defined inside `InMemoryPortfolioRepository`.

The existing default behaviour should remain available so current notebooks and interfaces do not break:

```python
portfolios = InMemoryPortfolioRepository()
portfolio = portfolios.get("60/40 Multi-Asset")
```

The new behaviour should allow a caller, such as a case-study notebook, to supply its own portfolio:

```python
portfolio = Portfolio(...)

portfolios = InMemoryPortfolioRepository(
    portfolios={portfolio.name: portfolio}
)
```

The repository remains the lookup adapter. It should not own every portfolio definition.

---

## Recommended design

### 1. `Portfolio` remains the domain object

Portfolio definitions belong in `src.domain.portfolio.Portfolio`.

A portfolio contains:

```python
Portfolio(
    name=...,
    assets=...,
    nav=...,
    risk_budget_annual_pct=...,
    mandate=...,
)
```

The mandate belongs with the portfolio because it defines the target risk budget for the same asset universe.

Example:

```python
from src.domain.mandate import Mandate
from src.domain.portfolio import Portfolio

portfolio = Portfolio(
    name="Inflation Regime Study",
    assets={
        "SPY": 0.40,
        "EFA": 0.20,
        "IEF": 0.25,
        "GLD": 0.15,
    },
    nav=10_000_000,
    risk_budget_annual_pct=0.30,
    mandate=Mandate(
        risk_budget_by_asset={
            "SPY": 0.45,
            "EFA": 0.20,
            "IEF": 0.20,
            "GLD": 0.15,
        }
    ),
)
```

The weights and mandate budgets must contain the same assets. `Portfolio` validation should enforce this.

---

### 2. Allow optional portfolios in `InMemoryPortfolioRepository`

The repository should support both default and supplied portfolios:

```python
InMemoryPortfolioRepository()
```

and:

```python
InMemoryPortfolioRepository(
    portfolios={
        portfolio.name: portfolio,
    }
)
```

Conceptually:

```python
class InMemoryPortfolioRepository:
    def __init__(
        self,
        portfolios: Mapping[str, Portfolio] | None = None,
    ):
        self._portfolios = (
            dict(portfolios)
            if portfolios is not None
            else self._default_portfolios()
        )
```

The current hardcoded portfolio should move into a private factory:

```python
@staticmethod
def _default_portfolios() -> dict[str, Portfolio]:
    return {
        "60/40 Multi-Asset": Portfolio(
            ...
        )
    }
```

This preserves the current default path:

```python
portfolios = InMemoryPortfolioRepository()
```

while allowing a case study to supply its own portfolio:

```python
portfolios = InMemoryPortfolioRepository(
    portfolios={portfolio.name: portfolio}
)
```

The repository contract remains:

```python
portfolio = portfolios.get(PORTFOLIO)
```

The engines do not need to know whether the portfolio came from the default mapping, a notebook, a YAML file, or a database.

---

## Referencing `src` from `case-studies/001-case-study.ipynb`

The notebook should add the project root to `sys.path`. It should not import files through fragile relative filesystem paths.

The project root is the directory containing:

```text
pyproject.toml
src/
case-studies/
```

Use an early notebook setup cell:

```python
import sys
from pathlib import Path

current_directory = Path.cwd().resolve()

project_root = next(
    path
    for path in (current_directory, *current_directory.parents)
    if (path / "pyproject.toml").exists()
)

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
```

The notebook can then import normally:

```python
from src.domain.mandate import Mandate
from src.domain.portfolio import Portfolio
from src.infrastructure.in_memory_portfolios import InMemoryPortfolioRepository
```

This works when the notebook is executed from either the project root or the `case-studies` directory, provided the project-root setup cell runs before the imports.

The dependency direction should be:

```text
case-studies/001-case-study.ipynb
        ↓
src.domain
src.engine
src.infrastructure
```

The `src` code should not import from `case-studies`.

---

## Case-study notebook setup

The notebook should have a portfolio-definition cell near the top.

### Parameters

```python
DATE = "2021-04-21"
PORTFOLIO = "Inflation Regime Study"
ESTIMATION_WINDOW = 252
REBALANCE_TOLERANCE = 0.05
```

### Project imports

```python
import sys
from pathlib import Path

current_directory = Path.cwd().resolve()

project_root = next(
    path
    for path in (current_directory, *current_directory.parents)
    if (path / "pyproject.toml").exists()
)

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.domain.mandate import Mandate
from src.domain.portfolio import Portfolio
from src.infrastructure.in_memory_portfolios import InMemoryPortfolioRepository
from src.infrastructure.yfinance_returns import YFinanceReturnsProvider
from src.engine.attribution_engine import AttributionEngine
from src.engine.risk_drift_engine import RiskDriftEngine
from src.engine.rebalance_trigger_engine import RebalanceTriggerEngine
```

### Define the case-study portfolio

```python
portfolio = Portfolio(
    name=PORTFOLIO,
    assets={
        "SPY": 0.40,
        "EFA": 0.20,
        "IEF": 0.25,
        "GLD": 0.15,
    },
    nav=10_000_000,
    risk_budget_annual_pct=0.30,
    mandate=Mandate(
        risk_budget_by_asset={
            "SPY": 0.45,
            "EFA": 0.20,
            "IEF": 0.20,
            "GLD": 0.15,
        }
    ),
)
```

### Composition root

```python
portfolios = InMemoryPortfolioRepository(
    portfolios={
        portfolio.name: portfolio,
    }
)

returns_provider = YFinanceReturnsProvider()

attribution_engine = AttributionEngine(
    portfolios,
    returns_provider,
)

risk_drift_engine = RiskDriftEngine()
rebalance_trigger_engine = RebalanceTriggerEngine()
```

The existing engine calls can remain name-based:

```python
attribution = attribution_engine.attribute(
    portfolio_name=PORTFOLIO,
    date=DATE,
    estimation_window=ESTIMATION_WINDOW,
)
```

This keeps the portfolio name as the application-level identifier.

---

## Why `src` should not import from `case-studies`

Avoid this direction:

```python
from case_studies.portfolios import inflation_portfolio
```

inside application code.

That would make `src` depend on a particular analysis artifact:

```text
src → case-studies
```

The correct direction is:

```text
case study → Portfolio → repository → engines
```

The case study is the consumer and supplies configuration into the application.

---

## Progression for portfolio definitions

### V1 — Define the portfolio in the notebook

```text
case-studies/001-case-study.ipynb
    defines Portfolio
    supplies Portfolio to repository
```

This is the smallest useful change.

### V2 — Reusable Python portfolio factory

If multiple notebooks use the same portfolio, create:

```text
case-studies/portfolios.py
```

with:

```python
def inflation_regime_portfolio() -> Portfolio:
    return Portfolio(...)
```

Then import it from the notebook:

```python
from case_studies.portfolios import inflation_regime_portfolio

portfolio = inflation_regime_portfolio()
```

Introduce this only when portfolio definitions are actually being duplicated.

### V3 — External configuration file

Later, portfolio definitions could be stored in a file such as:

```text
case-studies/config/60-40-multi-asset.yaml
```

Example:

```yaml
name: Inflation Regime Study
nav: 10000000
risk_budget_annual_pct: 0.30

assets:
  SPY: 0.40
  EFA: 0.20
  IEF: 0.25
  GLD: 0.15

risk_budget_by_asset:
  SPY: 0.45
  EFA: 0.20
  IEF: 0.20
  GLD: 0.15
```

This should be deferred until notebook-defined portfolios become repetitive because it introduces parsing, schema, configuration, and percentage-convention decisions.

---

## Stable repository contract

The repository should continue to expose:

```python
class PortfolioRepository(Protocol):
    def get(self, portfolio_name: str) -> Portfolio:
        ...
```

The caller decides how the repository is populated:

```python
# Existing default behaviour
portfolios = InMemoryPortfolioRepository()

# Case-study behaviour
portfolios = InMemoryPortfolioRepository(
    portfolios={portfolio.name: portfolio}
)
```

Everything downstream can remain name-based and unchanged.

---

## Recommended implementation scope

When implementing this change:

1. Update `InMemoryPortfolioRepository.__init__` to accept optional portfolios.
2. Move the current hardcoded mapping into a `_default_portfolios()` factory.
3. Preserve `InMemoryPortfolioRepository()` as the default path.
4. Add the project-root/import setup cell to `case-studies/001-case-study.ipynb`.
5. Define a `Portfolio` directly in the case-study notebook.
6. Supply it to `InMemoryPortfolioRepository`.
7. Add focused tests for:
   - the default repository still returning `60/40 Multi-Asset`;
   - a supplied portfolio being returned;
   - a supplied portfolio not being replaced by the default;
   - unknown portfolio names still raising `KeyError`.

This provides portfolio configurability without prematurely introducing a file format or a new configuration system.
