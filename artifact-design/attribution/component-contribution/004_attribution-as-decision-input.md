# Attribution as a Decision Input: Feeding the Rebalancing Pipeline

## The Principle

The decomposition base isn't a math question — it's a utility question. The test is: *does the ranking it produces lead to better rebalancing decisions?*

Attribution sits between the Snapshot (gate: "investigate?") and the downstream pipeline (drift analysis → rebalancing). Its output — a ranking — is the input to the PM's next question: "OK, this asset is the biggest risk driver. Should I reduce it, and by how much?"

## Two Rankings, Two Downstream Effects

Consider the PM seeing both decomposition approaches for the same portfolio:

| | Single-day forensic (VaR day) | Covariance-based structural |
|---|---|---|
| **SPY** | 42% | 61% |
| **EFA** | 28% | 33% |
| **IEF** | +5% (positive — it fell too) | −1% (negative — it offset) |
| **GLD** | −15% (rallied hard) | 7% |

The forensic view says IEF *contributed* to the loss on that specific day — because on that day, everything fell together. The structural view says IEF *reduces* risk systematically — because over the full window, it's negatively correlated with equities.

If the PM acts on the forensic view, they cut IEF — destroying the hedge that works 95% of the time. That's a bad rebalancing decision driven by a noisy signal.

The structural view protects the PM from overfitting to one day's idiosyncratic co-movement. It says: "IEF is doing its job — leave it alone, look at SPY." That's the ranking that feeds a sensible rebalancing conversation.

## What Attribution Needs to Provide

The PM's natural thought progression after seeing the ranking:

1. "SPY is the biggest risk driver" → **component contribution (CTR)** — the ranking itself
2. "What if I reduce it?" → **marginal contribution (MCTR)** — the sensitivity

CTR answers "where is the risk?" MCTR answers "how much does risk move if I act?" Both are needed to bridge from attribution to rebalancing.

The 001 document parked MCTR in the Rebalance artifact, which is clean from a taxonomy perspective. But there's a practical argument for surfacing it alongside the CTR ranking — because the PM's natural next thought after seeing the ranking is "what if I change it?" Having the sensitivity in the same view shortens the loop from insight to action.

Whether MCTR lives in the Attribution display or only in Rebalancing is a presentation choice — the computation is the same. The architectural principle is: compute it once, display it where the PM needs it to make the next decision.

## Design Criteria for the Decomposition Base

The decomposition base should be chosen so that the ranking is:

1. **Stable enough to act on** — doesn't jump when the VaR day changes with one new data point
2. **Reflects persistent relationships, not one-off events** — IEF's hedging property should show, not be masked by a day where correlations broke
3. **Feeds naturally into the rebalancing calculus** — the same covariance structure that produces the ranking also produces the MCTR sensitivities that size the trades

Covariance-based decomposition wins on all three. The single-day forensic breakdown is a useful diagnostic overlay — valuable for understanding a specific stress event — but it should not drive portfolio changes.