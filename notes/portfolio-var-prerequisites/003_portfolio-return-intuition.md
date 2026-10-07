# 003 — Intuition: The Portfolio Return as Position P&L Summed Up

**Date:** 2026-07-22
**Topic:** Mental models for why $r_p = \sum w_i r_i$ — what's actually happening under the hood

---

## Mental model 1: You own positions, not percentages

This is the most grounded model, and it connects directly to your work at Spreadex.

You don't think "I'm 60% SPY." You think "I have a £600,000 SPY position and a £400,000 BND position." Each position has its own P&L in pounds:

| Position | Value | Today's move | P&L (£) |
|----------|-------|-------------|---------|
| SPY | £600,000 | +0.50% | +£3,000 |
| BND | £400,000 | −0.20% | −£800 |

**Total portfolio P&L = +£3,000 + (−£800) = +£2,200**

To express this as a return, divide by total value:

$$r_p = \frac{+\pounds 2,200}{\pounds 1,000,000} = +0.22\%$$

That's it. The portfolio return is just **total P&L ÷ total exposure.** You're summing the actual pounds gained and lost across all positions, then normalising.

The algebraic form $r_p = \sum w_i r_i$ is the same thing, just factored differently:

$$r_p = \frac{600,000 \times 0.005 + 400,000 \times (-0.002)}{1,000,000} = 0.60(0.005) + 0.40(-0.002)$$

But the P&L-sum version is easier to hold in your head because it maps to what you actually see: positions, prices, P&L.

---

## Mental model 2: The weights are volume knobs

Think of a mixing desk. Each asset is a channel with a fader:

```
SPY  ████████████████░░░░  60%  ← louder
BND  ██████████░░░░░░░░░░  40%  ← quieter
```

On any given day, the portfolio return is the weighted blend of whatever each asset did. The weight is how loud that asset's voice is in the mix.

- If SPY screams +2% and BND whispers +0.1%, the portfolio is pulled strongly positive — SPY is both louder (60% weight) and shouting louder (bigger move)
- If SPY screams −2% and BND whispers +0.5%, they pull in opposite directions, and SPY's voice dominates — but BND takes the edge off
- If both whisper around zero, the portfolio barely moves

**The weight determines how much of each asset's return makes it into the final number.** A 60% weight means: "I care about SPY's return 1.5× as much as BND's."

---

## Mental model 3: The weighted sum is just the "centre of mass"

If you've ever computed a weighted average for anything — a course grade, a portfolio of exam scores, a blended interest rate — this is the same idea.

You have two exam scores and one counts for 60% of the grade:

$$\text{Final grade} = 0.60 \times 85\% + 0.40 \times 92\% = 87.8\%$$

The portfolio return is exactly the same computation. The only difference is that the "scores" ($r_i$) change every day. But the mechanics are identical: multiply each score by its importance weight, sum them up.

---

## The unifying thread

All three models say the same thing: **the portfolio return is what you get when you add up the actual money made and lost across all your positions, then divide by the starting capital.**

The algebraic form $r_p = \sum w_i r_i$ is just the compact way to write that. But the position-P&L version is what's actually happening in your systems at Spreadex — every risk report, every P&L breakdown, every exposure monitor traces back to "sum the P&Ls."

---

## Check-in

Does the P&L-sum model — positions → individual P&Ls → total P&L → normalise — give you a more grounded way to hold this? Or do you prefer one of the other frames?
