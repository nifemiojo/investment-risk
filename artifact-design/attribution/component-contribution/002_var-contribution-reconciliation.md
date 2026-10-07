# VaR Contribution: Realized vs Structural

## The Observation

If VaR is just a portfolio return observation on a particular day (e.g., the 5th percentile of the historical return distribution), then isn't the contribution just the breakdown of the return contribution on that day?

Historical VaR at the 5th percentile: sort all daily portfolio returns in the lookback window, take the 5th percentile. That's a specific day $d$ in your history, and on that day:

$$r_p(d) = \sum_i w_i \, r_i(d)$$

So mechanically:

$$\text{contribution}_i = w_i \times r_i(d)$$

These sum exactly to $\text{VaR}_\alpha$. It's additive, it's trivially computable, and it corresponds to a real historical event you can point at and say "this is what happened." In the most literal sense, the VaR contribution *is* the return contribution on the VaR day.

## So why doesn't everyone do this?

Three reasons, and they each illuminate something about what risk contribution is *for*:

### 1. The VaR day is unstable

Add one more data point to the window and the VaR day can jump — today it's the COVID crash (March 16 2020), tomorrow it's the taper tantrum (June 2013). The contribution picture flips completely, not because anything about the portfolio changed, but because the quantile slipped. A PM looking at this every morning would see noise, not signal.

The covariance-based decomposition uses the **full distribution** — all 252 days contribute to the covariance estimate — so it changes smoothly as new data arrives. The ranking (SPY first, EFA second) is stable.

### 2. Realized ≠ structural

The single-day decomposition answers: "What happened on that specific day?"  
The covariance decomposition answers: "Which assets *systematically* drive risk, given how they move together?"

These are different questions. On the VaR day, GLD might have had a particularly bad day alongside equities — but if GLD is normally *uncorrelated* with equities, that day's contribution overstates its structural role. The covariance approach credits GLD only for its persistent relationship with the portfolio, not an anomalous co-move on one day.

It's the difference between "what was this loss made of" (forensic, backward-looking) and "where does my risk come from" (structural, forward-looking). The PM needs the second one.

### 3. The covariance approach unifies volatility and VaR

Under normality (or any elliptical distribution), $\text{VaR}_\alpha = z_\alpha \times \sigma_p$, and contribution scales proportionally:

$$\text{Component VaR}_i = z_\alpha \times \text{Component Vol}_i$$

The pieces still sum, the ranking is identical, and the same decomposition serves both metrics. This is the standard approach because it gives one consistent "where is the risk" answer regardless of which headline number you're looking at.

For historical simulation specifically, the single-day decomposition *is* a valid alternative — and some systems show it alongside the structural one. But it answers a narrower question.

---

## The Bridge

The previous artifact (001) decomposed *volatility*, but the snapshot's headline is *historical VaR* — so the next step is to pin down whether (and how) the £ figures reconcile.

The user's question is essentially that reconciliation, worked from the other direction: if VaR is just a day, why isn't contribution just the day's breakdown? The answer — that structural and realized contributions are different things, and the PM needs both — is the design tension the next artifact should address.

### Implications for the system design

- The **structural** (covariance-based) decomposition is the default "where is my risk" view — stable, forward-looking, unified across volatility and VaR.
- The **realized** (VaR-day) decomposition is a diagnostic overlay — "what actually happened on my worst day" — useful for scenario analysis and forensic review.
- Both are additive (sum to the total) and both are computable from the same returns matrix and weights.
- The system should present the structural view prominently and offer the realized breakdown as a drill-down on the VaR day.