## V1 decision

The portfolio has a **mandate**, and the mandate explicitly defines the intended risk budget for each asset.

```text
Portfolio
    └── has a read-only Mandate
            └── defines asset-level target risk contributions
```

For the current portfolio, the mandate might contain:

```text
SPY: 45%
EFA: 20%
IEF: 20%
GLD: 15%
```

These are not calculated by the risk model. They are policy inputs supplied by the mandate.

The risk model calculates only the current observed contribution:

```text
current portfolio
    +
current covariance estimate
        ↓
current risk contribution
```

Then the drift calculation compares the two:

```text
drift_i = current_risk_contribution_i - mandate_target_risk_contribution_i
```

This is a good separation of responsibilities:

| Object | Responsibility |
|---|---|
| `Mandate` | Defines the intended risk budget |
| `Portfolio` | Owns the mandate and current portfolio definition |
| `AttributionEngine` | Measures current structural risk contribution |
| `RiskDriftEngine` | Compares current contribution with the mandate |
| Future portfolio-construction model | May eventually generate the mandate or target, but is out of scope for V1 |

## Domain-modelling implication

The mandate should be immutable after construction.

Conceptually:

```python
@dataclass(frozen=True)
class Mandate:
    risk_budget_by_asset: Mapping[str, float]
```

And:

```python
@dataclass(frozen=True)
class Portfolio:
    name: str
    assets: Mapping[str, float]
    nav: float
    mandate: Mandate
```

The important point is that the risk drift workflow reads the mandate; it does not modify or infer it.

I would keep the word **budget** in the domain model because it communicates that these are policy allocations of a finite risk resource:

```python
mandate.risk_budget_by_asset
```

rather than something like:

```python
portfolio.target_risk_contributions
```

The latter makes it sound as if the target belongs to the calculation rather than to the portfolio’s investment policy.

## Validation rules for the mandate

Even in V1, the mandate should enforce a few invariants at construction:

1. Every risk-budget value is non-negative.
2. The risk budgets sum to 100%, within a defined tolerance.
3. The budget assets are valid members of the portfolio universe.
4. There are no duplicate asset identifiers.
5. The mandate is immutable after construction.

The first rule is important because the mandate expresses a budget. Current realised contribution can be negative for a diversifying asset, but a policy risk budget probably should not be negative unless we deliberately introduce hedge budgets later.

The target values should therefore be treated as:

```text
policy risk budgets
```

not as expected realised contributions that must always be reproduced by the covariance model.

## Notebook

The next notebook should be something like:

```text
src/notebooks/002-risk-drift.ipynb
```

or, if the project uses descriptive names rather than sequence numbers:

```text
src/notebooks/risk-drift.ipynb
```

Given the existing `001-risk-attribution.ipynb` convention, I would use:

```text
src/notebooks/002-risk-drift.ipynb
```

The notebook should reuse the attribution workflow rather than recomputing contribution mathematics independently.

Its structure can stay very small:

```text
Parameters
    ↓
Dependencies and composition root
    ↓
Calculate current attribution
    ↓
Calculate risk contribution drift
    ↓
Render minimal drift artifact
    ↓
Methodological boundary
```

The notebook should not yet:

- calculate target weights;
- derive risk budgets from covariance;
- optimise weights;
- produce trades;
- decide whether a rebalance should occur;
- determine whether asset-level or sleeve-level budgets are economically correct.

## V1 visual

Yes, sorting by **absolute drift descending** is the right choice.

The artifact is intended to help identify where the risk profile differs most from the mandate. Absolute drift gives the priority ranking, while signed drift retains direction.

```text
RISK CONTRIBUTION DRIFT

Portfolio: 60/40 Multi-Asset
Observation date: 2021-02-21

Asset | Target risk | Current risk | Signed drift | Absolute drift
SPY  |       45.0% |       67.0% |     +22.0 pp |        22.0 pp
IEF  |       20.0% |       10.0% |     -10.0 pp |        10.0 pp
GLD  |       15.0% |        7.0% |      -8.0 pp |         8.0 pp
EFA  |       20.0% |       16.0% |       -4.0 pp |         4.0 pp
```

The ordering should be:

```python
sorted(
    contributions,
    key=lambda contribution: (
        -abs(contribution.signed_drift),
        contribution.asset,
    ),
)
```

The asset-name tie-breaker gives deterministic output when two assets have equal absolute drift.

I would avoid sorting by signed drift because that would put positive and negative deviations into separate directional groups. That is less useful for the initial question:

> Which assets are furthest from their mandated risk budgets?

## Open question to preserve explicitly

The unresolved future question is now narrower and better defined:

> At what abstraction level should a mandate specify risk budgets, and how should those budgets be determined?

Potential future levels include:

```text
Portfolio
    ├── asset class / sleeve risk budgets
    │     ├── equities
    │     ├── rates
    │     └── commodities
    │
    └── individual-asset risk budgets
          ├── SPY
          ├── EFA
          ├── IEF
          └── GLD
```

And potential future sources include:

- explicit investment-policy targets;
- strategic allocation translated through a reference risk model;
- risk-parity or other portfolio-construction objectives;
- an optimiser using expected returns, covariance, constraints, and costs;
- hierarchical budgets: sleeve-level first, asset-level second.

For V1, I would record that the system intentionally chooses:

```text
mandate risk budget level = individual asset
target source = explicit policy input
target-generation model = deferred
```

That makes the limitation deliberate rather than accidental.

The overall design now becomes:

```text
Portfolio
    └── Mandate
          └── explicit asset-level risk budgets
                         ↓
Current portfolio attribution
                         ↓
Compare current risk contribution to mandate budget
                         ↓
Sort by absolute drift
                         ↓
Present evidence only
```

This is a strong next slice because it introduces the first genuinely normative object—the mandate—without prematurely building a portfolio-construction model or an automatic rebalancing decision.
