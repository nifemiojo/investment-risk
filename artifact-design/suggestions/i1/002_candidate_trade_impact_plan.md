# Candidate Trade Impact — Implementation Plan

## 1. Purpose

This plan defines the next vertical slice after risk-contribution drift and tolerance-band review.

The key workflow is not merely:

```text
risk-contribution drift
    ↓
directional suggestion
```

It is:

```text
risk-contribution drift
    ↓
generate one explicit fixed-weight candidate trade
    ↓
construct a hypothetical post-trade portfolio
    ↓
recalculate portfolio risk
    ↓
evaluate the before/after impact
    ↓
present evidence for human review
```

The candidate trade is valuable because it gives the system something concrete to test. The purpose of this slice is to show what happens to the portfolio under one transparent hypothetical alteration, not to solve for an optimal rebalance.

This is an implementation plan, not an implementation record.

---

## 2. Business decision

The PM has reviewed a risk-contribution drift and wants to understand:

> **What would happen to the portfolio if we moved a fixed amount of weight from the most over-budget asset to the most under-budget asset?**

The system should support that decision by:

1. identifying one donor and one receiver;
2. generating one equal-and-opposite fixed-weight candidate trade;
3. constructing a hypothetical post-trade portfolio;
4. recalculating portfolio risk using the existing risk model;
5. showing the before/after impact;
6. leaving the rebalance decision to the human.

The system does **not** decide that the trade should be executed.

---

## 3. Scope boundary

### Included

- One configured fixed weight transfer.
- One donor asset.
- One receiver asset.
- Equal-and-opposite weight changes.
- Candidate selection inside `CandidateTradeEngine`.
- Candidate generation from the reviewed risk-drift state.
- Hypothetical portfolio construction.
- Recalculation using the existing attribution workflow.
- Before/after risk-contribution comparison.
- Before/after portfolio-level evaluation.
- A new notebook: `src/notebooks/003-candidate-trade-impact.ipynb`.
- A dedicated Markdown render.
- A separate notebook cell explaining every impact measure in plain English.

### Deferred

V1 does not include:

- multiple candidate sizes;
- multiple donor–receiver pairs;
- multiple donors or receivers;
- cash-funded trades;
- sleeve-level candidates;
- solving for weights that restore target risk contributions;
- optimisation;
- transaction costs;
- liquidity;
- tax;
- turnover constraints;
- execution modelling;
- automatic trade selection;
- portfolio mutation;
- decision journalling.

The intended output is:

> **One hypothetical candidate trade and its measured portfolio impact.**

---

## 4. Relationship to existing artifacts

The existing risk-drift workflow answers:

> **Where does current risk contribution differ from the mandate?**

The tolerance-band review answers:

> **Is the measured drift sufficiently outside the configured band to warrant review, and which assets are directionally relevant?**

This new artifact answers:

> **What would happen under one specified equal-and-opposite fixed-weight transfer?**

The layers should remain distinct:

```text
current portfolio
        ↓
current risk attribution
        ↓
risk-contribution drift
        ↓
tolerance/review state
        ↓
CandidateTradeEngine
        ↓
one fixed-weight candidate trade
        ↓
hypothetical portfolio
        ↓
recalculated attribution and drift
        ↓
before/after impact evidence
        ↓
human review
```

The existing risk-drift and tolerance-band renders should not be silently expanded to contain candidate-trade impact. The new output is a separate adjacent artifact.

---

## 5. Candidate-generation rule

### 5.1 Donor and receiver roles

The candidate is an equal-and-opposite transfer between two assets:

```text
donor    → weight decreases
receiver → weight increases
```

The `CandidateTradeEngine` selects:

```text
donor:
    eligible asset with the largest positive risk-contribution drift

receiver:
    eligible asset with the most negative risk-contribution drift
```

The drift definition remains:

```text
drift = current risk contribution − target risk contribution
```

Therefore:

```text
positive drift → contribution above target → donor
negative drift → contribution below target → receiver
```

### 5.2 Eligibility

Candidate generation should run after the existing tolerance/review calculation.

For the first implementation, an asset is eligible only when it is outside the configured tolerance band in the relevant direction:

```text
positive drift outside band → eligible donor
negative drift outside band → eligible receiver
```

This prevents a small in-band deviation from independently generating a candidate trade.

The implementation should not add fallback logic for cases such as:

- no asset with positive drift outside tolerance;
- no asset with negative drift outside tolerance;
- all assets inside tolerance;
- only donors but no receivers;
- only receivers but no donors.

For these cases, the engine should return an explicit no-candidate result. The broader edge-case policy is deferred.

### 5.3 Selection rule

Selection must be deterministic and transparent.

The intended rule is:

```text
donor    = eligible asset with the largest positive drift
receiver = eligible asset with the most negative drift
```

If two assets have equal drift, use the asset identifier as a deterministic tie-breaker.

Conceptually:

```python
max(eligible_donors, key=lambda item: (item.signed_drift, item.asset))
min(eligible_receivers, key=lambda item: (item.signed_drift, item.asset))
```

The exact ordering of the tie-breaker should be fixed in tests and documented in the implementation contract.

### 5.4 Fixed transfer size

Use one explicit notebook parameter:

```python
CANDIDATE_TRANSFER_WEIGHT = 0.005
```

This means:

```text
donor:    -0.005, or -0.50 percentage points
receiver: +0.005, or +0.50 percentage points
```

The transfer size is a test input. It is not derived from the risk-contribution shortfall and does not claim to be the correct trade size.

There is no size ladder in this slice.

### 5.5 Example

Given:

| Asset | Current RC | Target RC | Drift |
|---|---:|---:|---:|
| SPY | 42% | 30% | +12 pp |
| EFA | 18% | 25% | -7 pp |
| IEF | 12% | 25% | -13 pp |
| GLD | 28% | 20% | +8 pp |

The engine selects:

```text
donor:    SPY
receiver: IEF
```

With a transfer of `0.005`:

```text
SPY proposed weight = SPY current weight − 0.005
IEF proposed weight = IEF current weight + 0.005
all other asset weights unchanged
```

The result is a hypothetical experiment:

> What would happen if we moved 50 basis points of portfolio weight from SPY to IEF?

---

## 6. Domain responsibilities

Domain objects represent proposals and measured states. They do not perform covariance or risk calculations.

### 6.1 `CandidateTrade`

`CandidateTrade` represents the proposed weight alteration.

Conceptually:

```python
@dataclass(frozen=True)
class CandidateTrade:
    donor_asset: str
    receiver_asset: str
    transfer_weight: float
```

Its semantic contract is:

```text
donor weight change    = -transfer_weight
receiver weight change = +transfer_weight
```

It may expose:

```python
candidate.weight_changes()
```

returning:

```python
{
    "SPY": -0.005,
    "IEF": +0.005,
}
```

The object should not contain:

- portfolio volatility;
- covariance;
- risk contributions;
- target capital weights;
- trade notional;
- transaction costs;
- execution information.

It is a hypothetical portfolio alteration, not an executable order.

### 6.2 Candidate-generation result

Known deferred edge cases should not require a complex exception hierarchy.

A result contract can express both normal and no-candidate states:

```python
@dataclass(frozen=True)
class CandidateTradeResult:
    candidate: CandidateTrade | None
    reason: str | None
```

Normal result:

```text
candidate = CandidateTrade(...)
reason = None
```

No-candidate result:

```text
candidate = None
reason = "No eligible donor and receiver were available."
```

The exact type can follow existing project conventions. The important design point is that no candidate is an expected, reportable V1 state rather than an unexpected failure.

### 6.3 Risk state

The impact result needs to retain the current and proposed risk states. Reuse existing domain objects where their contracts match.

A risk state conceptually contains enough evidence to support:

- portfolio volatility;
- asset-level risk contribution;
- target risk contribution;
- signed drift;
- absolute drift;
- tolerance status.

Do not duplicate the risk-contribution mathematics in the new domain model.

### 6.4 `CandidateTradeImpact`

`CandidateTradeImpact` represents the measured result of evaluating a candidate.

Conceptually:

```python
@dataclass(frozen=True)
class CandidateTradeImpact:
    candidate: CandidateTrade
    current_risk: RiskState
    proposed_risk: RiskState
    portfolio_volatility_change: float
    maximum_absolute_drift_change: float
    total_absolute_drift_change: float
    breached_asset_count_change: int
```

The exact shape should follow the existing project model. The required semantic property is that both states are preserved, not only summary changes.

The user needs to inspect what changed, not just see a single score.

---

## 7. Engine responsibilities

### 7.1 Existing engines remain owners of existing mathematics

#### `AttributionEngine`

Continues to calculate current or proposed portfolio attribution.

It remains the owner of the contribution mathematics.

#### `RiskDriftEngine`

Continues to compare calculated contribution with mandate risk budgets.

It should be reusable for both:

```text
current portfolio
proposed portfolio
```

#### Tolerance/review engine

Continues to classify drift against the configured tolerance and identify assets eligible for review.

The existing engine and type names should be preserved where possible. The new slice should compose with them rather than create parallel calculations.

### 7.2 `CandidateTradeEngine`

The new engine answers:

> **Given the reviewed drift state, what one fixed-weight candidate trade should be tested?**

Responsibilities:

1. identify eligible donors;
2. identify eligible receivers;
3. select the largest positive donor drift;
4. select the most negative receiver drift;
5. apply the one configured transfer size;
6. construct one `CandidateTrade`;
7. perform basic candidate feasibility checks;
8. return either a candidate or an explicit no-candidate result.

It should not:

- calculate covariance;
- calculate risk contribution;
- recalculate portfolio volatility;
- evaluate whether the candidate improved the portfolio;
- choose between multiple candidate sizes;
- mutate the current portfolio.

Conceptually:

```python
candidate_result = candidate_trade_engine.generate(
    reviewed_drift=reviewed_drift,
    transfer_weight=0.005,
)
```

### 7.3 Candidate impact evaluation responsibility

The impact evaluation answers:

> **What is the measured effect of this candidate under the same risk assumptions?**

This can be implemented as a new `CandidateTradeImpactEngine`, or as a clearly named method on an existing portfolio-risk workflow if that better matches the repository architecture. The responsibility must remain distinct from candidate selection.

The evaluation component should:

1. receive the current portfolio and `CandidateTrade`;
2. construct proposed weights;
3. validate the proposed portfolio;
4. calculate proposed attribution;
5. calculate proposed drift;
6. calculate proposed tolerance status;
7. compare current and proposed risk states;
8. return `CandidateTradeImpact`.

It should not:

- select the donor or receiver;
- create a new covariance implementation;
- optimise the transfer;
- approve the candidate;
- mutate the current portfolio.

The preferred conceptual split is:

```text
CandidateTradeEngine
    reviewed drift → one CandidateTrade

CandidateTradeImpactEngine
    current portfolio + CandidateTrade
        → proposed portfolio
        → proposed risk state
        → before/after impact
```

### 7.4 Dependency flow

```text
AttributionEngine
        ↑
RiskDriftEngine
        ↑
Tolerance/review state
        ↑
CandidateTradeEngine
        ↓
CandidateTrade
        ↓
CandidateTradeImpactEngine
        ↓
Proposed attribution and drift
        ↓
CandidateTradeImpact
```

The composition root should wire the same attribution and drift calculations into both the current-state and proposed-state paths.

---

## 8. Proposed portfolio construction

For a candidate:

```text
SPY → IEF
transfer = 0.005
```

The proposed weights are:

```text
SPY proposed = SPY current − 0.005
IEF proposed = IEF current + 0.005
all other assets unchanged
```

The implementation should construct a new portfolio or an immutable validated copy:

```python
proposed_portfolio = portfolio.with_weights(
    candidate.apply_to(portfolio.weights)
)
```

The current portfolio must not be mutated.

### Required V1 invariants

- original portfolio is unchanged;
- asset universe remains unchanged;
- donor and receiver are different assets;
- donor weight decreases by exactly the transfer amount;
- receiver weight increases by exactly the transfer amount;
- all other weights remain unchanged;
- proposed weights sum to one;
- donor weight does not become negative;
- transfer is equal and opposite.

These are feasibility checks, not a full constraint system.

---

## 9. Evaluation measures

The evaluation should show both the specific trade impact and the broader portfolio consequence.

### 9.1 Portfolio volatility

**Plain-English definition:**

> Portfolio volatility measures the typical scale of the portfolio’s return variation over the estimation period. The comparison shows whether the hypothetical trade increased or decreased the overall level of portfolio risk.

A lower value does not automatically mean that the risk-contribution allocation is closer to target. It answers a different question from contribution drift.

Display:

```text
current portfolio volatility
proposed portfolio volatility
absolute change
```

The unit must follow the existing project convention, such as daily volatility. Do not introduce annualisation solely for this artifact.

### 9.2 Maximum absolute risk-contribution drift

**Plain-English definition:**

> Maximum absolute risk-contribution drift is the largest distance between an asset’s current risk contribution and its target contribution, ignoring whether the difference is positive or negative. It identifies the portfolio’s largest individual risk-budget deviation.

A lower value means the largest individual deviation has become smaller.

Calculate:

```text
max(abs(asset drift))
```

Display current, proposed, and change in percentage points.

### 9.3 Total absolute risk-contribution drift

**Plain-English definition:**

> Total absolute risk-contribution drift adds together the absolute deviations for all assets. It provides a portfolio-wide measure of how far the risk-contribution profile is from the target profile.

A lower value means the combined deviations have decreased, although one asset may improve while another worsens.

Calculate:

```text
sum(abs(asset drift))
```

Display current, proposed, and change in percentage points.

### 9.4 Assets outside tolerance

**Plain-English definition:**

> Assets outside tolerance counts how many assets sit beyond the configured risk-contribution tolerance band. It shows whether the hypothetical trade changes the number of assets requiring review under the configured rule.

A lower count does not show how much each asset moved. It should be read alongside the drift measures.

Display:

```text
current count
proposed count
change
```

### 9.5 Risk-contribution change

**Plain-English definition:**

> Risk-contribution change is the proposed risk contribution minus the current risk contribution for each asset. It shows how the hypothetical trade changes the share of total portfolio risk attributed to each asset.

This measure reflects the full covariance calculation, so the impact is not limited to the donor and receiver. Every asset may change because of covariance interactions and the change in total portfolio volatility.

Calculate for each asset:

```text
proposed contribution − current contribution
```

Display in percentage points.

### 9.6 Drift change

**Plain-English definition:**

> Drift change is the proposed risk-contribution drift minus the current drift for each asset. It shows whether each asset moved closer to or further from its target contribution.

For a positive current drift:

```text
a negative change generally means improvement
```

For a negative current drift:

```text
a positive change generally means improvement
```

The sign must therefore be interpreted together with the original direction of drift.

Calculate for each asset:

```text
proposed drift − current drift
```

Display in percentage points.

### 9.7 Measure summary

The notebook should make the distinct questions explicit:

| Measure | Question answered |
|---|---|
| Portfolio volatility | Did overall portfolio risk increase or decrease? |
| Maximum absolute drift | Did the largest individual risk-budget deviation improve? |
| Total absolute drift | Did the combined deviations improve? |
| Assets outside tolerance | Did the number of review breaches change? |
| Risk-contribution change | How did each asset’s share of portfolio risk change? |
| Drift change | Did each asset move closer to or further from its target? |

### 9.8 No universal score

The artifact should not collapse these measures into one automatic candidate score.

A trade may:

- reduce overall volatility while worsening risk-budget alignment;
- improve risk-budget alignment while increasing volatility;
- improve both;
- improve neither.

The output presents evidence for human review rather than an automatic trade recommendation.

---

## 10. Fixed analytical context

For the current and proposed calculations, hold the analytical context constant:

- observation date;
- portfolio asset universe;
- asset return data;
- covariance estimation window;
- covariance estimator;
- return frequency;
- risk-contribution methodology;
- mandate risk budgets;
- tolerance-band rule.

Only the hypothetical portfolio weights should change.

Otherwise, a difference between current and proposed results could reflect changing estimation inputs rather than the candidate trade itself.

The interpretation should therefore be:

> Under the current covariance estimate and fixed evaluation assumptions, this candidate produced the following hypothetical change in risk.

It should not be phrased as:

> This trade will produce this result.

---

## 11. Visual render design

The new render should be separate from the existing risk-drift and tolerance-band renders.

### 11.1 Header

Use a minimal header identifying:

- artifact name;
- portfolio name;
- observation date.

Proposed heading:

```text
CANDIDATE TRADE IMPACT

Portfolio: 60/40 Multi-Asset
Observation date: 21 June 2025
```

Do not put the entire methodology in the header. Place interpretation and boundary text next to the relevant sections.

### 11.2 Candidate summary

```text
Candidate:
Sell SPY / Buy IEF
Weight transfer: 0.50 percentage points
```

Then render:

```text
| Field | Value |
|---|---|
| Donor | SPY |
| Receiver | IEF |
| Donor weight change | -0.50 pp |
| Receiver weight change | +0.50 pp |
| Selection rule | Largest positive drift to largest negative drift |
| Candidate status | Hypothetical |
```

Boundary note:

```text
This is a hypothetical equal-and-opposite weight transfer.
It is not an executable order or an optimised rebalance.
```

### 11.3 Portfolio-level impact

```text
| Measure | Current | Proposed | Change |
|---|---:|---:|---:|
| Portfolio volatility | 8.40% | 8.35% | -0.05 pp |
| Maximum absolute RC drift | 13.00 pp | 11.30 pp | -1.70 pp |
| Total absolute RC drift | 31.00 pp | 27.80 pp | -3.20 pp |
| Assets outside tolerance | 3 | 2 | -1 |
```

Units must be explicit:

- volatility: the project’s configured volatility unit;
- risk-contribution drift: percentage points;
- counts: integer.

### 11.4 Asset-level impact

Render all assets, not only the donor and receiver, because the hypothetical trade can affect every asset’s measured contribution.

```text
| Asset | Current RC | Proposed RC | RC change | Current drift | Proposed drift | Drift change |
|---|---:|---:|---:|---:|---:|---:|
| SPY | 42.00% | 40.10% | -1.90 pp | +12.00 pp | +10.10 pp | -1.90 pp |
| IEF | 12.00% | 13.80% | +1.80 pp | -13.00 pp | -11.20 pp | +1.80 pp |
| GLD | 28.00% | 27.40% | -0.60 pp | +8.00 pp | +7.40 pp | -0.60 pp |
| EFA | 18.00% | 18.70% | +0.70 pp | -7.00 pp | -6.30 pp | +0.70 pp |
```

Rows should retain a deterministic order. Prefer the existing current-drift ranking unless the implementation contract establishes another explicit order.

### 11.5 No-candidate render

If no candidate is generated:

```text
CANDIDATE TRADE IMPACT

No candidate trade was generated.

Reason:
No eligible donor and receiver pair was available under the configured
candidate-generation rule.

Multi-leg, cash-funded, and fallback candidate generation are deferred.
```

This is an expected V1 output state, not necessarily an error.

### 11.6 Avoid generated conclusions

Do not add automatic prose such as:

```text
Trade recommended.
```

The output should stop at the evidence and boundary:

```text
The candidate is shown for hypothetical impact assessment.
```

The human may decide to rebalance, hold, or override after considering the evidence and wider investment context.

---

## 12. New notebook

Create:

```text
src/notebooks/003-candidate-trade-impact.ipynb
```

The notebook should be an orchestration and evidence artifact. It should reuse existing analytical components rather than reimplementing risk mathematics.

### Proposed cell inventory

#### Code cell 1 — Parameters

```python
OBSERVATION_DATE = ...
PORTFOLIO_NAME = ...
ESTIMATION_WINDOW = ...
REBALANCE_TOLERANCE = 0.05
CANDIDATE_TRANSFER_WEIGHT = 0.005
```

The notebook should make the one transfer size visible and easy to change.

#### Code cell 2 — Imports and project-root setup

Use the same project-root and import conventions as `002-risk-drift.ipynb`.

#### Code cell 3 — Composition root

Wire:

```text
portfolio repository
returns provider
attribution engine
risk-drift engine
tolerance/review engine
CandidateTradeEngine
candidate impact engine
renderers
```

The composition root should preserve constructor injection and the existing project boundary conventions.

#### Code cell 4 — Calculate current risk state

Calculate:

```text
current attribution
current risk drift
current tolerance/review state
```

The notebook should reuse the existing risk-drift workflow.

#### Code cell 5 — Generate one candidate trade

Call the candidate engine:

```python
candidate_result = candidate_trade_engine.generate(
    reviewed_drift=review_state,
    transfer_weight=CANDIDATE_TRANSFER_WEIGHT,
)
```

The result should contain either one candidate or an explicit no-candidate reason.

#### Code cell 6 — Render candidate definition

Render:

```text
donor
receiver
weight changes
selection rule
candidate status
```

This makes the proposed alteration visible before its impact is calculated.

#### Code cell 7 — Evaluate candidate impact

If a candidate exists:

```python
impact = candidate_trade_impact_engine.evaluate(
    portfolio=portfolio,
    candidate=candidate_result.candidate,
)
```

This constructs the proposed portfolio and recalculates the risk state.

#### Markdown cell 8 — Plain-English impact-measure definitions

This is a required separate cell.

It must explain every displayed impact measure before the results appear:

- portfolio volatility;
- maximum absolute risk-contribution drift;
- total absolute risk-contribution drift;
- assets outside tolerance;
- risk-contribution change;
- drift change.

It should include the following distinction:

```text
These measures answer different questions. None of them alone identifies
an automatically correct trade.
```

The definitions should be written for a reader who can interpret the tables without already knowing the mathematical terminology.

The cell should explain units and signs where relevant:

- volatility uses the project’s configured volatility unit;
- contribution and drift changes are percentage-point changes;
- a negative change is not automatically good or bad without considering the asset’s original drift direction;
- fewer assets outside tolerance does not reveal the size of the remaining deviations.

This cell is part of the artifact’s communication contract, not optional commentary.

#### Code cell 9 — Render portfolio-level impact

Render:

```text
current value
proposed value
absolute change
```

for:

- portfolio volatility;
- maximum absolute drift;
- total absolute drift;
- assets outside tolerance.

#### Code cell 10 — Render asset-level impact

Render all assets with:

```text
current contribution
proposed contribution
contribution change
current drift
proposed drift
drift change
```

#### Markdown cell 11 — Methodological and workflow boundary

State:

- one fixed transfer size was tested;
- the trade is hypothetical;
- the covariance and estimation assumptions are held constant;
- the result is not an optimised rebalance;
- no execution, costs, or liquidity are modelled;
- no automatic decision is produced;
- no-candidate and fallback edge cases are intentionally limited in V1.

### Notebook ordering rationale

The order should be:

```text
calculate current state
    ↓
generate candidate
    ↓
show candidate
    ↓
calculate impact
    ↓
explain each measure in plain English
    ↓
show portfolio-level impact
    ↓
show asset-level impact
    ↓
state methodological boundary
```

The definitions appear after the calculation is available but before the reader sees the result tables. This keeps the notebook understandable without mixing explanatory prose into the render output.

---

## 13. Implementation sequence

### Phase 1 — Candidate domain contract

Define:

- `CandidateTrade`;
- donor and receiver semantics;
- transfer-weight validation;
- equal-and-opposite invariant;
- candidate result contract;
- no-candidate state.

Do not add risk calculations to the candidate domain object.

### Phase 2 — `CandidateTradeEngine`

Implement:

- eligible donor selection;
- eligible receiver selection;
- deterministic tie-breaking;
- one fixed transfer;
- basic candidate feasibility checks;
- explicit no-candidate result.

The engine selects the pair. The notebook should not contain the selection rule.

### Phase 3 — Hypothetical portfolio construction

Implement or reuse:

- immutable weight alteration;
- proposed portfolio validation;
- preservation of the original portfolio;
- weight-sum validation;
- non-negative donor validation;
- asset-universe validation.

### Phase 4 — Candidate impact engine

Implement:

- proposed attribution;
- proposed drift;
- proposed tolerance state;
- before/after portfolio metrics;
- asset-level contribution changes;
- asset-level drift changes;
- outside-tolerance count changes;
- `CandidateTradeImpact` result.

Reuse the existing attribution and risk-drift engines.

### Phase 5 — Dedicated renderer

Implement a separate renderer, conceptually:

```python
render_candidate_trade_impact_markdown(impact)
```

Keep it separate from:

```python
render_risk_drift_markdown(...)
render_rebalance_review_markdown(...)
```

The renderer should display evidence and boundaries, not an automatic recommendation.

### Phase 6 — New notebook integration

Add:

```text
003-candidate-trade-impact.ipynb
```

Reuse the current composition-root conventions and analytical engines.

Add the required plain-English definitions cell as a distinct Markdown cell before impact results.

### Phase 7 — End-to-end verification

Execute the notebook and verify:

- one candidate is generated for the worked fixture;
- donor and receiver follow the documented selection rule;
- proposed weights reconcile;
- current portfolio remains unchanged;
- proposed risk is recalculated;
- all impact measures render;
- plain-English definitions appear before the impact tables;
- no-candidate behaviour can be exercised by a focused test;
- the existing risk-drift notebook remains unchanged.

---

## 14. Tests and acceptance criteria

### 14.1 Candidate trade tests

Test that:

- the largest positive drift is selected as donor;
- the most negative drift is selected as receiver;
- donor and receiver are different assets;
- donor and receiver are selected only from eligible outside-band observations;
- transfer weight is applied equally and oppositely;
- donor weight decreases;
- receiver weight increases;
- all other weights remain unchanged;
- equal-drift ties are deterministic;
- no eligible donor produces no candidate;
- no eligible receiver produces no candidate;
- invalid or non-positive transfer size is rejected;
- donor cannot become negative;
- proposed weights sum to one;
- the current portfolio is not mutated.

### 14.2 Proposed portfolio tests

Test that:

- the proposed portfolio has the same asset universe;
- the proposed portfolio reflects exactly the candidate weight changes;
- the donor and receiver changes sum to zero;
- all unchanged assets retain their original weights;
- the original portfolio remains unchanged after construction;
- invalid proposed weights are rejected according to existing portfolio rules.

### 14.3 Impact engine tests

Test that:

- proposed attribution uses the existing attribution engine;
- proposed drift uses the existing risk-drift engine;
- proposed tolerance status uses the existing tolerance rule;
- current and proposed portfolio volatility are reported;
- current and proposed maximum absolute drift are reported;
- current and proposed total absolute drift are reported;
- current and proposed outside-tolerance counts are reported;
- asset-level contribution changes are calculated;
- asset-level drift changes are calculated;
- contribution reconciliation remains valid;
- current and proposed states use the same analytical context;
- the impact engine does not select another candidate or alter the supplied candidate.

### 14.4 Renderer tests

Verify that the output contains:

- portfolio name;
- observation date;
- donor;
- receiver;
- transfer size;
- candidate status;
- current/proposed portfolio metrics;
- change values;
- asset-level contribution comparison;
- asset-level drift comparison;
- explicit units;
- hypothetical-trade boundary;
- no automatic recommendation language.

Verify that the no-candidate render contains:

- no-candidate status;
- reason;
- deferred edge-case boundary.

Also verify that the existing risk-drift renderer is not changed to include candidate trades.

### 14.5 Notebook tests and verification

The notebook should:

- run from the project root;
- use the existing attribution implementation;
- generate one candidate for the worked fixture;
- recalculate the proposed portfolio;
- render before/after impact;
- handle no-candidate output;
- include a separate plain-English impact-measure cell;
- place that cell before the impact result tables;
- not mutate the current portfolio;
- not perform optimisation;
- not introduce multiple candidate sizes;
- not add a hidden automatic selection step beyond the documented engine rule.

---

## 15. Definition of done

The slice is complete when:

1. `CandidateTradeEngine` selects one donor and one receiver using the documented drift rule.
2. The selected candidate is one equal-and-opposite fixed-weight transfer.
3. No-candidate states are represented explicitly without adding fallback complexity.
4. A hypothetical proposed portfolio can be constructed without mutating the current portfolio.
5. Existing attribution and drift engines calculate the proposed risk state.
6. Before/after portfolio-level impact measures are available.
7. Before/after asset-level contribution and drift measures are available.
8. The new renderer presents the candidate and its impact separately from the existing risk-drift artifact.
9. `003-candidate-trade-impact.ipynb` runs end to end.
10. The notebook contains a separate plain-English cell defining every displayed impact measure.
11. The definitions explain what each measure answers, its units, and relevant sign interpretation.
12. Tests verify candidate selection, portfolio construction, impact calculation, rendering, and no-candidate behaviour.
13. The implementation does not optimise, recommend, execute, or automatically approve a trade.

---

## 16. Final design position

The agreed vertical slice is:

```text
risk contribution snapshot
        ↓
risk drift and tolerance review
        ↓
CandidateTradeEngine
    select largest positive drift donor
    select most negative drift receiver
        ↓
one equal-and-opposite fixed-weight trade
        ↓
hypothetical portfolio
        ↓
reuse attribution and drift engines
        ↓
before/after impact analysis
        ↓
plain-English explanation of impact measures
        ↓
human review
```

The key design principle is:

> **Generate one transparent candidate, then measure its consequences using the same risk model.**

The notebook should make the workflow understandable both computationally and conceptually: the reader sees the candidate, understands exactly what each impact measure means, and then sees the recalculated evidence. The result is a decision-support artifact, not an automatic rebalance engine.
