# 002 — Deriving the Portfolio Return and Seeing Diversification in the Numbers

**Date:** 2026-07-22
**Topic:** Where the weighted sum comes from, and how a single column of portfolio returns encodes how assets move together

---

## Part A: Deriving the weighted sum from first principles

### What is a portfolio?

A portfolio is a collection of positions. You own some number of shares (or units, or contracts) of each asset.

Let's define:

| Variable | Meaning |
|----------|---------|
| $n_i$ | Number of units of asset $i$ you hold (e.g. 1,200 shares of SPY) |
| $p_i$ | Price per unit of asset $i$ (e.g. \$500 per share) |
| $V_i = n_i \times p_i$ | Market value of your position in asset $i$ |
| $V = \sum V_i$ | Total portfolio value |

### What is a return?

A return measures the proportional change in value over a period. For a single asset:

$$r_i = \frac{p_{i, \text{end}} - p_{i, \text{start}}}{p_{i, \text{start}}}$$

Equivalently: $p_{i, \text{end}} = p_{i, \text{start}} \times (1 + r_i)$

Since the number of units doesn't change (we're measuring a passive holding period), the position value changes by the same proportion:

$$V_{i, \text{end}} = V_{i, \text{start}} \times (1 + r_i)$$

### Now derive the portfolio return

The portfolio return $r_p$ is the proportional change in total portfolio value:

$$r_p = \frac{V_{\text{end}} - V_{\text{start}}}{V_{\text{start}}}$$

Substitute $V = \sum V_i$:

$$r_p = \frac{\sum V_{i, \text{end}} - \sum V_{i, \text{start}}}{\sum V_{i, \text{start}}}$$

Replace $V_{i, \text{end}}$ with $V_{i, \text{start}} \times (1 + r_i)$:

$$r_p = \frac{\sum V_{i, \text{start}} \times (1 + r_i) - \sum V_{i, \text{start}}}{\sum V_{i, \text{start}}}$$

$$r_p = \frac{\sum V_{i, \text{start}} + \sum V_{i, \text{start}} \times r_i - \sum V_{i, \text{start}}}{\sum V_{i, \text{start}}}$$

The $\sum V_{i, \text{start}}$ terms cancel:

$$r_p = \frac{\sum V_{i, \text{start}} \times r_i}{\sum V_{i, \text{start}}}$$

Now define the portfolio weight $w_i$:

$$w_i = \frac{V_{i, \text{start}}}{V_{\text{start}}}$$

This is "what fraction of my total capital is in asset $i$." By construction, $\sum w_i = 1$.

Then:

$$r_p = \sum_{i=1}^{n} w_i \times r_i$$

**That's it.** The portfolio return is a capital-weighted average of the individual asset returns. No assumptions. Just algebra from the definition of a return.

**Terms:**
- $n_i$ — units held of asset $i$ (constant over the period)
- $p_i$ — price per unit of asset $i$
- $V_i = n_i \times p_i$ — position value in asset $i$
- $V = \sum V_i$ — total portfolio value
- $r_i$ — return of asset $i$ over the period (decimal)
- $r_p$ — portfolio return over the period (decimal)
- $w_i = V_{i, \text{start}} / V_{\text{start}}$ — portfolio weight of asset $i$

---

## Part B: Where is the diversification?

Your question is exactly right: a single number like $r_p = +0.22\%$ tells you the outcome but not *how* you got there. You can't look at $+0.22\%$ and know whether SPY and BND both went up a little, or one soared while the other crashed.

But we don't look at *one* day. We look at the *distribution* of hundreds of portfolio returns. And the shape of that distribution — how spread out it is, how fat its left tail is — is what encodes the diversification.

Let me make this concrete.

### Scenario: Five days of SPY and BND returns

Here are five hypothetical daily returns:

| Day | SPY return | BND return | 60/40 Portfolio return |
|-----|-----------|-----------|----------------------|
| 1 | +1.00% | +0.30% | $0.60(1.00) + 0.40(0.30) = +0.72\%$ |
| 2 | −2.00% | +0.50% | $0.60(-2.00) + 0.40(0.50) = -1.00\%$ |
| 3 | +0.50% | −0.10% | $0.60(0.50) + 0.40(-0.10) = +0.26\%$ |
| 4 | −1.50% | −0.20% | $0.60(-1.50) + 0.40(-0.20) = -0.98\%$ |
| 5 | +2.00% | +0.10% | $0.60(2.00) + 0.40(0.10) = +1.24\%$ |

Now look at the **distributions** of the three series:

| Statistic | SPY alone | BND alone | 60/40 Portfolio |
|-----------|----------|----------|----------------|
| Best day | +2.00% | +0.50% | +1.24% |
| Worst day | −2.00% | −0.20% | −1.00% |
| Range (best − worst) | 4.00% | 0.70% | 2.24% |

The portfolio's worst day (−1.00%) is better than SPY's worst day (−2.00%). The portfolio's range (2.24%) is smaller than SPY's range (4.00%).

**This is diversification, made visible in the numbers.** The portfolio return series has a narrower distribution than the individual assets — specifically, its extremes are less extreme.

### Where does correlation enter?

Look at Day 2: SPY crashed −2.00%, but BND gained +0.50%. They moved in opposite directions. The portfolio return was only −1.00% — bad, but not as bad as SPY alone.

Look at Day 4: both lost money. The portfolio took the full hit (−0.98%).

The *pattern* of whether assets move together or apart on each day determines the shape of the portfolio return distribution. When they diverge (Day 2), losses cancel. When they converge (Day 4), there's no cushion.

**Correlation is embedded in the portfolio return series through these day-by-day interactions.** It's not a single number you can extract by looking at one $r_p$ — it's a property of the whole distribution. The weighted sum compresses the interaction into a single outcome each day, and then the collection of outcomes reveals the diversification (or lack thereof).

### Connecting to VaR

When you call `historical_var(portfolio_returns, confidence=0.95)`, the function:

1. Sorts all the portfolio returns from worst to best
2. Reads the 5th percentile

That 5th percentile will be less extreme than the 5th percentile of SPY alone — because on many of the worst days for stocks, bonds cushioned the blow.

The gap between "portfolio VaR" and "sum of individual VaRs" is the diversification benefit, measured in risk terms. We'll quantify that in the next file.

---

## Check-in

1. Does the derivation of $r_p = \sum w_i r_i$ from the definition of a return make sense — specifically, why the $V_{i, \text{start}}$ terms cancel?
2. Does the 5-day example make the diversification claim feel less like a leap? The key is: you're not looking at one day's $r_p$, you're looking at the *distribution* of hundreds of them.
3. Is it clear why the weighted sum compresses the interaction but the *distribution* of weighted sums reveals it?
