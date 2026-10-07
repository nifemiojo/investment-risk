## Proposed V1: Volatility Change

The useful question is not simply:

> “Is volatility higher or lower?”

It is:

> **“Has the risk profile of the current allocation changed over time, and is the change broad-based or concentrated in particular assets?”**

That supports the PM’s rebalancing decision by helping distinguish:

- a temporary market-regime change from a persistent change;
- an increase in overall portfolio risk from a redistribution of risk between assets;
- a portfolio-level change from a change driven by one or two positions;
- a change in risk caused by the market environment from one caused by portfolio weights.

The artifact should inform the PM’s review. It should not decide that the portfolio must be rebalanced.

---

# Recommended V1 boundary

I would make V1 an **evidence-only structural volatility trend artifact**.

It would answer:

> **“How has the estimated volatility and risk contribution of the current portfolio changed across recent historical observation dates?”**

The phrase **current portfolio** is important. We would calculate historical rolling covariance estimates using the current portfolio weights.

That means V1 isolates changes in the estimated market relationships and volatility environment. It does **not** yet claim to explain changes caused by historical portfolio trades.

This is a defensible first slice because the existing notebook already has the required point-in-time ingredients:

- asset returns;
- portfolio weights;
- covariance matrix;
- portfolio volatility;
- asset-level risk contributions.

---

# Minimal output

## 1. Portfolio volatility trend

A time-series visual containing:

- observation date;
- annualised portfolio volatility;
- latest volatility;
- previous comparable volatility;
- absolute change;
- percentage change.

For example:

| Observation date | Portfolio volatility |
|---|---:|
| 2024-01-31 | 8.7% |
| 2024-02-29 | 9.1% |
| 2024-03-31 | 10.4% |
| 2024-04-30 | 9.8% |

The primary comparison should be between the latest observation and a prior observation at the same frequency, such as one month earlier.

I would avoid adding thresholds such as “high volatility” or “volatility warning” in V1. Those would require a separate decision about what level is meaningful for this portfolio.

---

## 2. Latest versus prior asset contribution table

Reuse the existing contribution concept rather than introducing a new attribution method.

| Asset | Current weight | Prior risk contribution | Current risk contribution | Change |
|---|---:|---:|---:|---:|
| SPY | 40% | 53% | 61% | +8 pp |
| EFA | 20% | 21% | 24% | +3 pp |
| IEF | 25% | 17% | 8% | −9 pp |
| GLD | 15% | 9% | 7% | −2 pp |

The main output should remain **percentage contribution to portfolio volatility**, because it is comparable across dates and sums to approximately 100%, including any negative diversification contributions.

The change should be expressed in **percentage points**, not as a percentage change. For example:

- current contribution: 61%;
- prior contribution: 53%;
- change: **+8 percentage points**.

Percentage-point changes are easier to interpret for a contribution that can be positive, zero, or negative.

The table should be ranked by the latest contribution, consistent with the existing snapshot artifact.

---

## 3. Small reconciliation block

The artifact should retain the existing mathematical checks:

- portfolio volatility is positive;
- current component contributions sum to portfolio volatility;
- current percentage contributions sum to approximately 100%;
- prior percentage contributions sum to approximately 100%;
- all assets are present in both periods.

This is especially important for a change artifact because an apparent change could otherwise be caused by a calculation or alignment error.

---

# What this tells the PM

The artifact gives the PM three useful pieces of evidence.

### 1. Direction

Has estimated portfolio risk increased, decreased, or remained broadly stable?

This provides context for the rebalancing decision. A portfolio may still have the same weights while its risk changes materially because correlations or asset volatilities have changed.

### 2. Persistence

Is the latest change part of a continuing trend or just a one-period movement?

A single point-in-time snapshot cannot answer this. A trend visual allows the PM to see whether the latest observation is:

- a continuation of a gradual increase;
- a reversal;
- a sharp isolated movement;
- part of a broader volatility episode.

### 3. Concentration of change

Which assets account for the change in the structural risk profile?

The contribution table can show that total volatility has increased because:

- one asset has become a larger source of portfolio risk;
- several assets have become more volatile together;
- a diversifying asset has stopped offsetting other risk;
- the ranking of risk sources has changed.

This is more decision-relevant than portfolio volatility alone. Two portfolios can have the same headline volatility while having very different risk concentrations.

---

# Important methodological distinction

There are two different things we could call “volatility over time.”

## A. Structural volatility trend

Estimate covariance from a rolling historical window and calculate:

```text
current weights × rolling covariance × current weights
```

This asks:

> “Given today’s allocation, how would the estimated risk of the portfolio have changed as market conditions changed?”

This is the recommended V1.

## B. Realised portfolio volatility

Construct historical portfolio returns and calculate rolling volatility directly.

This asks:

> “How variable were the portfolio’s realised returns over time?”

That is also useful, but it answers a different question. It is affected by the realised sequence of returns and may not reconcile directly to the covariance-based contribution decomposition used in the existing notebook.

For consistency with the existing snapshot, V1 should use the **structural covariance-based measure** and label it clearly. We should not silently mix the two.

---

# The key limitation of V1

If the portfolio weights changed through history, then using current weights throughout the history deliberately excludes the effect of those historical weight changes.

That is not a flaw if we state the boundary clearly. It means:

> “This trend shows how the current allocation’s structural risk would have evolved under changing historical market estimates.”

It does **not** show:

> “The exact risk path of the portfolio actually held at each historical date.”

The second question requires historical weights or transactions and should be a later extension.

This distinction matters because a PM may otherwise interpret an increase in volatility as evidence that the portfolio’s own positioning caused the increase.

---

# Suggested V1 design

I would define the artifact as:

## `Portfolio Volatility Change`

### Decision supported

> Should the PM treat the current portfolio’s risk profile as unchanged, or investigate whether the allocation now has a materially different risk profile?

### Primary evidence

1. Rolling annualised structural portfolio volatility.
2. Latest-versus-prior portfolio volatility change.
3. Latest-versus-prior asset contribution change.

### Method

- current portfolio weights;
- rolling covariance estimates;
- annualised volatility;
- covariance-based component risk contribution;
- observation dates at a regular frequency.

### Deferred

- volatility thresholds;
- “risk alert” labels;
- recommended trades;
- historical weight-change attribution;
- factor-level explanations;
- scenario or stress analysis;
- formal statistical tests for trend;
- separate short-term and long-term regimes.

---

# One design choice to settle

The only significant V1 choice is the rolling estimation window and observation frequency.

My initial recommendation would be:

- **252 trading-day covariance window**;
- **monthly observation dates**;
- annualised volatility;
- latest observation compared with one month earlier;
- visual history covering the available sample.

This gives a relatively stable estimate and avoids making the artifact respond excessively to individual daily observations.

A shorter window, such as 63 trading days, would be more responsive but noisier. It may be useful later as a complementary short-term view, but I would not put both into V1 unless the notebook already has a clear convention for estimation windows.

The main thing to avoid is presenting a smooth-looking trend without making clear that it is generated by overlapping rolling covariance windows. The result is a monitoring signal, not an independent monthly sample of portfolio risk.

Overall, I think this is a worthwhile extension because it turns the existing snapshot from a static diagnostic into the beginning of a decision workflow:

> **current risk level → recent change → persistence → concentration of change → PM investigation/rebalancing judgement**.

It should stop at the evidence needed for that judgement, rather than attempt to make the rebalance decision itself.
