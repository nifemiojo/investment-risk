# Investment Risk

Portfolio risk monitoring and decision-support system. Measures risk, attributes it to sources, detects drift from target allocation, and produces rebalance recommendations.

Built around a historical Value-at-Risk engine with plans to extend to parametric and Monte Carlo methods. Notebook-driven v1 UI with a clean engine/display separation — the same engine powers notebooks, CLI reports, and future dashboards.

## Status

🚧 **Planning complete — implementation starting.** V1 vertical slice defined: portfolio risk monitoring through to rebalance decision.

## The Core Loop

```
Risk Snapshot → Change Detection → Attribution → Drift Analysis → Rebalance Recommendation → PM Decision → Outcome Tracking
```

The system doesn't just produce a VaR number. It asks: *what risk is the portfolio taking, where does it come from, what has changed, and should the PM act?*

## Design Documents

| Document | What it covers |
|---|---|
| `PLAN-v1-vertical-slice.md` | V1 scope: portfolio, decisions, artifacts, build plan |
| `TOP-DOWN-DESIGN-METHODOLOGY.md` | Process: how each vertical slice is approached (artifact-first, 7 steps) |
| `ARCHITECTURE.md` | Code structure: engine/display separation, data contracts, module design |
| `ARCHITECTURE-BOUNDARIES-AND-IOC.md` | Layer separation: protocols, dependency direction, composition root |
| `ARTIFACT-TAXONOMY.md` | Output model: 8 artifact types, composition graph, rendering is orthogonal |

## Quick Start

```python
from src.historical_var import historical_var

# Single-asset VaR (existing — being extended to portfolio-level)
result = historical_var(returns, confidence=0.95, position_value=1_000_000)
print(f"1-day 95% VaR: £{result:,.0f}")
```

## Sign Convention

Positive loss convention: VaR is reported as a positive number even though it represents a loss. The underlying return quantile is negative; we negate it.
