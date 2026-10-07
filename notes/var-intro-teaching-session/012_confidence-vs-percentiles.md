# The Confidence Question: Percentiles vs. Probability

**Date:** 2026-07-03  
**Topic:** What does "95% confidence" actually mean in VaR?

---

## **Your Question (This Is the Key Insight)**

> "Just because a return is the 95th percentile return does that mean we should have 95% confidence?"

**Yes—but only under a huge assumption that often fails.**

This is where most people gloss over something critical.

---

## **What Confidence Actually Means**

### The Plain Language Definition

"95% confidence" = "I believe there's a **95% probability** that tomorrow's loss will be **no worse than this number**."

This is a **probabilistic claim about the future**, not a fact about the past.

### The Distinction

- **Empirical fact:** In the last 252 days, 95% of returns were better than X%
- **Probabilistic claim:** Tomorrow, 95% probability that return will be better than X%

These are **not the same thing** unless you make an assumption.

---

## **The Assumption That Connects Them**

### Historical VaR Logic

```
Past 252 days: 95% of returns ≥ X%
    ↓ ASSUMPTION
If these 252 days are representative of future days (same distribution)
    ↓
Then tomorrow: ~95% probability return ≥ X%
```

The assumption: **The future will draw from the same distribution as the past.**

In fancy terms: **I.I.D.** (independent, identically distributed)

- Independent: Today's return doesn't depend on yesterday's
- Identically distributed: Tomorrow's distribution = yesterday's distribution

### When This Works
- Normal markets, stable regimes, no structural breaks
- You can assume tomorrow is like yesterday

### When This Breaks
- Regime changes (bull → bear)
- Correlation breakdowns (diversifiers suddenly correlate)
- Volatility spikes (2008 GFC, 2020 COVID)
- Structural changes (new macro policy, geopolitics)

**In all these cases:** Past ≠ Future, so the confidence claim is wrong.

---

## **The Parametric Method Has the Same Problem**

### Parametric VaR Logic

```
Assume returns are Normally distributed
    ↓
Use mean + volatility to calculate Z-score
    ↓
Then: 95% confidence that tomorrow's loss ≤ X
```

### The Assumption

"Returns are normally distributed"

### When This Works
- Mostly normal markets, few tail events
- Close enough for rough estimates

### When This Breaks
- **Fat tails:** Losses are bigger and more frequent than normal predicts
- **Skew:** Downside losses are worse than upside gains
- Crisis days: Way more extreme than normal distribution allows

**Example:** 
- Normal distribution predicts biggest daily loss in 1,000 years should be ~-7%
- Black Monday 1987: -22% in one day
- 2008: Many days > -9%
- 2020 COVID crash: -12% in one day

Normal distribution is **wildly optimistic** about tail risk.

---

## **So What Does 95% Confidence Really Mean?**

It means: **"Under my model assumptions, I expect tomorrow to be in the good 95% of outcomes."**

But the question is always: **Are my assumptions right?**

### Historical Method
Assumption: "Past = Future"
- Works until it doesn't
- Misses rare events outside historical window
- Conservative in stable times, blind in crises

### Parametric Method
Assumption: "Returns are normal"
- Works until regime breaks
- Underestimates tail risk
- Very wrong during fat-tail events

---

## **The Real Insight: Confidence is Conditional**

VaR doesn't give you unconditional confidence.

It gives you **confidence conditional on your assumptions being correct.**

```
95% VaR = -1.85% means:

"IF the future is like the past (historical)
 OR returns are normally distributed (parametric)
 THEN 95% confidence loss ≤ -1.85%"
```

The big IF is doing all the work.

---

## **When They Diverge = Warning Signal**

Remember from the earlier comparison:

- **Historical VaR:** -1.85%
- **Parametric VaR:** -1.92%

They're close, so we trust both.

But if they diverged wildly (say -1.85% vs. -2.50%):

That's telling you: **"The normal distribution assumption is very wrong. History shows bigger tail losses than normal predicts."**

Translation: **"Your parametric confidence is too high. Real tail risk is worse."**

---

## **How to Think About Confidence**

### Frame 1: The Overconfident View
"VaR is 95% confidence loss = -1.85%, so I'm 95% sure I won't lose more than that."

**Wrong.** You're confusing empirical frequency with future probability.

### Frame 2: The Honest View
"VaR is 95% confidence loss = -1.85% **assuming the distribution is stable.**

If the future is like the past, I have 95% confidence.

But if the market regime changes, correlations break, or volatility spikes, all bets are off."

### Frame 3: The Production View (What Spreadex Does)
"VaR is -1.85%, so:
- Most days I'm fine
- 5% of days things get weird
- On weird days, losses could be 2x, 3x, or way worse

So I:
1. Set VaR limit as the trigger for autohedging
2. Have backup hedges for when VaR fails
3. Monitor for regime change (when methods diverge, when historical beats parametric)
4. Override the model when things smell wrong"

---

## **Key Principle**

**Confidence is only valid under your model assumptions.**

The best traders know this. They use VaR as a starting point, not an answer.

They ask:
- When is this model assumption breaking?
- When is the past not representative of the future?
- What could go wrong that VaR doesn't measure?
- Do I have hedges for tail events?

This is where VaR becomes a tool instead of a crutch.

---

## **For You at Spreadex**

When you look at VaR in the system:

1. **Ask:** What assumptions are baked in? (Historical? Parametric? Hybrid?)
2. **Check:** Do historical and parametric agree? If not, why?
3. **Think:** What's changed in the market that would break these assumptions?
4. **Plan:** If my assumptions break tomorrow, what happens? Do I have hedges?

That's dangerous-good risk thinking.

---

## **Bottom Line on Confidence**

95% confidence in VaR is not "I'm 95% sure I won't lose more."

It's "90% of the time, the model's assumptions hold, so losses stay within this range. 5% of the time, something breaks (regime shift, correlation breakdown, fat tail realized) and all bets are off."

**The real question isn't "What's my VaR?" It's "What happens when my model breaks?"**

That's what separates good risk managers from people who got blown up.

---

## **Questions to Dig In**

1. How would you detect if the past is no longer representative of the future?
2. What market events would cause historical and parametric to diverge?
3. At Spreadex, when VaR triggers a hedge, what's the assumption about regime?
4. How would you design a backup hedge for when VaR fails?

Pick one, and we go deep.
