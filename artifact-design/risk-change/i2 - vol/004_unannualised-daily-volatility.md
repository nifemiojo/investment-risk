I agree with your instinct. **Daily rolling portfolio volatility without annualisation is the simpler and more honest V1 default**, especially if the existing snapshot already works on that basis.

The artifact can answer:

> **“How has the estimated variability of daily portfolio returns changed over the last year?”**

That is a clear question with no need to introduce an additional reporting convention.

## Recommended measure

At each trading day:

1. take the trailing 252 daily asset returns;
2. estimate the covariance matrix;
3. apply the portfolio weights;
4. calculate portfolio volatility;
5. plot the result.

The output is:

> **Rolling standard deviation of daily portfolio returns**

For example:

```text
Date        Rolling daily portfolio volatility
2025-01-02  0.58%
2025-01-03  0.59%
2025-01-06  0.61%
...
```

The chart title could simply be:

> **Rolling Daily Portfolio Volatility — Last Year**

And the y-axis:

> **Daily volatility (%)**

## Why this is a good default

### It matches the calculation basis

We are using daily returns over a daily rolling window, so the output remains on the daily return scale.

There is no translation from:

```text
daily estimate → annualised estimate
```

The measure is easier to explain:

> “Based on the most recent 252 daily returns, the estimated standard deviation of daily portfolio returns is currently 0.62%.”

### It avoids unnecessary assumptions

Annualisation is often useful as a reporting convention, but it adds an implicit interpretation:

```text
daily volatility × √252
```

That is only a scale conversion under assumptions about how risk aggregates through time. Those assumptions are not needed to determine whether the rolling estimate has risen or fallen.

For this artifact, the core decision is about **change**, not whether the portfolio has a particular annual risk level. Since scaling by a constant does not alter the direction, ranking, or relative movement of the series, annualisation adds little analytical value here.

### It keeps the artifact evidence-focused

The unannualised measure avoids making the chart look like a direct forecast of next year’s risk.

It says exactly what was estimated:

> rolling variability of daily returns.

That fits the evidence-only boundary better.

## The main implication

The PM will see smaller numbers:

```text
Current daily volatility: 0.62%
Previous daily volatility: 0.54%
Change: +0.08 percentage points
```

That is perfectly valid, but the artifact should make the units highly visible. The change should probably be presented in **basis points** as well:

```text
Current daily volatility: 0.62%
Previous daily volatility: 0.54%
Change: +0.08 percentage points
Change: +8 basis points
```

Here, 1 basis point is 0.01 percentage points, so 0.08 percentage points equals 8 basis points.

I would treat the percentage-point change as the primary value and basis points as a readability aid.

## What remains comparable?

The following remain comparable across the whole series:

- portfolio volatility level;
- direction of change;
- size of change;
- asset contribution percentages;
- contribution rankings;
- concentration of risk.

Annualisation is not required for any of those.

The asset-level contribution percentages are especially unaffected. If the daily portfolio volatility is multiplied by $\sqrt{252}$, each component volatility is multiplied by the same factor, while percentage contribution remains unchanged.

## Important wording

I would avoid saying merely:

> “Daily portfolio vol”

because that can be interpreted loosely.

The precise internal definition should be:

> **Portfolio volatility measured as the rolling standard deviation of daily portfolio returns, using a 252-trading-day estimation window.**

For the PM-facing chart:

> **Rolling daily portfolio volatility**

With a methodology note:

> The estimate is recalculated at each trading day using the trailing 252 daily asset returns and current portfolio weights. Values are shown on the daily-return scale and are not annualised.

## One subtle distinction

This does not mean that we calculate a realised portfolio return series using historical portfolio weights. If the design continues to use current weights at every historical date, the measure remains:

> the estimated daily volatility of the current allocation under historical rolling covariance conditions.

That convention should remain explicit, because it is more important to the interpretation than whether the result is annualised.

## Recommendation

I would revise the V1 decision to:

> **Calculate portfolio volatility daily using a rolling 252-trading-day covariance estimate from daily asset returns, apply the current portfolio weights, and display the resulting rolling daily portfolio volatility over the last year without annualisation.**

This gives us a clean first implementation:

```text
daily returns
→ rolling 252-day covariance
→ current weights
→ daily portfolio volatility
→ daily one-year chart
```

Annualised volatility can remain a later presentation option if we discover that PM comparisons with annual risk budgets require it. It does not need to be part of the core risk-change measure.
