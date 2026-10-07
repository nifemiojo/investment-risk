# 001 — Portfolio Return: Just a Weighted Sum

**Date:** 2026-07-22
**Topic:** What a portfolio return actually is, and why it's the foundation of everything that follows

---

## Here's what you know

You've spent 11 notebooks computing historical VaR for SPY. Every notebook does the same thing at its core:

```
returns → sort → read the 5th percentile → that's your VaR
```

Your functions don't know or care that the returns came from a single stock. `historical_var(returns)` works on any array of numbers. This is the architectural insight the plan praises: *the separation pays off here.*

## Here's the concrete example

Let's say you hold two positions:

| Asset | Allocation | Daily return today |
|-------|-----------|-------------------|
| SPY (US stocks) | £600,000 (60%) | +0.50% |
| BND (US bonds) | £400,000 (40%) | −0.20% |

**Question:** What was your portfolio's return today?

## The weighted sum

$$r_p = 0.60 \times (+0.50\%) + 0.40 \times (-0.20\%)$$

$$r_p = 0.30\% + (-0.08\%) = +0.22\%$$

Your £1M portfolio made 0.22%, or £2,200. Stocks went up, bonds went down — but because stocks are 60% of the portfolio, their gain dominated.

**Terms:**
- $r_p$ — portfolio return (decimal)
- $w_1, w_2$ — portfolio weights (fraction of total capital in each asset, must sum to 1)
- $r_1, r_2$ — individual asset returns (decimal)

## The key insight hiding in plain sight

Here's the thing. Imagine you compute that weighted sum for every single day in your history — 1,000+ trading days. You now have a **portfolio return series**: a single column of numbers, one per day, just like the SPY return series you've been working with.

That series already contains *everything* about how SPY and BND interact:

- On days when both went up, the portfolio return is strongly positive
- On days when both went down, the portfolio return is strongly negative
- On days when they moved in opposite directions (like our example), they partially cancel

You don't need to model correlations explicitly. The historical record of $r_p$ captures whatever relationship existed between SPY and BND on each day.

## Where does your understanding break?

Before I go further, let me find the first hazy concept. Here are some questions — not because I expect you to answer all of them, but to locate where we should go deep:

1. The weighted sum itself — is $r_p = \sum w_i r_i$ clear, or does the notation feel abstract?
2. "The portfolio return series already contains the diversification" — does that claim land, or does it feel like we're skipping something?
3. When you think about extending your `historical_var()` to a portfolio, what's your instinct — do you see how it works, or is there a gap?

Pick whichever feels least solid, and we'll go there.
