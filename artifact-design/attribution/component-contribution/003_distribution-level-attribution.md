# Distribution-Level Attribution: Resolving the Decomposition Base

## The Two Paths

The question starts from a simple observation: if historical VaR is the 5th percentile of portfolio returns — a specific day in the lookback — then isn't the contribution just the asset return breakdown on that day?

From there, two paths emerge:

**Path 1 — single-day forensic decomposition:**
VaR is the 5th percentile day → contribution is $w_i \times r_i(\text{that day})$ → additive, mechanically correct, corresponds to a real historical event. Valid arithmetic, wrong question.

**Path 2 — distribution-level structural decomposition:**
VaR is a statement about the *distribution* (the 5th percentile is a property of the whole return series, not just one day) → attribution should also be a distribution-level answer → covariance-based decomposition. This is where design tension D (from 001) pointed.

## The Pivot

VaR isn't really about the observation on that day — it's about the shape of the tail. That day is just the measurement instrument. Decomposing the day rather than the distribution answers a question the PM didn't ask: "what was this loss made of" (forensic, backward-looking) rather than "where does my risk come from" (structural, forward-looking). The PM needs the second one.

The PM doesn't care which specific day hit the 5th percentile. They care about which assets *systematically* drive the portfolio's downside risk, given how everything moves together. That's a covariance question, not a single-day question.

## Reconciling the Two Decomposition Bases

This resolves design tension D from 001_attribution-thinking.md: the Snapshot produces a historical VaR number that isn't cleanly decomposable, but the PM needs a "where from" answer that *is* additive.

| What | Which base | Why |
|---|---|---|
| The PM reads | % contribution ranking | Unit-invariant — same whether from vol, variance, or parametric VaR |
| The £ number | Parametric VaR = $z_\alpha \times \sigma_p$ | Additive; components sum to the total |
| The honest note | "£ uses parametric VaR (normal assumption); the Snapshot's headline uses historical VaR — direction agrees, £ may differ modestly" | Names the gap rather than papering over it |

The key insight: the **ranking** — which is what the PM actually uses to decide where to look — is robust. The % contributions are identical whether you decompose volatility, variance, or parametric VaR (they differ only by a scaling factor that cancels in normalisation). The £ mismatch between parametric and historical VaR is a reconciliation footnote, not a design flaw.

## Connection to Design Tension D

From 001:

> The Snapshot's headline number is **historical VaR** — an empirical quantile of the portfolio's own return series. Historical VaR is *not additively decomposable*; there's no clean "component historical VaR". Component contribution is fundamentally a **covariance/volatility** concept. So attribution can't decompose the exact number the Snapshot produces.

This tension is now resolved by:
1. Accepting that the decomposition base is covariance/volatility — the distribution-level answer
2. Scaling to parametric VaR for £ figures
3. Documenting the reconciliation gap honestly rather than forcing a match
4. Recognising that the % ranking — the PM's actual decision input — is unaffected by which base is used