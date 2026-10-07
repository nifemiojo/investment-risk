Yes — I think this is the correct refinement of the next feature.

The existing roadmap jumps fairly quickly from:

```text
Risk Snapshot
    ↓
Risk Change Report
    ↓
Attribution
```

But the PM’s actual first question is more basic:

> **Has the portfolio-level risk state changed, and how significant is the change?**

Only after answering that does it make sense to ask:

> **Why did it change?**

So I would separate the workflow into three distinct steps:

```text
1. Current risk state
   “What risk is the portfolio taking now?”

2. Risk change
   “How different is the current risk state from the reference state?”

3. Risk diagnosis
   “What appears to explain the change?”
```

Attribution belongs in step 3, not step 2.

---

# 1. Why the PM needs portfolio-level risk change first

The PM is responsible for the portfolio as a whole, not just its individual positions.

Before looking at assets, correlations, or contribution, they need to know whether the portfolio has moved into a meaningfully different risk state.

That supports several decisions.

## Decision 1: Does this require a different level of attention?

The PM may need to distinguish between:

```text
Risk is stable
Risk has increased modestly
Risk has increased materially
Risk has breached a limit
Risk is falling again after a previous increase
```

The immediate decision is not necessarily “trade.”

It is more likely:

> **Should this remain part of routine monitoring, or should I spend time investigating it?**

This is the portfolio-level equivalent of triage.

---

## Decision 2: Has the portfolio moved closer to, or further from, its risk budget?

The PM needs to understand not only whether risk changed, but whether the available risk capacity changed.

For example:

| State | VaR | Risk budget | Utilisation |
|---|---:|---:|---:|
| Earlier | 8.0% | 10.0% | 80% |
| Current | 9.5% | 10.0% | 95% |

The important decision-support information is:

- the portfolio is carrying more risk;
- headroom has reduced;
- a future volatility increase could create a breach;
- adding a new position may now have a different implication.

This does not mean the system should say “reduce risk.” That would require mandate, expected-return, liquidity, cost, and constraint information.

But it should make the change in risk capacity visible.

---

## Decision 3: Is this a transient movement or a persistent change in state?

A one-day increase may not deserve the same response as a persistent change across several observations.

The PM may ask:

> “Has risk actually moved to a new level, or am I looking at a noisy daily observation?”

This means the change view should provide some temporal context, even though it should not yet explain the cause.

A simple risk history can help distinguish:

```text
One-day spike
Gradual rise
Sudden step-change
Persistent elevation
Risk already falling
```

The view does not need to classify these automatically in V1. The important thing is that the PM can see the current and comparison points in context.

---

## Decision 4: Should the PM escalate or communicate the state?

If the portfolio has breached a formal limit, the decision may be procedural:

- notify the investment committee;
- record the breach;
- begin an investigation;
- monitor more frequently;
- consider an approved response process.

This is different from a portfolio-manager decision to change the allocation.

The system should distinguish:

```text
Risk changed
Risk is unusually high
Risk budget was breached
```

Those are related but not identical statements.

---

## Decision 5: Is there evidence that the investment process is behaving as intended?

A systematic multi-asset portfolio is expected to have a certain risk role.

The PM may want to know:

> “Is the portfolio still operating within the risk characteristics I expect?”

The first question remains portfolio-level:

> “Is total risk materially different from its prior state?”

The asset-level explanation comes later.

# 2. The proposed artifact question

I would define this artifact as a **Portfolio Risk Change View** or **Risk Comparison View**, rather than immediately calling it a diagnostic report.

Its primary question should be:

> **How has the portfolio’s estimated total risk changed between the current date and a defined comparison date?**

A slightly more decision-oriented version is:

> **Is the portfolio’s current risk state materially different from its reference state, and does that warrant a different level of PM attention?**

That gives the artifact a useful decision without pretending to explain causality.

---

# 3. The questions the PM wants answered

The view should answer these in order.

## A. What is the current risk state?

> **What is the portfolio’s current total risk?**

Minimum evidence:

- observation date;
- portfolio name;
- current VaR;
- current VaR as a percentage of NAV;
- current VaR in currency;
- risk budget;
- budget utilisation;
- historical percentile.

The existing Risk Snapshot already owns this question.

---

## B. What is the reference state?

> **What earlier state am I comparing against?**

The PM must be able to identify:

- comparison date;
- comparison VaR;
- comparison VaR as a percentage of NAV;
- comparison budget utilisation;
- comparison percentile;
- comparison assumptions.

The comparison date cannot be implicit. Otherwise the PM cannot tell whether “risk increased” means since yesterday, since the last review, or since the start of a market episode.

---

## C. How much did risk change?

> **What is the size and direction of the change?**

Show both absolute and relative change.

For example:

| Measure | Earlier | Current | Change |
|---|---:|---:|---:|
| VaR as % of NAV | 8.0% | 9.5% | +1.5 percentage points |
| VaR in currency | £800k | £950k | +£150k |
| Relative change | — | — | +18.75% |
| Budget utilisation | 80% | 95% | +15 percentage points |
| Historical percentile | 62nd | 91st | +29 percentile points |

The labels matter.

Do not display only:

```text
+18.75%
```

because the PM needs to know whether that means:

- an 18.75% relative increase;
- an increase of 18.75 percentage points;
- a change in currency;
- or a change in annualised volatility.

For risk percentages, use **percentage points** for the absolute difference and **percent** for the relative difference.

---

## D. Is the current state unusual in context?

> **Is this just a change, or is the current level unusual relative to the portfolio’s own history?**

This is where the existing percentile measure is useful.

The PM may see:

```text
Risk increased by 1.5 percentage points
Current risk is at the 91st historical percentile
```

Those two facts are more useful together than either alone.

A large change from an unusually low starting point may still leave the portfolio within its normal range.

A smaller change may be important if it moves the portfolio into an unusually high historical state.

---

## E. Has risk-budget capacity changed?

> **How much risk capacity is now being used?**

The view should show:

- current utilisation;
- earlier utilisation;
- change in utilisation;
- current headroom;
- whether a formal budget breach exists.

For example:

```text
Current utilisation: 95%
Earlier utilisation: 80%
Headroom: 5%
Status: within budget
```

The status should be descriptive. “Within budget” is different from “safe” or “appropriate.”

---

## F. Is the change persistent enough to warrant attention?

> **Does the history suggest a new risk state, or a short-lived movement?**

A small line chart could show:

```text
Trailing portfolio VaR
Earlier comparison date
Current date
Risk budget
```

This is probably more useful than adding generated prose.

The chart should allow the PM to see whether the current observation is:

- an isolated spike;
- part of a sustained rise;
- a gradual drift;
- a return toward normal;
- or a persistent elevated state.

---

# 4. The UX position

I would place this **after the current Risk Snapshot and before Attribution**.

```text
Portfolio review
        ↓
Current Risk Snapshot
“What is the risk now?”
        ↓
Risk Change View
“How different is it from the reference state?”
        ↓
Attribution / diagnosis
“What appears to explain the change?”
        ↓
Later analysis
“Is the allocation appropriate?”
        ↓
Much later
“What trade, if any, should be made?”
```

The key UX principle is progressive disclosure.

The PM should not initially be presented with the covariance matrix or component-contribution table. They should first see whether the portfolio-level state has changed enough to justify opening those details.

## Suggested screen structure

```text
┌──────────────────────────────────────────────┐
│ Portfolio Risk Snapshot                       │
│ 60/40 Multi-Asset · 14 March 2022             │
├──────────────────────────────────────────────┤
│ CURRENT RISK STATE                            │
│ VaR: 9.5% of NAV        £950k                 │
│ Budget utilisation: 95%                         │
│ Historical percentile: 91st                    │
├──────────────────────────────────────────────┤
│ CHANGE SINCE 31 January 2022                  │
│ Earlier VaR: 8.0%         Current: 9.5%       │
│ Change: +1.5 percentage points                │
│ Relative change: +18.75%                      │
│ Utilisation change: +15 percentage points      │
├──────────────────────────────────────────────┤
│ RISK HISTORY                                  │
│ trailing VaR chart                            │
│ comparison marker · current marker · budget    │
├──────────────────────────────────────────────┤
│ METHOD AND SCOPE                              │
│ Historical VaR · 95% confidence · 252-day     │
│ rolling window · fixed portfolio weights      │
└──────────────────────────────────────────────┘
```

The next diagnostic layer could be available later, but it should not be mixed into this first view.

---

# 5. What should and should not be in this feature

## Include

- current portfolio-level risk;
- comparison-date portfolio-level risk;
- explicit comparison period;
- absolute change;
- relative change;
- change in budget utilisation;
- current headroom;
- historical percentile context;
- a simple risk history;
- data and methodology metadata;
- clear positive and negative change representation.

## Exclude for now

- asset-level contributions;
- component volatility;
- correlation changes;
- volatility attribution;
- factor attribution;
- explanations such as “equity volatility caused the increase”;
- generated causal narratives;
- “reduce SPY” or any trade recommendation;
- target-weight comparisons;
- rebalance sizing.

The boundary should be explicit:

> **This view describes how the estimated portfolio-level risk changed. It does not explain the source of the change or recommend a portfolio action.**

That is a strong boundary, not a deficiency.

---

# 6. Important distinction: level and change are separate signals

I would avoid reducing the whole view to a single “risk increased” flag.

The PM needs at least two dimensions:

```text
1. Current risk level
2. Change from reference state
```

Conceptually:

| Current level | Change | Possible PM interpretation |
|---|---|---|
| Normal | Stable | Routine monitoring |
| Normal | Rising | Early warning or closer monitoring |
| High | Stable | Persistent elevated risk; investigate mandate/context |
| High | Rising | Highest-priority review state |
| High | Falling | Risk is improving, but may remain elevated |
| Low | Falling | More headroom, but not automatically a reason to add risk |

The system does not need to attach normative labels to every cell yet. The point is that **current level and direction are different pieces of evidence**.

A portfolio can have:

- high but stable risk;
- low but rapidly increasing risk;
- high and falling risk;
- low and stable risk.

A single current VaR number cannot express those distinctions.

---

# 7. The comparison-date design decision

This is probably the most important unresolved UX question.

Possible comparison bases include:

| Comparison basis | Useful for | Risk |
|---|---|---|
| Previous trading day | Daily monitoring | Can be noisy |
| Previous week | Short-term operational review | May miss a slower change |
| Previous month | Regular PM review | More stable, less reactive |
| Last formal review | Governance and decision records | Requires review dates |
| User-selected date | Historical investigation | Less automatic |
| Rolling history | Trend context | Does not define one comparison state |

My recommendation for the first version is:

1. Make the comparison date explicit.
2. Support one default comparison period.
3. Allow a selected historical comparison date for case-study replay.
4. Show the full trailing history alongside the two-point comparison.

However, the default period should come from the intended PM workflow. If the PM reviews risk weekly, “since last week” is more meaningful than “since yesterday.”

---

# 8. The historical VaR limitation

Because the current system uses historical VaR, the wording should be careful.

The view should say something like:

> **Estimated historical VaR increased from 8.0% to 9.5% of NAV between the comparison and current dates. This reflects a change in the empirical return distribution used by the rolling estimation window. It does not, by itself, establish the economic cause of the change.**

That avoids claiming that the portfolio itself has mechanically become more risky in an absolute sense.

With fixed weights, the feature can compare changes in:

- the portfolio return distribution;
- the rolling historical VaR estimate;
- the historical percentile;
- the risk-budget utilisation.

It should not claim that the holdings or portfolio composition changed, because V1 does not model dynamic weights.

---

# 9. Proposed final workflow boundary

I would define the first three artifacts like this:

| Artifact | Primary question | Decision supported |
|---|---|---|
| **Risk Snapshot** | What risk is the portfolio taking now? | What is the current state? |
| **Risk Change View** | How has portfolio-level risk changed? | Does the current state warrant more attention? |
| **Attribution** | Where does structural risk currently live? | Which positions should be examined first? |

Then later artifacts can answer:

| Artifact | Question |
|---|---|
| Diversification analysis | Have risk relationships changed? |
| Drift analysis | Is the portfolio different from its intended allocation? |
| Rebalance analysis | What would happen if weights changed? |
| Trade recommendation | What should actually be traded? |

So the refined workflow becomes:

```text
Monitor current state
        ↓
Compare portfolio-level risk
        ↓
Decide whether deeper review is warranted
        ↓
Diagnose the change
        ↓
Assess allocation and constraints
        ↓
Consider trades
```

My recommendation is therefore:

> **Make the next feature a standalone, evidence-first Portfolio Risk Change View. It should compare two portfolio-level risk states, show the magnitude and context of the change, and support the decision to increase attention. It should stop before attribution, causal explanation, or trade recommendation.**

The main questions we still need to settle before documenting the design are:

1. What is the PM’s normal comparison cadence: previous day, week, month, or last review?
2. Is the immediate decision “investigate or continue routine monitoring,” or should the change view only present evidence and leave that classification to the existing Snapshot?
3. Which risk measure is primary in the UI: daily VaR, annualised VaR, or both?
4. What reference makes a change “material”: risk budget, historical percentile, absolute percentage-point movement, or a combination?
5. Should the first version compare only two dates, or should a trailing history be part of the minimum view?