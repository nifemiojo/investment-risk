# Candidate Trade Generation Approaches

Yes — there is a wide design space between:

1. **“Asset A is above its risk budget, so sell it”**, and  
2. **“Solve for the portfolio weights that restore every target contribution.”**

The important distinction is that **candidate-trade generation does not necessarily need to become full portfolio construction**. We can make it progressively more sophisticated while keeping the output explicitly as *proposals*, not an optimal rebalance.

## First, separate three questions

The system should avoid conflating:

1. **Which assets are misaligned?**
2. **What direction would probably reduce the misalignment?**
3. **How large should the trade be, and what should fund it?**

The first two can be addressed quite simply. The third is where the problem starts becoming portfolio construction.

---

# Approach 1: Independent directional candidates

This is the simplest possible version.

For every asset:

```text
risk contribution > target + tolerance
    → candidate action: reduce / sell

risk contribution < target - tolerance
    → candidate action: add / buy

inside tolerance
    → no candidate
```

The candidate list might look like:

| Asset | Current RC | Target RC | Drift | Suggested direction | Priority |
|---|---:|---:|---:|---|---:|
| SPY | 42% | 30% | +12% | Reduce | High |
| EFA | 18% | 25% | -7% | Add | Medium |
| IEF | 12% | 25% | -13% | Add | High |
| GLD | 28% | 20% | +8% | Reduce | Medium |

This does not answer:

- how many shares to trade;
- whether buying IEF actually reduces total portfolio risk;
- which sale should fund which purchase;
- whether the recommendation is feasible under constraints.

That is acceptable if the artifact is honestly framed as:

> **A ranked list of directional actions indicated by current risk-contribution drift.**

## Strengths

- Very easy to explain.
- Low implementation complexity.
- Keeps the distinction between monitoring and portfolio construction clear.
- Produces useful PM-facing triage.
- Does not pretend to have solved the rebalance.

## Weaknesses

- It can produce several buys and several sells without connecting them.
- It ignores trade magnitude.
- It may recommend buying an asset whose contribution is low because it is a useful diversifier, but the trade could have an unexpected impact under the covariance assumptions.
- It does not know whether the portfolio has cash available.

This is probably the cleanest starting point for the first version.

---

# Approach 2: Add fixed trade-size templates

The next step is to turn directions into executable-sized candidates without trying to solve for the required weights.

For example, each directional signal could generate a small set of standard trade sizes:

```text
SPY: reduce by 25 bp
SPY: reduce by 50 bp
SPY: reduce by 100 bp
IEF: add by 25 bp
IEF: add by 50 bp
IEF: add by 100 bp
```

Here, the system is not claiming:

> “Sell 73 basis points of SPY because that is the mathematically correct amount.”

It is saying:

> “These are standard-sized candidate actions for the user to evaluate.”

The size ladder could be configured by the portfolio:

```text
small: 25 bp
medium: 50 bp
large: 100 bp
```

Or expressed as relative changes:

```text
reduce position by 5%
reduce position by 10%
reduce position by 20%
```

I would favour **portfolio-weight changes**, such as basis points, because they are easier to compare across assets and portfolios.

## Why this is useful

It makes the output more concrete while avoiding optimisation. It also creates a natural place to add scenario analysis later:

| Candidate | Action | Trade size | Expected purpose |
|---|---|---:|---|
| C01 | Sell SPY | -50 bp | Reduce excess equity risk contribution |
| C02 | Buy IEF | +50 bp | Increase under-represented defensive contribution |
| C03 | Sell GLD | -50 bp | Reduce excess GLD contribution |

At this stage, the system is still generating candidate actions, not selecting a final rebalance.

---

# Approach 3: Separate donors and receivers

If trades must be funded by other trades, independent signals are not enough.

The system can classify assets into two groups:

## Donors

Assets with contribution above target:

```text
excess contribution = actual contribution - target contribution
```

These are potential sources of capital.

## Receivers

Assets with contribution below target:

```text
shortfall = target contribution - actual contribution
```

These are potential destinations for capital.

Then generate possible pairs:

```text
sell SPY → buy IEF
sell SPY → buy EFA
sell GLD → buy IEF
sell GLD → buy EFA
```

The list can be ranked using simple rules:

- largest donor excess first;
- largest receiver shortfall first;
- perhaps prefer trades that remain within position constraints;
- perhaps avoid trades that are too small to be meaningful.

This creates a **funding-aware candidate list** without solving the full rebalance.

Example:

| Pair | Sell | Buy | Rationale |
|---|---|---|---|
| P01 | SPY | IEF | Move capital from excess equity risk to under-represented defensive risk |
| P02 | SPY | EFA | Reduce SPY concentration while increasing EFA contribution |
| P03 | GLD | IEF | Reduce excess GLD contribution and increase IEF allocation |

## Important limitation

The pair is based on risk-contribution drift, not on a guarantee that the pair will reduce the total drift after trading.

It should therefore be labelled something like:

> **Directional funding proposal**

rather than:

> **Recommended rebalance**

That wording matters.

---

# Approach 4: Candidate trade plus simple impact assessment

A useful intermediate design is:

1. Generate candidates from contribution drift.
2. Apply each candidate hypothetically.
3. Recalculate the portfolio risk contribution.
4. Report the resulting change.

For example:

```text
Current:
SPY RC = 42%
SPY target = 30%

Hypothetical trade:
Sell SPY by 50 bp

Recalculated:
SPY RC = 40%
IEF RC = 13%
Portfolio volatility = slightly lower
```

For a paired trade:

```text
Sell SPY by 50 bp
Buy IEF by 50 bp

Recalculated:
SPY RC = 40%
IEF RC = 15%
maximum absolute RC drift falls from 13% to 10%
```

This is still not solving for the target weights. It is simply answering:

> **What would happen under this particular candidate trade?**

That is a scenario or sensitivity analysis rather than an optimisation problem.

This may be the most valuable step after the crude directional list because it exposes an important reality:

> A trade can point in the intuitively correct direction while having a smaller, larger, or even opposite effect than expected once covariance and the portfolio-volatility denominator are considered.

## Possible evaluation measures

For each hypothetical trade, report:

- change in each asset’s risk contribution;
- change in total portfolio volatility;
- change in maximum absolute contribution drift;
- change in the number of assets outside tolerance;
- whether any constraints are breached.

For example:

```text
maximum drift before: 13%
maximum drift after:  10%
number outside band:  3 → 2
portfolio volatility: 8.4% → 8.2%
```

The system should not necessarily use these metrics to automatically choose a trade yet. It could simply show them to support human selection.

---

# Approach 5: Greedy sequential selection

A more advanced approach would repeatedly select the trade that appears to improve the situation most.

For example:

1. Generate all valid candidate trades.
2. Apply each one hypothetically.
3. Calculate an improvement score.
4. Select the best candidate.
5. Update the portfolio.
6. Repeat until:
   - drift is within tolerance;
   - the trade budget is exhausted;
   - no candidate improves the score.

A simple score might be:

```text
score =
    reduction in maximum absolute RC drift
    - transaction-cost penalty
    - turnover penalty
```

This is not yet a full optimiser, but it is already an **iterative heuristic**.

It introduces questions such as:

- Does the order of trades matter?
- How do we prevent oscillation?
- Should we prioritise the largest contributor or the largest drift?
- Do we stop after one trade or continue?
- How do we deal with several equally good candidates?
- How do we penalise turnover?
- Should the objective be maximum drift, squared drift, or something else?

That may be entirely appropriate later, but it is a meaningful complexity jump.

I would not call this “just generating a candidate list” anymore. It is closer to:

> **A rule-based rebalance proposal engine.**

---

# Approach 6: Full constrained optimisation

At the far end, the system would solve for new weights:

```text
choose new weights
subject to:
    weights sum to one
    position bounds
    turnover limits
    liquidity constraints
    long-only restrictions
    cash constraints

while minimising:
    distance from target risk contributions
    + transaction costs
    + turnover penalty
```

This is the portfolio-construction problem you explicitly wanted to exclude from crude V1.

It could be a later phase, but it should not be allowed to appear implicitly through an overcomplicated “candidate list” feature.

---

# A useful staged roadmap

I would think about the progression like this:

## V1A — Directional triage

Generate:

- reduce candidates;
- add candidates;
- contribution drift;
- priority;
- reason.

No trade sizes. No funding logic.

```text
SPY — reduce — contribution 42%, target 30%, excess +12%
IEF — add — contribution 12%, target 25%, shortfall -13%
```

## V1B — Standard-sized proposals

Add configurable trade-size templates:

```text
SPY — reduce by 25 bp
SPY — reduce by 50 bp
IEF — add by 25 bp
IEF — add by 50 bp
```

Still no claim that any size restores the target.

## V1C — Funding-aware pairs

Generate:

```text
sell SPY / buy IEF
sell GLD / buy EFA
```

with equal notional or equal weight changes.

## V1D — Hypothetical impact

For each candidate or pair:

- recompute risk contributions;
- show before/after drift;
- show portfolio-volatility change;
- show constraint checks.

The user still chooses the trade.

## V2 — Rule-based proposal selection

Use a transparent greedy heuristic to rank or select proposals.

## Later — Optimisation

Solve for the required portfolio weights subject to explicit constraints.

---

# My recommendation for this project

For the project’s purpose, I would make the first candidate-trade artifact deliberately modest:

## Candidate Trade List

Each row contains:

- candidate ID;
- asset or asset pair;
- direction;
- current weight;
- current risk contribution;
- target risk contribution;
- signed drift;
- proposed trade-size template;
- funding source, if applicable;
- rationale;
- status: candidate only.

Example:

| ID | Trade | Current RC | Target RC | Drift | Size | Rationale |
|---|---|---:|---:|---:|---:|---|
| C01 | Reduce SPY | 42% | 30% | +12% | 50 bp | Largest excess contribution |
| C02 | Add IEF | 12% | 25% | -13% | 50 bp | Largest contribution shortfall |
| C03 | Sell SPY / buy IEF | — | — | — | 50 bp | Funding-aware transfer |

Then make the boundary explicit:

> These candidates are generated from current risk-contribution drift. They indicate direction and possible trade sizes; they do not solve for the weights required to restore target contributions. Any post-trade risk estimate is a hypothetical scenario, not an optimised rebalance.

That gives you a clean vertical slice:

```text
risk contribution snapshot
        ↓
drift classification
        ↓
candidate directional trades
        ↓
human review
        ↓
optional hypothetical post-trade assessment
```

## One design decision I would make early

Do not let “candidate trade list” silently mean “recommended trades”.

You could use three distinct terms:

- **Signal**: the asset is above or below its target contribution.
- **Candidate trade**: a possible action derived from the signal.
- **Rebalance proposal**: a selected and funded set of trades with impact analysis.

That terminology gives you room to increase sophistication later without pretending that the V1 output is more rigorous than it is.
