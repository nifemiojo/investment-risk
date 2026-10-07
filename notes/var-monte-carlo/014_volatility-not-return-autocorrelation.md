# Returns vs Volatility: What GARCH Actually Models

**Date:** 2026-07-10
**Topic:** GARCH models volatility autocorrelation, not return autocorrelation — the distinction you just identified

---

## Your Insight, Made Explicit

You said:

> "It is volatility that is being modelled as autocorrelated here not returns."

Exactly right. And this is easy to confuse because both involve $r_{t-1}$ showing up in an equation for $r_t$. Let me separate them clearly.

---

## Two Different Kinds of Dependence

### Return Autocorrelation: Direction Predicts Direction

$$r_t = \phi \cdot r_{t-1} + \epsilon_t$$

**Terms:**
- $\phi$: if positive, yesterday's direction predicts today's direction (momentum). If negative, yesterday's direction predicts reversal (mean reversion).

If $\phi = 0.2$:
- Yesterday +2% → today biased positive (+0.4% expected)
- Yesterday −2% → today biased negative (−0.4% expected)

This says: **"What goes up tends to keep going up."** (or down, if φ < 0). It's about the **sign** of the return.

### Volatility Clustering (GARCH): Magnitude Predicts Magnitude

$$r_t = \mu + \sigma_t \cdot z_t, \quad \sigma_t^2 = \omega + \alpha \cdot r_{t-1}^2 + \beta \cdot \sigma_{t-1}^2$$

GARCH makes **no prediction about the sign of $r_t$.** The $z_t$ term is symmetric — equally likely to be positive or negative.

What GARCH predicts: the **width** of the distribution around zero.

- Yesterday +5% → today's σ is wide → big moves in EITHER direction are more likely
- Yesterday −5% → today's σ is wide → same
- Yesterday +0.1% → today's σ is narrow → small moves are more likely

This says: **"After a storm, expect more storms — but you don't know which way the wind will blow."**

---

## Visual Intuition

Imagine the distribution of tomorrow's return as a bell curve centered at zero.

**After a calm day ($r_{t-1} \approx 0$):**

```
        narrow distribution
        ______
       /      \
      /        \
  ---+----------+---
    -2%    0   +2%
```

Small σ. Tomorrow's return will probably be small.

**After a crash ($r_{t-1} = -5\%$):**

```
        wide distribution
       _            _
      / \          / \
     /   \        /   \
  ---+--------------+---
    -4%    0      +4%
```

Large σ. Tomorrow's return could easily be +4% or −4%. The model doesn't know which — it just knows the range is wider.

**After a rally ($r_{t-1} = +5\%$):** Exactly the same wide distribution. The model treats +5% and −5% identically.

---

## Is There Evidence for Return Autocorrelation?

You asked this implicitly. The answer: **very little at daily frequency for liquid markets.**

- **Daily equity returns:** Autocorrelation is near zero. Yesterday's direction tells you almost nothing about today's direction. (At very short horizons — minutes — there can be momentum. At very long horizons — years — there's mean reversion. Daily is the "no man's land" for return predictability.)
- **Daily volatility:** Strong autocorrelation. Yesterday's magnitude strongly predicts today's magnitude. This is one of the most robust empirical facts in financial econometrics.

This is why GARCH is so useful: it models the thing that actually has structure (volatility) while leaving the thing that's essentially random (direction) as random.

---

## The Misconception You Avoided

A common mistake: hearing "yesterday's return affects today" and thinking GARCH is about momentum or trend. It's not. It's about:

> **"Big moves beget big moves, but the direction of the next move is a coin flip."**

---

## Why This Matters for Monte Carlo VaR

Parametric VaR says: "Tomorrow's distribution is always the same width. VaR is the same every day."

GARCH says: "Tomorrow's distribution is wider after a shock. VaR is HIGHER after a crash."

Monte Carlo with GARCH simulates this: the simulated paths show periods where VaR is elevated (after shocks) and periods where it's low (during calm). You can answer: **"Given what happened yesterday, what's my risk today?"** rather than just **"What's my average risk?"**

---

## Check-In

Your mental model is correct: GARCH captures volatility autocorrelation, not return autocorrelation. After a big shock, the distribution widens, making another big shock more likely — but in *either* direction.

Does this distinction feel solid? And do you see why this matters operationally? After a crash, a risk manager using parametric VaR sees the same limit as yesterday. A risk manager using GARCH-informed Monte Carlo sees a wider limit — and might reduce positions or increase hedges accordingly.