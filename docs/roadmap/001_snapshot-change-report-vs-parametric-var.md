# Recommendation

Choose **Snapshot → Risk Change Report → temporal attribution** before introducing parametric VaR.

This is the higher-value next slice for the project’s stated CV objective.

The short version:

> **Parametric VaR demonstrates another method. Change-over-time demonstrates that you understand how a portfolio risk system is used by an investment professional.**

That distinction matters because your existing employment already provides evidence that you can build quantitative risk systems. The project needs to add evidence that you can connect those systems to **portfolio monitoring, diagnosis, historical context, and investment judgement**.

---

## Why change-over-time is the better next slice

Your project constitution defines the career gap as:

> moving from building risk systems toward understanding how risk information is used in portfolio decisions.

The temporal slice directly advances that.

It creates this workflow:

```text
Risk Snapshot
    ↓
Risk appears unusual
    ↓
Compare current state with prior state
    ↓
What changed?
    ↓
How did the risk allocation change?
    ↓
What hypothesis should the PM investigate?
```

That is much closer to systematic investment-management work than simply adding:

```text
Historical VaR
    ↓
Parametric VaR
```

A hiring manager can immediately understand the value of:

> “I built a portfolio monitoring workflow that identified unusual risk, compared portfolio states over time, and showed how the sources of risk changed across a historical market episode.”

The value of:

> “I implemented both historical and parametric VaR”

is more limited unless it is attached to a specific model-selection decision.

---

## Comparison

| Criterion | Snapshot + temporal attribution | Parametric VaR |
|---|---:|---:|
| Advances the project’s north-star workflow | **High** | Medium |
| Demonstrates PM/investment-management thinking | **High** | Low–medium |
| Builds directly on existing work | **High** | Medium |
| Supports historical replay | **High** | Medium |
| Demonstrates model limitations | **High** | **High** |
| Adds methodological breadth | Medium | **High** |
| Risk of becoming method collection | Low | **High** |
| Interview story | **Strong** | Moderate |
| Necessary for current V1 | **Yes** | No |

The roadmap already points to this sequence. `docs/project-management/v1-roadmap-and-definition-of-done.md` identifies Phase 2 as the Change Report and Phase 3 as attribution. The micro-scope is even clearer: one methodology, one investigation workflow, and one historical case study.

The broader taxonomy currently lists more ambitious Drift and Rebalance work, but that conflicts with the later V1-Micro scope. I would treat the later micro-scope as authoritative for now.

---

# What the next slice should be

I would not turn Attribution itself into a time-series artifact.

Keep Attribution as the point-in-time answer to:

> **Where does structural portfolio risk live at this observation date?**

Then introduce a separate **Risk Change Report** that composes multiple point-in-time artifacts.

## Risk Change Report question

> **What changed between the comparison date and the current date, and what evidence helps explain the change in portfolio risk?**

For example:

```text
Comparison date: 31 January 2022
Current date:    14 March 2022

Risk Snapshot at comparison date
Attribution at comparison date

Risk Snapshot at current date
Attribution at current date

Change Report
```

This respects the project’s artifact taxonomy:

```text
Risk Snapshot ───────┐
                     ├──→ Change Report
Attribution ─────────┘
```

The Change Report is not a replacement for Attribution. It is a temporal composition of two point-in-time observations.

---

## Minimum evidence

The first version only needs to show:

### 1. Portfolio risk changed

- current VaR;
- comparison VaR;
- absolute change;
- percentage change;
- current percentile versus comparison percentile;
- change over a clearly defined interval.

### 2. The structural risk allocation changed

For each asset:

| Asset | Weight | Earlier risk contribution | Current risk contribution | Change |
|---|---:|---:|---:|---:|
| SPY | 40% | 55% | 67% | +12 pp |
| EFA | 20% | 18% | 22% | +4 pp |
| IEF | 25% | 8% | -3% | -11 pp |
| GLD | 15% | 19% | 14% | -5 pp |

The exact numbers would come from the system. The important point is that the PM can see not only that total risk changed, but that **the portfolio’s risk allocation changed**.

### 3. The ingredients of risk changed

Show supporting evidence such as:

- asset volatility at each date;
- selected pairwise correlations;
- especially equity–bond correlation;
- the contribution of each asset to current structural volatility;
- whether the historical VaR window gained or lost extreme observations.

### 4. An honest diagnostic conclusion

The report might say:

> Portfolio risk increased materially between the comparison and current dates. The increase coincided with higher equity volatility and a deterioration in the diversification relationship between equities and bonds. Equity assets also represented a larger share of structural portfolio volatility at the current date. These observations support the hypothesis that the increase was driven by both higher equity risk and weaker diversification, but they do not establish a unique causal decomposition of the total change.

That is a credible investment-management statement. It distinguishes:

- observed evidence;
- plausible interpretation;
- what the model cannot prove.

---

# Important scope constraint: fixed weights

The current project uses fixed portfolio weights.

That means the first temporal slice should **not** claim to diagnose changing portfolio composition or weight drift. The current code and design support changes in:

- estimated volatility;
- estimated covariance;
- estimated correlation;
- the empirical return distribution;
- the observations entering or leaving the rolling window.

They do not yet support genuine changes in holdings or weights.

So the first Change Report should say:

> This version holds portfolio weights constant. Changes in risk are therefore examined through the estimated return distribution and covariance structure, not through active portfolio reweighting.

That is not a weakness. It is a useful modelling boundary.

It also gives you a good future extension:

```text
V1:
Fixed weights
→ risk changes caused by market behaviour and estimation window

Later:
Changing weights
→ distinguish market-driven change from portfolio-composition-driven change
```

Do not add dynamic weights merely to make the artifact look more complete. Add them when you need to answer that specific diagnostic question.

---

# Where parametric VaR should go

Parametric VaR is still valuable, but I would position it as a later **model-risk and method-selection investigation**, not as the next main project slice.

A decision-first version would be:

> **Would the investigation decision change if portfolio risk were estimated using a parametric covariance model rather than historical VaR?**

That is much stronger than simply implementing a second calculator.

The later artifact could compare:

```text
Historical VaR
Parametric VaR
Structural volatility attribution
```

For selected historical events, it could ask:

- Did both methods identify the same unusual-risk period?
- Did parametric VaR smooth away an important tail event?
- Did historical VaR react slowly after a regime change?
- Did the method choice change whether the PM would investigate?
- Does the parametric model produce a more internally coherent attribution?
- Which method is more interpretable for this specific decision?

That would make parametric VaR meaningful.

It could also help address the current methodological boundary: your Snapshot uses **historical VaR**, while Attribution decomposes **structural covariance-based volatility**. Parametric VaR would make it possible to place the headline risk measure and component attribution on a more directly connected basis.

But that is a second-order improvement. It should come after the project has demonstrated the core workflow.

---

# Recommended sequence

## Next: Change Report and temporal attribution

Scope it as:

```text
One portfolio
One historical VaR method
Two observation dates
Two point-in-time attributions
One Risk Change Report
One historical investigation case
```

The report should answer:

> **What changed, how did the risk allocation change, and what evidence supports a first diagnostic hypothesis?**

Stop before:

- causal attribution of every basis point;
- dynamic weight decomposition;
- factor attribution;
- trade recommendations;
- drift analysis;
- model comparison.

## Then: historical operation

Run the workflow through a selected episode:

```text
Snapshot at t₀
Snapshot at t₁
Investigation trigger
Change Report
Attribution comparison
PM-style interpretation
Limitations
```

This is the point at which the project becomes much more compelling as a CV artifact.

## Later: parametric method as model-risk analysis

Only after the historical workflow works:

```text
Historical method
    vs
Parametric method
    ↓
Would the investigation decision change?
```

That makes parametric VaR serve the project rather than becoming a disconnected feature.

---

# Final decision

I would record the next priority as:

> **Build the Risk Change Report: compare two point-in-time portfolio-risk snapshots and their asset-level structural attributions to support the PM’s diagnosis of what changed.**

And defer parametric VaR to:

> **A later model-method comparison focused on whether methodology choice changes the investigation decision.**

This gives you the stronger career signal:

```text
Existing strength:
I can build quantitative risk systems.

Project evidence to add:
I understand how portfolio risk changes over time,
how a PM investigates it,
and where the analysis stops being conclusive.
```

That is the higher-value bridge from market-maker/dealer quant development toward systematic investment management.
