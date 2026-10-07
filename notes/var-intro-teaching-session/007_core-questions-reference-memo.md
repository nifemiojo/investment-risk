# 10 Core Questions — Interview Reference Memo

**You should be able to answer all 10 from memory (no notes, 30 minutes max).**

Use this for interview prep. If you can nail these, you understand VaR at dangerous-good level.

---

## Q1: What is VaR? (Explain in 60 seconds)

### Your Answer Should Include:
- Definition (percentile of losses)
- Confidence level (95% = worst 5%)
- Dollar vs. percentage
- What it does NOT tell you

### Sample Answer:
"Value at Risk is a percentile measure of portfolio losses. It answers: 'What's the worst loss I'd experience on a really bad day?' 

Specifically, VaR at 95% confidence means: on 95% of normal trading days, my portfolio won't lose more than X. On 1-in-20 bad days, it will.

For example, a $10M portfolio with 95% VaR of -$85K means that on typical days, I lose at most ~0.85%. But 5% of the time, I lose more.

Important: VaR does NOT tell you the maximum loss. It's just a percentile. In a crisis, losses could be 10x worse."

---

## Q2: Explain the two main ways to calculate VaR

### Your Answer Should Cover:

**Historical Method:**
- Sort past returns
- Find the percentile
- Example: Worst 5%
- Pros: No assumptions
- Cons: Can't predict worse than history

**Parametric Method:**
- Assume normal distribution
- Use formula: Mean - (Z-score × Vol)
- Pros: Estimates tail beyond history
- Cons: Often wrong in crises

### Sample Answer:
"There are two main approaches.

**Historical:** Just take past returns, sort them, and grab the percentile. If I want 95% VaR, I find the 5th worst day out of 252 days. Simple, honest, based on reality. Problem: If markets crash worse than any day I've seen, I won't know it.

**Parametric:** Assume returns follow a bell curve. Then use the normal distribution formula to calculate the percentile. For 95% confidence, that's Mean minus 1.645 times the volatility. Problem: Returns don't follow bell curves, especially in stress scenarios."

---

## Q3: When do historical and parametric VaR diverge? Why?

### Your Answer Should Explain:
- Fat tails (crashes happen more often than normal predicts)
- Skewness (asymmetric risk, more downs than ups)
- Kurtosis (extreme probability in tails)
- Regime changes (old patterns break)

### Sample Answer:
"They diverge when the normal distribution assumption breaks down.

Real returns have fat tails—extreme events happen more than a bell curve predicts. They're also often negatively skewed (more crash risk than boom risk, especially for stocks). This means parametric VaR often *underestimates* tail risk.

Also, regime changes. During normal times, bonds hedge stocks. During a crisis, they crash together. Historical VaR adapts immediately. Parametric lags.

The bigger the divergence, the more you should trust historical and dig into why the environment changed."

---

## Q4: What does 95% confidence actually mean?

### Your Answer Should Clarify:
- NOT "95% worst-case"
- IS "5th percentile of losses"
- Timing: "One in 20 days"
- What 99% and 90% mean differently

### Sample Answer:
"95% confidence means the 5th percentile. Out of 20 trading days, 19 are OK (you lose less than VaR). On day 20, you lose more.

It does NOT mean '95% chance this is the worst.' It means: 'I looked at all historical days, sorted them by loss, and found the 5th worst.'

90% confidence would be: 1 in 10 days, so more often you hit the limit.
99% confidence would be: 1 in 100 days, so you rarely hit it but when you do, it's much worse."

---

## Q5: Why is a portfolio's VaR often lower than the weighted average of individual VaRs?

### Your Answer Should Include:
- Diversification
- Correlation < 1
- Bad days don't align
- Example: 60/40

### Sample Answer:
"Diversification. When stock VaR is -1.3% and bond VaR is -0.4%, the portfolio VaR might be -0.85%, which is better than the average.

Why? Because on days stocks crash, bonds often survive. On days bonds suffer, stocks often do OK. The worst days for each asset class don't align perfectly. So when I mix them, the portfolio's worst day isn't as bad as either individual asset's worst day.

This only works if correlation < 1. If stocks and bonds always move together, diversification fails."

---

## Q6: When is VaR dangerously wrong?

### Your Answer Should List:
- Tail events (2008, COVID, 2022)
- Correlation breakdowns
- Regime shifts
- Feedback loops (hedging cascades)

### Sample Answer:
"In stress scenarios. VaR is built on historical data and normal-time correlations. When:

1. **New crashes:** 2008 and 2020 both had crashes worse than any day in previous years. Traders relying on historical VaR got wiped out.

2. **Correlation breakdown:** In 2022, stocks AND bonds crashed together. The 60/40 'diversification' failed. Traders who relied on correlation = 0.5 got crushed.

3. **Feedback loops:** If everyone's VaR tells them to hedge at the same time, you get a cascade—hedging causes prices to move, triggering more hedges. VaR can't see this.

4. **Regime change:** If market regime changes (volatility spikes, new correlations), yesterday's VaR is obsolete."

---

## Q7: What's the key assumption in parametric VaR? When does it break?

### Your Answer Should Cover:
- Normal distribution assumption
- Bell curve shape
- When real returns deviate
- How to test (Shapiro-Wilk, skewness, kurtosis)

### Sample Answer:
"Parametric assumes returns follow a perfect bell curve—symmetric, thin tails, no extreme outliers.

This breaks almost constantly. Real returns:
- Have negative skew (more crashes than booms)
- Have fat tails (more extreme days than curve predicts)
- Have regime shifts (bull market vs. bear market)

You can test this. Run a Shapiro-Wilk test (p-value > 0.05 = normal). Check skewness (0 = symmetric, negative = left tail fat). Check kurtosis (0 = normal, positive = fatter tails).

If these fail, parametric is lying to you."

---

## Q8: How would you validate VaR against production data?

### Your Answer Should Outline:
- Pick a live position at Spreadex
- Calculate VaR using your method
- Compare to system
- Debug differences
- Repeat with different portfolios

### Sample Answer:
"I'd:

1. Pick a live client position at Spreadex—say, their equity book.
2. Get the position data (tickers, sizes, dates).
3. Run my VaR calculator (both historical and parametric).
4. Compare my results to what Spreadex's system shows.
5. If they match ± 1-2%, we're solid.
6. If they diverge, debug: Am I using the same lookback period? Same confidence level? Same weighting? Same data source?
7. Once one matches, try another position (bonds, FX, mixed).
8. Once confident on multiple positions, I'd then look for edge cases (tail events, regime changes)."

---

## Q9: At Spreadex, where does VaR integrate? Give me three use cases.

### Your Answer Should Show:
- You've thought about real application
- Autohedging triggers
- Margin requirements
- Spread pricing

### Sample Answer:
"Three key places:

1. **Autohedge triggers:** When a client's portfolio VaR exceeds a threshold (say $500K), our system auto-hedges their position to de-risk. VaR accuracy here is critical—if we underestimate, we don't hedge enough and lose money.

2. **Margin requirements:** We tell clients: 'Your portfolio's daily VaR is $X, so you need $X as margin.' This is how we manage our credit risk with them.

3. **Quote pricing:** When a client asks for a price, we quote based on risk. Higher VaR = wider spread (more risk = we charge more). If VaR is wrong, our spreads are wrong and we take bad trades."

---

## Q10: What would you do differently if you were building VaR from scratch today?

### Your Answer Should Show:
- Critical thinking
- Limitations awareness
- Practical engineering
- Career ambition

### Sample Answer:
"I'd probably:

1. **Use historical as baseline**, not parametric. It's simpler, more honest, less assumptions.

2. **Add granularity:** VaR for single day is nice, but I'd also calculate 10-day VaR, stress VaR, and scenario VaR.

3. **Build in diagnostics:** Automatically compare historical vs. parametric. When they diverge by >10%, flag it. When skewness spikes >0.5, flag it. These are warning signals.

4. **Add feedback loops:** Monitor VaR accuracy. Backtest: Did the 95th percentile actually occur 5% of the time? If not, the model is miscalibrated.

5. **Build for regime detection:** Automatically detect when correlations change, volatility regime shifts. Alert on regime change.

6. **Layer in scenarios:** Not just VaR, but 'what if' stress tests. What if VIX spikes 50%? What if credit spreads widen 200bps?

That's dangerous-good level: not just calculate VaR, but know when it's wrong and what to do about it."

---

## How to Use This

1. **Print this page or save to phone**
2. **This week:** Read all 10 questions
3. **Next week:** Answer each from memory (no notes)
4. **Interview:** You should nail all 10 in <30 minutes, confident, no stumbling

If you can do that, you're interview-ready on VaR.

---

## What "Good" Looks Like

✅ **Not reading off answers** (you're explaining with your own examples)
✅ **Connecting to Spreadex** (showing you've thought about application)
✅ **Admitting limitations** (VaR is useful but imperfect)
✅ **Building mentally** (moving from concept to models to practice)
✅ **Being specific** (numbers, methods, concrete examples)

That's how you nail interviews at AQR/Bridgewater.
