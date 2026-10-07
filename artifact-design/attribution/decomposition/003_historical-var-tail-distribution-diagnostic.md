Exactly. This reframes the artifact from **“How do I allocate VaR across assets?”** to:

> **“What does the lower tail of the portfolio-loss distribution look like, and what is driving it?”**

That is a much more natural use of historical VaR.

## The object being diagnosed

Historical VaR is a quantile of the portfolio-loss distribution. At, say, 99% confidence:

- the **VaR level** is the loss threshold near the lower tail;
- observations beyond that threshold are worse losses;
- those observations represent the portfolio’s historically severe scenarios;
- the asset-level P&L contributions explain the composition of each scenario.

One terminology refinement: VaR does not identify the “worst-case scenario” in an absolute sense. It identifies a **tail threshold** or, depending on the historical quantile convention, one observation near that threshold. The worst historical losses may be substantially beyond VaR.

So the diagnostic should distinguish:

1. **VaR boundary**
   - What loss level marks the selected percentile?

2. **Tail observations**
   - Which scenarios are at or beyond that boundary?

3. **Extreme observations**
   - What are the largest losses in the historical sample?

That avoids treating one VaR-defining day as if it were the whole tail.

---

# What the tail diagnostic is trying to understand

The PM is effectively asking:

> “What kind of market conditions produce the portfolio’s severe losses?”

And then:

> “Which assets and interactions are responsible for those losses?”

That leads to several useful questions.

## 1. How severe is the tail?

- What is the historical VaR?
- How far below VaR are the worst observations?
- Is the tail thin and tightly clustered?
- Is there a large gap between the VaR boundary and the worst losses?
- Has the tail become more severe since the previous snapshot?

This distinguishes a modest movement in the percentile from a genuinely more damaging downside distribution.

## 2. How broad is the tail?

- Are the losses spread across many different historical episodes?
- Or are they concentrated in one crisis period?
- Does one event account for most of the tail observations?
- Are the current tail scenarios representative of several regimes?

This matters because a VaR increase driven by one historical episode has a different interpretation from a broad deterioration across many periods.

## 3. What is the composition of the losses?

For each tail scenario:

$$
L_t = \sum_i L_{i,t}
$$

where:

- $L_t$ is the portfolio loss on historical scenario $t$;
- $L_{i,t}$ is asset $i$’s contribution to that loss.

This is an exact decomposition of the realised portfolio loss on that scenario.

Across a selected tail set $\mathcal{T}$, you could calculate:

$$
\bar{L}_i
=
\frac{1}{|\mathcal{T}|}
\sum_{t \in \mathcal{T}} L_{i,t}
$$

This answers:

> “Across these severe historical scenarios, what was the average loss contribution from each asset?”

The contributions remain additive across the selected scenarios:

$$
\frac{1}{|\mathcal{T}|}
\sum_{t \in \mathcal{T}} L_t
=
\sum_i \bar{L}_i
$$

This is not a decomposition of VaR itself. It is a decomposition of the **average loss across a defined tail set**.

That wording is important and honest.

---

# The useful distinction: VaR boundary versus tail composition

A single VaR scenario can answer:

> “What happened on the observation nearest the VaR threshold?”

A tail set can answer:

> “What tends to happen across the portfolio’s severe historical losses?”

The second is probably more useful for your project because it is less dependent on one arbitrary observation.

For example, suppose the 99% tail contains five observations. The artifact could show:

| Tail statistic | Value |
|---|---:|
| VaR threshold | -4.8% |
| Worst historical loss | -8.6% |
| Number of tail observations | 5 |
| Average tail loss | -6.1% |
| Tail date concentration | 4 of 5 observations from one crisis period |

Then show average asset loss contribution:

| Asset | Average tail P&L | Share of average tail loss |
|---|---:|---:|
| SPY | -3.1% | 51% |
| EFA | -1.8% | 30% |
| IEF | -0.6% | 10% |
| GLD | -0.6% | 10% |

The PM can then ask:

- Is the tail primarily an equity sell-off?
- Did bonds diversify the portfolio in these scenarios?
- Did all assets become loss-making together?
- Is gold providing protection or adding to losses?
- Is the tail composition stable across observations?

Those are meaningful questions about the downside distribution.

---

# A subtle but important point about “drivers”

The tail diagnostic can show what **contributed to observed losses**, but it cannot by itself prove why those assets lost value.

For example, if SPY contributes most of the loss in the tail, the artifact can say:

> “SPY contributed most of the observed portfolio loss across these tail scenarios.”

It should not automatically say:

> “SPY caused the tail.”

That stronger claim could mean several different things:

- SPY had the largest negative return;
- SPY had the largest loss in portfolio currency;
- SPY had the largest contribution relative to its weight;
- SPY was part of a common equity factor shock;
- SPY’s correlation with other assets amplified the portfolio loss.

Those are different analyses.

For v1, I would use language such as:

- **loss contribution**;
- **tail scenario composition**;
- **asset contribution across selected tail observations**;
- **observed co-movement in severe scenarios**.

I would avoid causal language unless a later factor or event analysis supports it.

---

# What “distribution diagnosis” could contain

I think the artifact naturally has four layers.

## Layer 1: Tail position

Where is the current portfolio in relation to its historical loss distribution?

- VaR;
- selected percentile;
- average tail loss;
- worst loss;
- tail depth.

## Layer 2: Tail membership

Which observations make up the relevant tail?

- scenario dates;
- portfolio losses;
- asset returns;
- event or regime labels, if available;
- whether observations entered or exited since the previous window.

## Layer 3: Tail composition

What assets contributed to those losses?

- per-scenario asset P&L;
- average contribution across the tail;
- percentage contribution to average tail loss;
- signs showing whether an asset diversified or amplified losses.

## Layer 4: Tail stability

Is the conclusion robust across the tail?

- Does the same asset dominate most scenarios?
- Does the ranking change materially between observations?
- Is diversification consistently absent?
- Is one observation driving the result?
- Does the composition change between the VaR boundary and the extreme tail?

This last layer is especially useful because it separates:

> “The current VaR observation has this composition”

from:

> “The portfolio’s severe-loss behaviour generally has this composition.”

---

# How this fits with the broader workflow

The sequence becomes:

1. **Risk snapshot**
   - What is historical VaR now?

2. **Risk change**
   - How much did VaR move?

3. **Distribution diagnosis**
   - What changed in the lower tail?
   - Did the tail become deeper, broader, or differently composed?

4. **Tail composition**
   - Which assets contributed to severe historical losses?
   - Which assets diversified those losses?

5. **Structural risk decomposition**
   - Where does current covariance-based portfolio volatility risk live?

6. **Reference comparison**
   - Is this consistent with the intended allocation or risk budget?

7. **Trade analysis**
   - Would a proposed rebalance improve the relevant risk property?

This gives the historical VaR diagnostic a clear place: **immediately after observing a VaR change and before deciding whether the change is actionable**.

---

# It also explains the gap with structural decomposition

The two views are now clearly complementary:

| View | Distribution being examined | Question |
|---|---|---|
| Structural risk decomposition | Estimated covariance structure | Where does current risk live? |
| Historical tail diagnostic | Observed historical loss distribution | What does severe downside look like? |
| Scenario contribution | One or more realised loss observations | What made up these losses? |

They may agree, but they do not need to.

For example:

- structural decomposition says bonds are current diversifiers;
- the historical tail shows bonds lost money during a particular inflation shock;
- both can be true.

The first describes the current estimated relationship between assets and the portfolio. The second describes what actually happened in selected severe historical scenarios.

That difference is precisely what makes the comparison interesting rather than a problem to eliminate.

## The core framing

I would describe the historical VaR artifact as:

> **A lower-tail distribution diagnostic that examines the location, depth, membership, and asset composition of severe historical portfolio-loss scenarios.**

Its job is not to manufacture a component VaR number. Its job is to help the PM understand:

> **What has historically gone wrong for this portfolio, how bad was it, and what was happening across the holdings when it did?**

That is a strong and defensible answer to the “why did risk change?” question—particularly when the change is driven by the empirical tail rather than by a smooth change in covariance-based risk.
