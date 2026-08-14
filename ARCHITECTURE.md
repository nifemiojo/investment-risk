# Architecture: Engine / Display Separation

**Status**: Decisions recorded, not yet implemented  
**Date**: 2026-08-02

---

## Core Principle

> The computational engine produces structured data. It has no opinion about how that data is displayed.

Notebooks are the v1 UI — but they are **thin clients**. They import modules, call functions, display results. A notebook cell should be ~10 lines of orchestration, not 100 lines of business logic.

The engine is the product. The display layer is swappable.

---

## The Trap We're Avoiding

Bad notebook projects look like this:

```
notebook_001.ipynb:  500 lines of pandas, VaR calculation embedded in cell 12
notebook_002.ipynb:  400 lines, copy-pasted the VaR logic from notebook 1 but tweaked the window
notebook_003.ipynb:  imports notebook_001? No — just copies the code again
```

The business logic is married to the display. You can't swap the UI because the UI *is* the code. This is where most quant projects die — they become a pile of notebooks that can't be reused, tested, or composed.

---

## The Architecture

```
┌─────────────────────────────────────────┐
│             ENGINE (src/)                │
│                                          │
│  src/                                    │
│  ├── portfolio.py     Portfolio class    │
│  ├── var_engine.py    VaR computation    │
│  ├── attribution.py   Risk attribution   │
│  ├── monitoring.py    Change detection   │
│  └── rebalance.py     Rebalance logic    │
│                                          │
│  Returns: DataFrames, dataclasses, dicts │
│  Knows NOTHING about display             │
└──────────────────┬──────────────────────┘
                   │
                   │  Structured data contract
                   │
     ┌─────────────┼─────────────┬──────────────┐
     ▼             ▼             ▼              ▼
┌─────────┐  ┌──────────┐  ┌─────────┐   ┌──────────┐
│Notebook │  │  Streamlit│  │  CLI    │   │  Web UI  │
│ (v1 UI) │  │ Dashboard│  │ Report  │   │ (future) │
└─────────┘  └──────────┘  └─────────┘   └──────────┘
```

The notebook is a consumer of the engine, just like a dashboard would be. Same imports, same function calls, same structured output. The display layer swaps; the engine doesn't change.

---

## Project Structure On Disk

```
historical-var/
├── src/
│   ├── __init__.py
│   ├── portfolio.py          # Portfolio dataclass, weights, validation
│   ├── var_engine.py         # VaREngine, VaRBrief dataclass
│   ├── attribution.py        # IncrementalAttributor, AttributionResult
│   ├── monitoring.py         # ChangeDetector, DiversificationMonitor
│   ├── rebalance.py          # RebalanceAnalyzer, RebalanceRecommendation
│   └── display/
│       ├── __init__.py
│       ├── brief_renderer.py     # Markdown, terminal renderers for Daily Risk Brief
│       └── review_renderer.py    # Markdown renderer for Monthly Risk Review
├── notebooks/
│   ├── 001_daily_brief.ipynb         # Thin: imports engine, shows brief
│   ├── 002_monthly_review.ipynb      # Thin: imports engine, shows review
│   └── 003_historical_replay.ipynb   # Full replay + decision journal
├── data/
│   └── prices/                       # SPY, EFA, IEF, GLD CSVs
├── tests/
│   ├── test_var_engine.py
│   ├── test_attribution.py
│   ├── test_monitoring.py
│   ├── test_rebalance.py
│   └── test_portfolio.py
├── PLAN-v1-vertical-slice.md
├── TOP-DOWN-DESIGN-METHODOLOGY.md
└── ARCHITECTURE.md
```

Key decisions:
- `src/` is the engine — importable, testable, completely independent of Jupyter
- `notebooks/` sits at the project root as a consumer, not inside `src/`
- `src/display/` is the presentation layer — takes engine output, produces formatted strings
- `tests/` mirrors `src/` module-for-module
- No `.ipynb` files inside `src/` — notebooks are always consumers, never producers of reusable logic

---

## The Data Contract: Typed Dataclasses

Engine modules return typed dataclasses — never markdown, never formatted strings:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class VaRBrief:
    """Structured output of daily VaR analysis. No display logic."""
    date: str
    var_pct: float
    var_currency: float
    budget_utilisation_pct: float
    var_percentile: float          # rank in historical distribution
    change_pct: float              # vs. last month
    change_z: float                # z-score of the change
    attribution: dict[str, float]  # {'SPY': 0.65, 'EFA': 0.22, ...}
    diversification_ratio: float
    flags: list[str]               # ['risk_elevated', 'equity_concentration']


@dataclass(frozen=True)
class RebalanceRecommendation:
    """Structured output of monthly rebalance analysis. No display logic."""
    date: str
    should_rebalance: bool
    drift: dict[str, float]           # {'SPY': +0.12, 'IEF': -0.09, ...}
    proposed_trades: dict[str, float]  # {'SPY': -180_000, 'IEF': +200_000, ...}
    rationale: str
    counterargument: str
    historical_context: str
```

Why `frozen=True`:
- Immutable — once computed, the result doesn't change
- Prevents accidental mutation in display code
- C# instinct: these are records/DTOs, not mutable objects

Why no display logic:
- `rationale` is a plain string, not markdown
- The display layer decides formatting (bold, headers, tables) — the engine supplies the content
- Same `rationale` string works in markdown, HTML, plain-text email, or a Streamlit component

---

## Engine Module Design (C# Principles, Python Syntax)

### Example: `VaREngine`

```python
class VaREngine:
    """
    Computes VaR and produces structured briefs.
    Knows nothing about notebooks, markdown, or display.
    """
    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio
    
    def daily_brief(self, returns: pd.DataFrame, date: str) -> VaRBrief:
        """Returns structured data. Caller decides how to display."""
        var_pct = self._compute_portfolio_var(returns, date)
        percentile = self._percentile_rank(returns, var_pct, date)
        change = self._var_change(returns, var_pct, date)
        attrib = self._attribution(returns, date)
        div_ratio = self._diversification_ratio(returns, date)
        flags = self._assess_flags(var_pct, percentile, change, div_ratio)
        
        return VaRBrief(
            date=date,
            var_pct=var_pct,
            var_currency=var_pct * self.portfolio.nav,
            budget_utilisation_pct=var_pct / self.portfolio.risk_budget_annual_pct,
            var_percentile=percentile,
            change_pct=change.pct,
            change_z=change.z_score,
            attribution=attrib,
            diversification_ratio=div_ratio,
            flags=flags,
        )
    
    # Private implementation — leading underscore convention
    def _compute_portfolio_var(self, returns, date): ...
    def _percentile_rank(self, returns, var, date): ...
    def _var_change(self, returns, var, date): ...
    def _attribution(self, returns, date): ...
    def _diversification_ratio(self, returns, date): ...
    def _assess_flags(self, var, pctile, change, div): ...
```

### C# Principles Mapped to Python

| C# concept | Python expression in this codebase |
|---|---|
| Immutable DTOs / records | `@dataclass(frozen=True)` — data, not behaviour |
| Constructor injection | `VaREngine.__init__(self, portfolio: Portfolio)` — dependencies passed in, not created inside |
| Public API / private implementation | Leading underscore: `_compute_portfolio_var()` — convention for internal methods |
| Single responsibility | Engine doesn't know about display. Display doesn't know about computation. |
| Explicit contracts | Type hints on all public signatures: `-> VaRBrief`, `-> dict[str, float]` |
| `internal` access modifier | `_leading_underscore` — Python's convention for "don't call this from outside" |
| XUnit test project | `pytest` in `tests/`, mirroring `src/` module structure |
| Solution / project separation | `src/` is the package, `notebooks/` is a consumer, `tests/` is a separate test project |

### Domain-Named APIs

Following the convention from the finance area AGENTS.md:

- `day` not `t`
- `trailing_vol` not `rv`
- `daily_returns` not `r`
- `sample_means` not `sm`
- `true_mu` not `mu`

Variables keep their domain meaning through type conversions. Names describe what the thing *is*, not what operation produced it.

### Import Surface

```python
from src.var_engine import VaREngine, VaRBrief
from src.attribution import IncrementalAttributor
from src.monitoring import ChangeDetector
```

Not:
```python
from src.var_engine import *        # never wildcard
from src import var_engine           # prefer named imports from module
```

---

## The Display Layer (Thin, Swappable)

Display modules take engine dataclasses as input and return formatted strings:

```python
# src/display/brief_renderer.py

from src.var_engine import VaRBrief

def render_daily_brief_markdown(brief: VaRBrief) -> str:
    """Convert a VaRBrief into markdown for notebook display."""
    return f"""
## Portfolio Risk Brief — {brief.date}

**VaR Today**: £{brief.var_currency:,.0f} ({brief.var_pct:.2%} of NAV)  
**Risk Budget**: ...utilisation bar...

### Attribution
| Asset | Contribution |
|-------|-------------|
...per-asset rows...

**Diversification Ratio**: {brief.diversification_ratio:.2f}

**Bottom Line**: {_summary_text(brief)}
"""

def render_daily_brief_terminal(brief: VaRBrief) -> str:
    """Plain-text version for CLI. Different format, same data."""
    ...

def render_daily_brief_html(brief: VaRBrief) -> str:
    """HTML for future web dashboard. Same data, different output."""
    ...
```

Multiple renderers for the same `VaRBrief`. The engine never knows which one is used.

---

## What a Thin Notebook Looks Like

```python
# Cell 1: Setup
from src.portfolio import Portfolio
from src.var_engine import VaREngine
from src.display.brief_renderer import render_daily_brief_markdown

# Cell 2: Parameters
PORTFOLIO = Portfolio(
    assets={'SPY': 0.40, 'EFA': 0.20, 'IEF': 0.25, 'GLD': 0.15},
    nav=10_000_000,
    risk_budget_annual_pct=0.15,
    var_confidence=0.95,
    var_window=252,
)
DATE = '2022-03-31'
returns = load_returns('data/prices/')

# Cell 3: Compute
engine = VaREngine(PORTFOLIO)
brief = engine.daily_brief(returns, DATE)

# Cell 4: Display
from IPython.display import Markdown
Markdown(render_daily_brief_markdown(brief))
```

Each cell is thin orchestration. The logic lives in `src/`. If you want Streamlit instead, you keep every `src/` module and write `st.write(render_daily_brief_markdown(brief))`.

---

## The Migration Path: UI Layers Without Engine Changes

```
v1 (now)              v2 (later)               v3 (future)
────────              ─────────                ──────────

Notebook              Notebook                 Web Dashboard
as UI                 as UI                    (FastAPI + React
                          │                    or Streamlit)
                          ├─ CLI report             │
                          │  (cron: daily           │
                          │   brief to email)       │
                          │                         │
     └──────────────────────┼───────────────────────┘
                            │
              ┌─────────────┴──────────────┐
              │     ENGINE (unchanged)     │
              │                            │
              │  Same modules, same        │
              │  dataclasses, same         │
              │  DataFrames. UI layers     │
              │  come and go. The engine   │
              │  doesn't care.             │
              └────────────────────────────┘
```

The engine is the investment. UI layers are consumers — built once, replaced when needed, never requiring engine changes.

---

## Testing Strategy

| Test type | Lives in | Tests what |
|---|---|---|
| Unit tests | `tests/test_var_engine.py` | `VaREngine._compute_portfolio_var()` with known returns produces expected VaR |
| Unit tests | `tests/test_attribution.py` | Incremental VaR sums to approximately portfolio VaR |
| Unit tests | `tests/test_monitoring.py` | Z-score > 2 on known outlier correctly flags |
| Unit tests | `tests/test_rebalance.py` | Drift of +12% on SPY triggers rebalance flag |
| Unit tests | `tests/test_portfolio.py` | Portfolio weights sum to 1.0, negative weights rejected |
| Integration | `tests/` or notebook | `daily_brief()` runs end-to-end on synthetic 4-asset data |
| Smoke | `notebooks/` | Historical replay runs without error on real data |

Tests verify the engine. Notebooks verify the display renders. They're different concerns.

---

## Design Decisions Log

| Decision | Rationale |
|---|---|
| Engine returns dataclasses, not dicts | Type safety, IDE autocomplete, explicit contract. Dicts are "what keys exist?" — dataclasses answer that at the type level. |
| `frozen=True` on dataclasses | Immutable results prevent accidental mutation in display code. C# instinct: records, not mutable objects. |
| `_leading_underscore` for private methods | Python convention. No `private` keyword. Signals to callers: "this is implementation detail." |
| Display layer in `src/display/`, not in notebooks | Display logic is reusable. Multiple notebooks, CLI tools, and dashboards share renderers. |
| `notebooks/` at project root, not inside `src/` | Notebooks are consumers. They import from `src/`. They are not part of the package. |
| Type hints on all public signatures | IDE support. Documentation. Catches type mismatches at development time. |
| Constructor injection for dependencies | `VaREngine(portfolio)` — the portfolio comes from outside. Testable: inject a test portfolio. |
| No C# interop in v1 | Python-only keeps the build simple. C# domain layer is a future option, not a v1 requirement. |
