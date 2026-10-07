# Tolerance Bands and Rebalancing Trade Suggestions

## Purpose

This design extends the current risk-contribution drift artifact into the next step of the rebalancing decision workflow.

The existing artifact measures current risk contribution against the mandate's target contribution. This feature applies a simple tolerance band to that drift and identifies when the portfolio warrants a rebalance review.

The zoomed-out V1 workflow also identifies what remains before this becomes a crude but complete portfolio rebalancing system: target capital weights, candidate trade generation, an explicit PM decision, simulated post-trade risk measurement, and a decision journal.

The first version should remain deliberately crude. It should introduce the workflow, make its assumptions visible, and provide a basis for observing where the approach breaks before adding complexity.

This is a design record for the feature and its remaining V1 workflow boundary. It is not an implementation record.

---

## 1. PM decision

The PM is not deciding whether risk drift exists. The existing risk-drift artifact already answers that question.

The next decision is:

> **Has the portfolio's risk contribution drifted far enough from its mandate budget to justify reviewing a rebalance, and which assets should be considered for reducing or increasing exposure?**

The PM still decides whether to trade.

The system should support that decision by:

1. comparing current risk contribution with the mandate target;
2. applying a simple tolerance band;
3. identifying assets outside the band;
4. producing directional trade suggestions;
5. leaving trade size, execution, constraints, costs, and final approval to later workflow stages.

To complete a crude V1 rebalancing workflow, the system must subsequently:

6. identify the fixed capital allocation it is moving toward;
7. generate a simple candidate trade list;
8. record the PM's decision;
9. apply an accepted trade to a simulated portfolio;
10. measure the post-trade risk state and record the outcome.

The complete V1 workflow becomes:

```text
Current portfolio
        +
Mandate risk budgets
        +
Target capital weights
        ↓
Current risk attribution
        ↓
Risk contribution drift
        ↓
Apply tolerance bands
        ↓
Identify breached assets
        ↓
Generate directional review suggestions
        ↓
PM decision:
rebalance / hold / override
        ↓
If rebalance:
move capital weights toward fixed targets
        ↓
Candidate trade list
        ↓
Simulated post-trade portfolio
        ↓
Recalculate risk
        ↓
Record outcome
```

The current feature covers the middle of this workflow. It does not turn the system into an automatic trading engine.

---

## 2. Current starting point

The current implementation already provides, for each asset:

```text
RiskContributionDrift
    asset
    weight
    target risk contribution
    current risk contribution
    signed drift
    absolute drift
```

The current `RiskDriftEngine`:

- compares current contribution with mandate budget;
- calculates signed and absolute drift;
- ranks assets by absolute drift;
- returns evidence only.

The current renderer presents:

```text
Asset | Weight | Target risk contribution | Current risk contribution
      | Signed drift | Absolute drift
```

The notebook `src/notebooks/002-risk-drift.ipynb` currently follows:

```text
Parameters
    ↓
Dependencies and composition root
    ↓
Current attribution
    ↓
Risk contribution drift
    ↓
Markdown render
    ↓
Tolerance-band review
    ↓
Methodological boundary
```

The existing risk-drift renderer remains an evidence-only renderer. The tolerance-band review is a separate decision-support layer.

---

## 3. What the current feature covers

The current implementation covers the **risk review trigger**:

```text
Current risk contribution
        ↓
Compare with mandate risk budget
        ↓
Calculate signed drift
        ↓
Apply tolerance band
        ↓
Review rebalance if breached
```

This answers:

> **Is measured risk contribution drift sufficiently large under the configured rule to warrant PM review?**

It produces:

- asset-level inside/outside-band status;
- a portfolio-level review trigger;
- directional suggestions such as `Consider reducing` and `Consider increasing`.

It does not yet answer:

> **What exact capital trades would produce the desired portfolio?**

That requires a separate target-allocation and trade-generation layer.

---

## 4. V1 scope

### Included in the tolerance-band slice

- one simple tolerance-band configuration;
- an inside/outside-band classification;
- an overall rebalance-review trigger;
- directional suggestions for breached assets;
- a dedicated Markdown presentation;
- notebook integration after the existing risk-drift calculation.

### Included in the eventual crude complete V1 workflow

- fixed explicit target capital weights;
- simple long-only candidate trade sizing toward those weights;
- an explicit PM decision of rebalance or hold;
- simulated application of accepted trades;
- before/after risk comparison;
- a basic decision journal over repeated review dates.

### Excluded

V1 should not add:

- optimisation;
- solving for weights that exactly restore risk contributions;
- marginal VaR trade sizing;
- transaction-cost optimisation;
- liquidity modelling;
- tax considerations;
- turnover limits;
- cash-flow-aware rebalancing;
- execution scheduling;
- order-book or fill simulation;
- automatic portfolio mutation;
- a mandatory trading decision.

The output is a **candidate trade suggestion**, not an executable order.

---

## 5. Tolerance-band design

### Proposed first version

Use a symmetric absolute tolerance band around each asset's target risk contribution.

For each asset:

```text
lower bound = target contribution − tolerance
upper bound = target contribution + tolerance
```

For example, with a tolerance of five percentage points:

| Target contribution | Lower bound | Upper bound |
|---:|---:|---:|
| 45% | 40% | 50% |
| 20% | 15% | 25% |
| 15% | 10% | 20% |

An asset is outside tolerance when:

```text
current contribution < lower bound
or
current contribution > upper bound
```

Equivalently:

```text
abs(signed drift) > tolerance
```

The boundary is inclusive:

```text
abs(signed drift) <= tolerance
```

means that the asset is within tolerance.

### Why use percentage points?

The current risk-drift artifact already expresses drift as percentage points. A tolerance of `0.05` means five percentage points, not five percent relative change.

```text
target: 45%
current: 52%
drift: +7 percentage points
tolerance: ±5 percentage points
result: outside tolerance
```

Relative bands are deferred. They would make small targets behave differently from large targets and add another interpretation layer before the basic workflow has been tested.

### Parameter choice

The implementation should make the tolerance configurable:

```python
tolerance = 0.05
```

The initial notebook example can use:

```text
±5 percentage points
```

This is a deliberately crude starting parameter, not a validated investment-policy threshold. The system should not describe it as optimal, statistically significant, or economically justified.

The first purpose is to make the tolerance concept visible and testable.

---

## 6. Decision output

The tolerance calculation should produce two related outputs.

### Asset-level status

Each asset should receive:

```text
WITHIN TOLERANCE
or
OUTSIDE TOLERANCE
```

The result should retain:

- target risk contribution;
- current risk contribution;
- signed drift;
- absolute drift;
- lower bound;
- upper bound;
- status.

### Portfolio-level trigger

The portfolio-level result should indicate whether at least one asset is outside tolerance:

```text
REVIEW REBALANCE
```

or:

```text
WITHIN TOLERANCE
```

The wording should be weaker than `REBALANCE` because the system has not considered:

- transaction costs;
- investment views;
- liquidity;
- tax;
- implementation constraints;
- whether the drift is temporary;
- whether the mandate itself should change.

The trigger means:

> The portfolio's measured risk-contribution drift is sufficiently large under the configured rule to warrant PM review.

It does not mean:

> A trade must be executed.

---

## 7. Directional trade suggestions

For assets outside the tolerance band, generate a simple directional suggestion from the sign of drift.

| Drift condition | Suggestion |
|---|---|
| Current contribution above upper band | Consider reducing exposure |
| Current contribution below lower band | Consider increasing exposure |
| Current contribution within band | No risk-drift trade suggestion |

Example:

| Asset | Target | Current | Drift | Status | Direction |
|---|---:|---:|---:|---|---|
| SPY | 45% | 67% | +22 pp | Outside tolerance | Consider reducing |
| IEF | 20% | 10% | −10 pp | Outside tolerance | Consider increasing |
| GLD | 15% | 7% | −8 pp | Outside tolerance | Consider increasing |
| EFA | 20% | 16% | −4 pp | Within tolerance | No suggestion |

The phrase **“consider reducing”** is preferable to **“sell”** in V1 because risk contribution does not translate directly into a trade quantity.

### Important limitation

A risk contribution is not a position size.

The system cannot safely infer:

```text
SPY is 22 percentage points over budget
therefore sell £X of SPY
```

without modelling how a change in position affects:

- portfolio volatility;
- covariance interaction;
- the risk contribution of other assets;
- the resulting total portfolio risk.

Therefore, the tolerance-band layer produces **directional candidate trade suggestions only**.

---

## 8. Target capital weights are a separate input

To generate simple candidate trades, the system needs a target capital allocation in addition to target risk contributions.

For example:

```text
Target capital weights

SPY: 40%
EFA: 20%
IEF: 25%
GLD: 15%
```

The system currently knows:

```text
Current capital weights
Target risk contributions
```

A simple trade generator also needs:

```text
Target capital weights
```

These concepts must remain distinct:

| Input | Question answered |
|---|---|
| Current weights | What do we own now? |
| Target risk contributions | How should portfolio risk be allocated? |
| Target capital weights | What simple capital portfolio are we moving toward? |

For crude V1, do not solve for the capital weights that exactly restore target risk contributions. That would be a portfolio-construction problem requiring iterative risk calculations, constraints, and potentially optimisation.

Instead:

- use risk contribution drift to trigger review;
- use fixed explicit capital weights to generate a simple candidate rebalance.

This makes the separation transparent rather than implying that risk drift uniquely determines trade size.

---

## 9. Candidate capital trade generation

After the PM accepts a rebalance review, the simple candidate trade layer can calculate:

```text
target value = target weight × NAV
trade value = target value − current value
```

For a long-only portfolio:

```text
trade value < 0 → sell
trade value > 0 → buy
trade value = 0 → hold
```

Example:

| Asset | Current weight | Target weight | Current value | Target value | Candidate trade |
|---|---:|---:|---:|---:|---:|
| SPY | 40% | 35% | £400k | £350k | Sell £50k |
| EFA | 20% | 20% | £200k | £200k | Hold |
| IEF | 25% | 30% | £250k | £300k | Buy £50k |
| GLD | 15% | 15% | £150k | £150k | Hold |

The candidate trade object should conceptually contain:

```text
CandidateTrade
    asset
    current_weight
    target_weight
    current_value
    target_value
    direction
    trade_value
```

The output should be labelled:

```text
Candidate capital rebalance
```

not:

```text
Recommended orders
```

The trade list is a transparent mechanical proposal. It does not yet account for costs, liquidity, investment conviction, taxes, or alternatives.

---

## 10. PM decision capture

The system should separate the system trigger from the human decision.

```text
System output:
    REVIEW REBALANCE

PM decision:
    REBALANCE / HOLD / OVERRIDE
```

For the first version, this can be represented in the notebook or a decision-record artifact rather than a user interface:

```python
PM_DECISION = "rebalance"
PM_RATIONALE = "Risk contribution drift breached tolerance band."
```

The decision record should retain:

- review date;
- portfolio name;
- system trigger;
- configured tolerance;
- PM decision;
- rationale;
- candidate trades considered;
- whether candidate trades were applied in the simulation.

A PM may reasonably choose `HOLD` even when the system says `REVIEW REBALANCE`, for example because the drift is believed to be temporary or the investment view supports accepting it.

The system should not overwrite the PM decision with its own interpretation.

---

## 11. Simulated post-trade portfolio and risk impact

To complete the crude workflow, an accepted candidate rebalance should produce a simulated post-trade portfolio:

```text
current portfolio
    +
accepted candidate trades
    ↓
post-trade portfolio
```

V1 does not need to model:

- partial fills;
- market impact;
- settlement;
- intraday execution;
- order-book depth.

It only needs to answer:

> If the PM accepts this simple rebalance, what portfolio would result?

The risk attribution workflow can then be run on the post-trade portfolio to create a before/after comparison:

| Measure | Before | Proposed after | Change |
|---|---:|---:|---:|
| Portfolio volatility | ... | ... | ... |
| SPY risk contribution | ... | ... | ... |
| IEF risk contribution | ... | ... | ... |
| Number of breached assets | ... | ... | ... |

This tests whether the simple capital rebalance moved risk in the intended direction. It may not restore risk targets exactly; that result is itself useful evidence about the limitation of sizing trades by capital weights.

---

## 12. Historical decision loop

The final part of the crude system is operating it repeatedly through a historical period.

```text
Review date
    ↓
Measure current portfolio risk
    ↓
Check tolerance
    ↓
PM accepts or rejects candidate rebalance
    ↓
Apply accepted decision in simulation
    ↓
Move to next review date
    ↓
Measure:
    - did drift reduce?
    - did volatility change?
    - did the portfolio remain inside tolerance?
    - what happened to performance?
```

The initial decision journal can be simple:

| Review date | Trigger | PM decision | Candidate action | Post-trade drift | Outcome |
|---|---|---|---|---|---|
| Jan 2021 | No | Hold | None | ... | ... |
| Feb 2021 | Yes | Rebalance | Sell SPY, buy IEF | ... | ... |
| Mar 2021 | No | Hold | None | ... | ... |

This is the artifact that validates the workflow through a market period. It demonstrates not only that the system can calculate risk, but that the builder operated the system, made explicit decisions, and measured the consequences.

---

## 13. Visual design

### Tolerance-band review render

The rendered notebook output should let the PM answer, in order:

1. What portfolio and date am I looking at?
2. What tolerance rule is being applied?
3. Has the rule triggered a review?
4. Which assets caused the trigger?
5. What directional suggestions follow?
6. What does the system explicitly not decide?

```text
RISK DRIFT — REBALANCE REVIEW

60/40 Multi-Asset
As of 21 June 2025

Tolerance band: ±5.00 percentage points

REVIEW REBALANCE

| Asset | Target | Current | Drift | Band | Status | Suggested direction |
|---|---:|---:|---:|---:|---|---|
| SPY | 45% | 67% | +22.00 pp | ±5.00 pp | Outside | Consider reducing |
| IEF | 20% | 10% | -10.00 pp | ±5.00 pp | Outside | Consider increasing |
| GLD | 15% | 7% | -8.00 pp | ±5.00 pp | Outside | Consider increasing |
| EFA | 20% | 16% | -4.00 pp | ±5.00 pp | Within | No suggestion |

The trigger identifies risk-contribution drift outside the configured tolerance
band. It does not determine trade size, execution, cost, liquidity, or whether
the PM should rebalance.
```

### Candidate trade render

A later adjacent render should show the mechanical capital proposal separately:

```text
CANDIDATE CAPITAL REBALANCE

| Asset | Current weight | Target weight | Trade direction | Trade value |
|---|---:|---:|---|---:|
| SPY | 40% | 35% | Sell | £50,000 |
| IEF | 25% | 30% | Buy | £50,000 |
```

This should not be merged into the tolerance-band table. The two tables answer different questions:

```text
Tolerance table:
    Is the risk state sufficiently outside target to review?

Candidate trade table:
    What simple capital moves would be considered if the PM accepts review?
```

### Before/after risk render

A third adjacent view should show whether the candidate portfolio changes the measured risk state:

```text
POST-TRADE RISK IMPACT

| Measure | Current | Proposed after | Change |
|---|---:|---:|---:|
| Portfolio volatility | ... | ... | ... |
| SPY risk contribution | ... | ... | ... |
| IEF risk contribution | ... | ... | ... |
| Breached assets | ... | ... | ... |
```

Rendering remains orthogonal to the analytical artifacts. The notebook can compose these views without making them one domain contract.

### Existing renderer or new renderer?

Preserve:

```python
render_risk_drift_markdown(risk_drift)
```

Add separate renderers for the separate questions:

```python
render_rebalance_review_markdown(rebalance_trigger)
render_candidate_trades_markdown(candidate_trades)
render_post_trade_risk_markdown(before_after_risk)
```

The existing evidence-only renderer should not be silently changed to include workflow routing or candidate trades.

---

## 14. Notebook presentation design

The existing `src/notebooks/002-risk-drift.ipynb` is the natural location for the tolerance-band review because the feature directly follows its current output.

The immediate notebook structure is:

```text
Code cell 1 — Parameters
    DATE
    PORTFOLIO
    ESTIMATION_WINDOW
    REBALANCE_TOLERANCE

Code cell 2 — Imports and project-root setup

Code cell 3 — Composition root
    portfolio repository
    returns provider
    attribution engine
    risk-drift engine
    rebalance-trigger engine

Code cell 4 — Calculate attribution and risk drift

Code cell 5 — Render current risk-drift evidence

Code cell 6 — Apply tolerance bands

Code cell 7 — Render rebalance review and directional suggestions

Markdown cell — Methodological and workflow boundary
```

The current implementation composes the existing evidence render and the new tolerance-band review in the same notebook.

The eventual complete V1 notebook or adjacent notebook should add:

```text
Parameters
    target capital weights
    PM decision

Candidate trade calculation

Candidate trade render

Post-trade portfolio construction

Post-trade risk calculation

Before/after risk render

Decision journal append
```

The notebook remains an orchestration and evidence artifact. It should not become a full educational lesson or a simulation of order execution.

---

## 15. Domain and architecture boundary

The current `RiskDrift` object answers:

> What is the current contribution drift versus mandate?

The tolerance result answers:

> Does that drift breach the configured tolerance, and what directional review suggestion follows?

A future candidate-trade result answers:

> What simple capital trades move the portfolio toward the explicit target weights?

A future post-trade result answers:

> What risk state would result if those candidate trades were applied?

These are related but distinct questions.

Recommended separation:

```text
RiskDrift
    current drift evidence

RebalanceTrigger
    tolerance configuration
    per-asset band status
    portfolio-level trigger
    directional suggestions

CandidateTrades
    explicit target capital weights
    current values
    target values
    trade directions
    trade values

PostTradeRisk
    current risk state
    proposed post-trade risk state
    before/after differences

DecisionRecord
    system trigger
    PM decision
    rationale
    candidate action
    outcome
```

Recommended responsibility boundaries:

```text
RiskDriftEngine
    calculates current drift

RebalanceTriggerEngine
    applies tolerance policy

CandidateTradeEngine
    converts current and target capital weights into simple trade values

PortfolioSimulationEngine
    applies accepted candidate trades in a controlled simulation

PostTradeRiskEngine
    recalculates risk on the proposed portfolio

DecisionJournal
    records the PM decision and observed outcome
```

The candidate trade engine should not recalculate covariance or risk contribution. The post-trade risk engine should reuse the existing attribution workflow rather than duplicate its mathematics.

---

## 16. Implementation sequence

### Phase 1 — Tolerance decision contract

Completed by this slice:

- tolerance is expressed as an absolute proportion;
- `0.05` means five percentage points;
- the band is symmetric around target;
- equality with the band boundary is within tolerance;
- the portfolio trigger is true if any asset breaches;
- positive drift implies consider reducing;
- negative drift implies consider increasing.

### Phase 2 — Tolerance domain result and engine

Completed by this slice:

- immutable tolerance-band observations;
- asset status;
- directional suggestion;
- portfolio-level trigger;
- negative tolerance validation;
- deterministic preservation of risk-drift ordering.

### Phase 3 — Dedicated Markdown render

Completed by this slice:

- explicit tolerance display;
- prominent review status;
- status and directional suggestion columns;
- boundary note;
- no notional trade amount or execution language.

### Phase 4 — Notebook integration

Completed by this slice:

- visible tolerance parameter;
- trigger-engine wiring;
- existing risk-drift render preserved;
- new tolerance-band review rendered beside it.

### Phase 5 — Fixed target capital weights

Next slice:

- add explicit capital targets to the portfolio or mandate boundary;
- keep risk budgets and capital weights as distinct inputs;
- validate that capital target weights form a valid long-only allocation;
- render the target allocation as input evidence.

### Phase 6 — Candidate capital trades

Next slice:

- calculate target value from target weight and NAV;
- calculate trade value from target value minus current value;
- derive buy, sell, or hold direction;
- render candidate trades separately from risk drift;
- do not model costs, liquidity, or execution yet.

### Phase 7 — PM decision and simulated application

Next slice:

- represent `REBALANCE`, `HOLD`, and `OVERRIDE`;
- capture a rationale;
- apply only an accepted rebalance to a simulated portfolio;
- keep system trigger and human decision separate.

### Phase 8 — Post-trade risk impact

Next slice:

- rerun attribution on the proposed portfolio;
- compare current and proposed risk contribution;
- compare portfolio volatility;
- count assets outside tolerance before and after;
- show whether the simple capital rebalance moved risk in the intended direction.

### Phase 9 — Historical decision loop

Capstone V1 slice:

- choose fixed historical review dates;
- run the workflow repeatedly;
- record the PM decision at each review;
- apply accepted trades in simulation;
- measure subsequent drift, risk, and performance;
- produce a decision journal and lessons about where the crude process breaks.

---

## 17. Tests and acceptance criteria

### Tolerance domain and engine tests

Test that:

- assets exactly on the band boundary are within tolerance;
- assets just outside the band are flagged;
- positive drift produces a reduction suggestion;
- negative drift produces an increase suggestion;
- zero drift produces no suggestion;
- all assets within tolerance produce no portfolio trigger;
- one breached asset produces a portfolio trigger;
- results retain deterministic ordering;
- tolerance cannot be negative;
- attribution/mandate asset mismatch remains rejected by the existing workflow.

### Tolerance renderer tests

Test that the rendered output contains:

- portfolio name;
- formatted date;
- tolerance value;
- portfolio-level trigger;
- asset status;
- directional suggestion;
- signed drift in percentage points;
- no notional trade amount;
- no language implying execution;
- methodological boundary.

Also verify that the existing evidence-only renderer still does not contain:

```text
REBALANCE
trade
suggested direction
```

unless the existing renderer is intentionally changed later.

### Candidate trade tests

When implemented, test that:

- target values equal target weights multiplied by NAV;
- positive trade value means buy;
- negative trade value means sell;
- zero trade value means hold;
- candidate trades reconcile to the change in portfolio value;
- current and target asset universes must match;
- target capital weights satisfy the chosen long-only invariants.

### Post-trade tests

When implemented, test that:

- accepted trades produce the expected post-trade weights;
- rejected or held decisions do not mutate the simulated portfolio;
- post-trade attribution uses the existing attribution calculation;
- before/after portfolio volatility is reported consistently;
- before/after risk contribution rows reconcile to the respective portfolio totals.

### Decision-journal tests

When implemented, test that:

- every review has a date and system trigger;
- every accepted decision has a candidate action or explicit no-trade rationale;
- held or overridden decisions retain the PM rationale;
- post-trade outcome fields remain distinguishable from the original trigger evidence.

### Notebook validation

Execute the notebook and verify that:

- it runs from the project root;
- attribution and drift calculation still succeed;
- both Markdown outputs render;
- the trigger result matches the fixture expectations;
- the notebook does not generate executable orders or quantities in the tolerance-only slice.

---

## 18. Known limitations

This V1 deliberately leaves several distinctions unresolved:

1. **Risk drift versus desired trade** — a risk-contribution breach does not uniquely determine a trade.
2. **Risk target versus capital target** — fixed capital targets are a crude proxy for restoring a desired risk state.
3. **Temporary risk change versus persistent drift** — one observation may be noisy or regime-dependent.
4. **Risk-budget restoration versus investment view** — the PM may intentionally accept drift.
5. **Directional suggestion versus trade quantity** — the tolerance layer does not know how much to buy or sell.
6. **Candidate trade versus executable order** — no execution, costs, liquidity, or fill modelling exists.
7. **Asset-level budget versus sleeve-level policy** — the current mandate remains individual-asset based.
8. **Threshold trigger versus economic benefit** — no transaction-cost or implementation-benefit calculation exists.
9. **Immediate post-trade improvement versus investment outcome** — a risk state can improve while returns or longer-term outcomes do not.

These limitations are not defects in the first version. They are reasons to keep the workflow simple and observe where it breaks.

---

## 19. Iteration path

Only add complexity when operating the first version exposes a concrete weakness.

```text
V1a
simple ±5 pp risk-contribution band
directional review suggestions
no sizing

V1b
fixed target capital weights
simple candidate buy/sell values

V1c
PM decision capture
simulated post-trade portfolio

V1d
before/after risk impact
historical decision journal

V2
trade sizing using marginal/component risk

V3
transaction costs and minimum trade sizes

V4
persistence requirement
for example, breach across multiple observations

V5
different tolerances by asset or sleeve

V6
portfolio-level netting and constrained trade proposals

V7
decision journal with richer post-rebalance outcome analysis
```

The immediate completed feature stops at:

> **A transparent tolerance-band trigger that tells the PM which risk contributions are sufficiently outside mandate to warrant review, plus directional candidate suggestions.**

The remaining path to a crude complete V1 is:

> **Add explicit target capital weights, generate simple candidate trades, record the PM decision, simulate accepted trades, recalculate risk, and operate the loop through a historical period.**

That is the smallest useful extension from current risk measurement toward a complete portfolio rebalancing workflow.
