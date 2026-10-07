# Risk Metrics from First Principles: What the PM Actually Needs to Capture

## Start from the Mandate, Not the Metric

A PM doesn't wake up thinking "I need to monitor VaR." They wake up responsible for a portfolio that has a mandate. The mandate defines:

- **The objective** — absolute return? benchmark-relative? volatility-targeted? income?
- **The universe** — what can they hold?
- **The constraints** — leverage limits, concentration limits, drawdown limits, liquidity requirements
- **The beneficiaries** — who is this money for, and what can they tolerate?

The risk monitoring system exists to answer one question: *is this portfolio still doing what it's supposed to do, within the bounds it's supposed to do it?*

VaR answers one slice of that — "what's the worst plausible loss over the next N days?" But different mandates demand different risk lenses:

- A PM with a drawdown-averse mandate cares more about max drawdown than VaR
- A PM benchmarked to the S&P 500 cares about tracking error, not absolute volatility
- A PM running risk parity cares about whether risk is actually balanced, not whether total risk is low

The risk metric should flow from the mandate, not the other way around. We shouldn't compute numbers just because they're computable.

## What VaR Captures, and What It Misses

VaR is useful — common language, regulatorily familiar, collapses a distribution to one number. But:

| VaR doesn't tell you | Why it matters |
|---|---|
| What happens *beyond* the 5th percentile | The 1-in-20 loss might be −2%, but the 1-in-100 could be −15%. VaR is blind past its own threshold |
| Path dependency | A −15% drawdown that recovers in a week is different from grinding −15% over six months. VaR sees neither — only end-of-period returns |
| Correlation regime shifts | VaR assumes the covariance structure is stable. In stress, correlations → 1. The structural decomposition breaks exactly when you need it most |
| Liquidity | VaR says nothing about whether you can actually exit the position at the modelled loss |
| Why risk changed | VaR says "risk is up." Attribution says "SPY." Neither says "because vol spiked" vs "because correlation shifted." That's a different artifact |

## The Design Implication

The risk monitoring system shouldn't be a single-metric system. The Snapshot's VaR gate is one lens, but the PM's dashboard may ultimately need:

- **VaR** — the tail-risk headline, the gate trigger
- **Volatility + attribution** — the structural "where from" — stable, decomposable, feeds rebalancing
- **Expected shortfall (CVaR)** — what VaR leaves out; the average loss when things are worse than VaR
- **Drawdown** — the path-dependent pain metric that actually keeps PMs awake
- **Diversification ratio** — is the portfolio still doing the multi-asset job, or has it become a disguised equity bet?

This doesn't mean building everything now. The "one method, one portfolio, one loop" discipline still applies. But the *design* should name what's deliberately deferred — so the system has a place for expected shortfall or drawdown when the PM asks for it, rather than being architected around VaR as if it were the only risk question that exists.

## The First-Principles Question to Answer Before Proceeding

What is this PM's mandate? Even a simplified one — "multi-asset, absolute return, 10% annualised vol target, no single asset above 40%" — would anchor every subsequent design choice:

- The decomposition base
- The metrics in the Snapshot
- What attribution surfaces
- What rebalancing optimises toward

They all flow from the mandate.