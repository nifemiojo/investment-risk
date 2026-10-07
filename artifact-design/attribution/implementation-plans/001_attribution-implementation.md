# Proposed implementation sketch: Attribution

## 1. Implementation approach

I recommend following the same progression as the risk snapshot:

```text
V0.1  Notebook-first
      Build the PM-facing attribution artifact with representative data.

V0.2  Engine contract
      Move the notebook's calculation behind an AttributionEngine,
      while keeping the notebook output unchanged.

V0.3  Real computation
      Replace illustrative values with covariance-based calculations
      using the existing portfolio and returns infrastructure.
```

This lets us validate the artifact and the user experience before spending time building a broader backend structure.

The notebook should remain the first consumer of the engine, not the place where the attribution logic permanently lives.

---

# 2. Proposed notebook

## File

```text
workflows/002-risk-attribution.ipynb
```

The notebook would follow the established snapshot pattern:

### Section 1 — Lesson statement

The notebook should open with the question:

> Where does the portfolio's structural volatility come from?

And establish the boundary:

> This notebook decomposes structural portfolio volatility into asset-level contributions. It does not decompose historical VaR and does not produce investment recommendations.

### Section 2 — Parameters

```python
# ⚙️ Parameters — change these and re-run

DATE = "2025-06-21"
PORTFOLIO = "60/40 Multi-Asset"
ESTIMATION_WINDOW = 252
```

The important point is that the user supplies the portfolio and date, while the engine resolves the portfolio's weights and returns internally.

### Section 3 — Composition root

Initially, this would mirror the snapshot:

```python
from src.engine.attribution_engine import AttributionEngine
from src.infrastructure.in_memory_portfolios import InMemoryPortfolioRepository
from src.infrastructure.yfinance_returns import YFinanceReturnsProvider
from src.display.attribution_renderer import render_attribution_markdown

portfolios = InMemoryPortfolioRepository()
returns_provider = YFinanceReturnsProvider()

engine = AttributionEngine(
    portfolios=portfolios,
    returns_provider=returns_provider,
)
```

The notebook should not construct covariance matrices, calculate contributions, or format tables itself.

### Section 4 — Generate attribution

```python
attribution = engine.attribute(
    portfolio_name=PORTFOLIO,
    date=DATE,
    estimation_window=ESTIMATION_WINDOW,
)
```

### Section 5 — Render the artifact

```python
display(Markdown(render_attribution_markdown(
    attribution,
    portfolio_name=PORTFOLIO,
    date=DATE,
)))
```

### Section 6 — Reconciliation checks

The notebook should expose the important mathematical checks visibly:

```python
sum(c.risk_contribution_pct for c in attribution.risk_contributions)
```

The expected result is approximately:

```text
1.0
```

The notebook can also show:

- the cumulative contribution column reaching ~100% on the final row;
- positive and negative contributors;
- the effect of ranking.

These should be presented as evidence and validation, not translated into generated commentary.

---

# 3. Proposed backend structure

I would add the attribution implementation alongside the existing snapshot structure:

```text
src/
├── domain/
│   ├── portfolio.py
│   └── attribution.py
│
├── boundaries/
│   ├── portfolio_repository.py
│   └── returns_provider.py
│
├── engine/
│   ├── risk_snapshot_engine.py
│   └── attribution_engine.py
│
├── infrastructure/
│   ├── in_memory_portfolios.py
│   └── yfinance_returns.py
│
└── display/
    ├── snapshot_renderer.py
    └── attribution_renderer.py
```

The attribution implementation should reuse the existing portfolio and returns boundaries rather than introducing separate data-access logic.

---

# 4. Domain output model

The central output should be an immutable evidence object.

Something conceptually like:

```python
@dataclass(frozen=True)
class Attribution:
    portfolio_volatility: float
    risk_contributions: tuple[RiskContribution, ...]
```

The object holds only what the engine *computed*. The caller's own inputs —
`portfolio_name`, `date`, and `estimation_window` — are not echoed back. The
renderer receives them directly and owns their presentation (formatting the
date, headings, and any window reference).

This convention is new to Attribution. The existing `RiskSnapshot` still echoes
`timestamp` and `portfolio_name`; it is intentionally left unchanged.

Each ranked asset would be represented by a separate immutable object:

```python
@dataclass(frozen=True)
class RiskContribution:
    asset: str
    weight: float
    risk_contribution_pct: float
    cumulative_risk_contribution_pct: float
```

The exact field names should be reviewed before implementation, but the important design is that the object contains evidence rather than interpretation.

## Fields included

### Portfolio-level

- portfolio volatility.

### Asset-level

- asset identifier;
- portfolio weight;
- percentage contribution;
- cumulative contribution percentage.

Components are ranked by `risk_contribution_pct` descending; rank is expressed by the
ordering itself, not stored as a field.

I would avoid storing separate fields such as:

```python
focus
observations
next_investigation
decision
interpretation
```

Those are explicitly outside Attribution v1.

---

# 5. Calculation model

The calculation is based on the covariance matrix of asset returns.

Let:

- $w_i$ be the portfolio weight of asset $i$;
- $\Sigma$ be the covariance matrix of asset returns;
- $\sigma_p$ be portfolio volatility;
- $\operatorname{Cov}(r_i, r_p)$ be the covariance between asset $i$ and the portfolio.

Portfolio volatility is:

$$
\sigma_p = \sqrt{w^\top \Sigma w}
$$

Here:

- $w$ is the vector of portfolio weights;
- $\Sigma$ contains the covariance between every pair of assets;
- $w^\top \Sigma w$ is portfolio variance;
- the square root converts variance into volatility.

The covariance of each asset with the portfolio is:

$$
\operatorname{Cov}(r_i, r_p) = (\Sigma w)_i
$$

The component contribution to volatility is:

$$
C_i =
\frac{w_i \operatorname{Cov}(r_i, r_p)}
{\sigma_p}
$$

The contributions should reconcile to the total portfolio volatility:

$$
\sum_i C_i = \sigma_p
$$

The percentage contribution is:

$$
P_i =
\frac{C_i}{\sigma_p}
=
\frac{w_i \operatorname{Cov}(r_i, r_p)}
{\sigma_p^2}
$$

The percentages should reconcile to 100%:

$$
\sum_i P_i = 1
$$

In code, the core calculation should remain small and pure:

```python
covariance_matrix = returns.cov()
portfolio_volatility = np.sqrt(
    weights @ covariance_matrix @ weights
)

covariance_with_portfolio = covariance_matrix @ weights

risk_contribution = (
    weights
    * covariance_with_portfolio
    / portfolio_volatility
)

risk_contribution_pct = (
    risk_contribution
    / portfolio_volatility
)
```

`covariance_with_portfolio` and `risk_contribution` (volatility units) above are
computation *intermediates*. They are required to derive `risk_contribution_pct`,
but they are **not returned** in the output object. Only `portfolio_volatility`
and the per-asset `risk_contribution_pct` (plus the cumulative running total)
leave the calculation layer.

The calculation module should accept returns and weights. It should not know about:

- tickers;
- yfinance;
- portfolios by name;
- notebook display;
- markdown;
- PM interpretation.

---

# 6. Proposed engine API

The engine should expose a user-facing method that reflects how a PM thinks:

```python
attribution = engine.attribute(
    portfolio_name="60/40 Multi-Asset",
    date="2025-06-21",
    estimation_window=252,
)
```

The caller should not need to supply:

```python
weights
returns
covariance_matrix
portfolio_volatility
```

Those are internal dependencies that the engine can resolve.

Conceptually:

```python
class AttributionEngine:
    def __init__(
        self,
        portfolios: PortfolioRepository,
        returns_provider: ReturnsProvider,
    ):
        self._portfolios = portfolios
        self._returns_provider = returns_provider

    def attribute(
        self,
        portfolio_name: str,
        date: str,
        estimation_window: int,
    ) -> Attribution:
        ...
```

The engine would:

1. retrieve the portfolio;
2. obtain the asset weights;
3. obtain the historical returns required for the estimation window;
4. align the returns with the portfolio assets;
5. calculate the covariance matrix;
6. calculate portfolio volatility;
7. calculate each asset's contribution;
8. rank assets by contribution;
9. calculate cumulative contribution;
10. return the immutable domain object.

The engine would not render markdown or generate observations.

---

# 7. Boundary protocols

The engine should depend on abstractions rather than concrete infrastructure.

For example:

```python
class PortfolioRepository(Protocol):
    def get(self, portfolio_name: str) -> Portfolio:
        ...
```

```python
class ReturnsProvider(Protocol):
    def get_returns(
        self,
        assets: tuple[str, ...],
        end_date: str,
        window: int,
    ) -> pd.DataFrame:
        ...
```

The concrete implementations would remain in infrastructure:

```python
InMemoryPortfolioRepository
YFinanceReturnsProvider
```

This is consistent with the snapshot implementation:

```text
Notebook
   ↓
AttributionEngine
   ↓
PortfolioRepository / ReturnsProvider
   ↓
In-memory portfolio / yfinance
```

The engine should not import `yfinance` directly.

---

# 8. Ranking and cumulative contribution

The primary table should be ranked by `risk_contribution_pct`, descending.

For example:

| Asset | Weight | Risk contribution | Cumulative |
|---|---:|---:|---:|
| SPY | 40% | 62% | 62% |
| EFA | 20% | 21% | 83% |
| GLD | 15% | 18% | 101% |
| IEF | 25% | -1% | 100% |

The cumulative total temporarily exceeding 100% is not an error. Positive contributors can sum to more than 100% when a negative contribution offsets them.

That behavior is worth preserving because it makes diversification and offsetting positions visible.

I would not use absolute contribution for the primary ranking because that would hide the distinction between:

- a large positive contributor;
- a large negative contributor;
- a genuinely small contribution.

Instead:

- rank by signed percentage contribution;
- preserve the sign;
- make negative values visible in the renderer;
- calculate cumulative contribution in the displayed ranking order.

One design point to confirm is whether the table should rank strictly by signed contribution or whether negative contributors should be displayed in a separate section after positive contributors. My recommendation is to keep one signed ranked table for v1, because it directly supports the reconciliation property.

---

# 9. Renderer design

The renderer would be responsible only for arranging the evidence into the designed PM-facing artifact.

```python
def render_attribution_markdown(
    attribution: Attribution,
    *,
    portfolio_name: str,
    date: str,
) -> str:
    ...
```

The display would contain:

## Header

```text
ATTRIBUTION
60/40 Multi-Asset
As of 21 June 2025
```

## Portfolio risk

```text
Portfolio volatility: 1.8% daily
```

## Main ranked table

```text
WHERE DOES RISK LIVE?

Asset   Weight   Risk contribution   Cumulative
SPY     40%      62%                 62%
...
```

## Boundary note

The artifact should end with:

> Component contributions describe structural portfolio volatility over the estimation window. They are not a trade recommendation and do not decompose historical VaR.

---

# 10. What belongs in the notebook versus the engine

## Notebook

The notebook owns:

- user-selected parameters;
- composition-root wiring;
- calling the engine;
- displaying the returned artifact;
- optional inspection/reconciliation cells;
- lesson-oriented markdown.

## Engine

The engine owns:

- resolving portfolio data;
- requesting returns;
- orchestrating the calculation;
- ranking;
- cumulative contribution;
- constructing the output model.

## Pure calculation module

The calculation module owns:

- covariance matrix calculation;
- portfolio volatility;
- covariance with portfolio;
- component volatility contributions;
- percentage contributions;
- reconciliation calculations.

## Renderer

The renderer owns:

- headings;
- table layout;
- percentage and volatility formatting;
- negative-value presentation;
- cumulative contribution column;
- methodological boundary note.

This keeps the notebook thin and makes the backend reusable later by a CLI, dashboard, or report generator.

---

# 11. Proposed implementation sequence

## Phase 1 — Build the notebook artifact

Use representative data first to validate:

- visual hierarchy;
- table columns;
- negative contributions;
- cumulative contributions above 100%;
- the cumulative contribution column;
- boundary note.

At this point, the notebook could construct the domain object directly or use a temporary fixture.

## Phase 2 — Define the domain contract

Extract:

- `Attribution`;
- `RiskContribution`;
- portfolio and returns protocols;
- the engine method signature.

The notebook output should remain unchanged.

## Phase 3 — Add the engine with fixture data

Wire:

```python
engine.attribute(...)
```

but initially return controlled values. This validates that the notebook is consuming an engine contract rather than depending on its implementation.

## Phase 4 — Add pure computation

Implement the covariance-based calculation and test it independently using small, deterministic return matrices.

## Phase 5 — Connect real portfolio and returns infrastructure

Reuse:

- the existing portfolio repository;
- the existing returns provider;
- the same date and asset-alignment conventions as the snapshot.

## Phase 6 — Execute the full notebook

The final verification should include:

```text
notebook executes from a clean kernel
returns are correctly aligned
portfolio volatility is positive
component contributions reconcile to portfolio volatility
percentage contributions reconcile to 100%
negative contributions remain visible
rendered output contains no interpretation or recommendation
```

---

# 12. Tests I would expect

The first implementation should have focused tests around the mathematical contract.

## Calculation tests

- one-asset portfolio contribution equals 100%;
- percentage contributions sum to 1;
- negative correlation can produce a negative contribution;
- zero-weight asset contributes zero;
- asset ordering does not change the final contribution assigned to each asset;
- the final cumulative contribution equals 100%.

## Ranking tests

- assets are ordered by signed contribution;
- cumulative contributions follow displayed order;
- cumulative contribution can exceed 100% before returning to 100%;
- negative contributors are retained.

## Engine tests

Using fake repository/provider implementations:

- portfolio name is resolved through the repository;
- returns are requested for the portfolio assets;
- the estimation window is passed to the returns provider;
- the engine returns an `Attribution` object;
- no infrastructure dependency leaks into the pure calculation layer.

## Renderer tests

- the portfolio name and date appear;
- the main ranked table appears;
- weights and contribution percentages appear;
- the cumulative contribution column appears;
- negative contributions are rendered visibly;
- the methodological boundary note appears;
- no standalone-volatility column appears;
- no top-1/2/3 concentration summary appears;
- no generated `focus`, `decision`, or recommendation text appears.

---

# 13. Decisions I would like to preserve before implementation

My recommendation is:

1. **Use daily structural volatility**, not historical VaR, for Attribution v1.
2. **Use the same estimation window as the design specifies**, initially 252 observations.
3. **Rank by signed percentage contribution**, retaining negative contributors in the same table.
4. **Return only the ranked percentage contribution, weight, and cumulative contribution.** Standalone volatility and the volatility-unit contribution are computation internals, not output.
5. **Express concentration through the cumulative contribution column**, not a top-1/2/3 summary and not a concentrated/diversified verdict.
6. **Keep the artifact evidence-only**, with no interpretation or workflow routing.
7. **Reuse the snapshot’s repositories and data providers**, rather than creating attribution-specific infrastructure.
8. **Build the notebook display before implementing the full engine**, so the API is shaped by the artifact the user actually consumes.

The resulting implementation would be deliberately small:

```text
notebook
   ↓
renderer
   ↓
Attribution domain object
   ↑
Attribution engine
   ↓
pure component-contribution calculation
   ↓
portfolio and returns protocols
   ↓
existing infrastructure adapters
```

That gives us a thin, inspectable vertical slice without prematurely turning Attribution into a general-purpose risk platform.
