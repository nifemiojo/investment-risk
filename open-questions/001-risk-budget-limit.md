# Q001 — How is the risk budget / limit decided?

**Status**: open
**Raised**: 2026-08-14

## The Question

The system currently takes the risk budget (the limit that VaR utilisation is measured against) as **input — pre-decided, external to the system**. The question is: *where does that number come from, and who decides it?*

## Why It Matters

The budget is the reference point every monitoring artifact compares against. If the system treats it as given, it can't reason about whether the budget itself is appropriate — and that judgement lives in the governance layer *above* monitoring (investment policy statement, mandate, client risk tolerance, drawdown constraints). Understanding what sits outside the system clarifies what the system is *for* and where its boundary is.