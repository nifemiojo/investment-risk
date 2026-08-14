# The Snapshot's Decision: Investigate or No Action

**Artifact**: Risk Snapshot
**Field**: `decision` (replaces `summary_text`)
**Date**: 2026-08-13

---

## The Decision Space

The Risk Snapshot produces exactly **two** decisions:

| Value | Meaning | Next step |
|---|---|---|
| `investigate` | Something warrants a closer look | Open Change Report + Attribution |
| `no action` | Nothing unusual today | Move on to the next portfolio |

The rule:

```python
decision = "investigate" if (is_breach or percentile_rank > 0.80) else "no action"
```

Two inputs the engine already computes, one binary output. Nothing else is needed.

---

## Why Not "Reduce Risk"?

Portfolio-level VaR is too broad to support a risk-reduction decision. To reduce
risk you need to know *what to sell* — and a single VaR number doesn't tell you
*where* the risk lives. That is attribution's job, and it lives one hop
downstream.

So the snapshot cannot honestly output "reduce risk" — it would be prescribing a
trade it has no information to size or direct. "Reduce risk" lives in the
Rebalance Recommendation, driven by drift and marginal VaR per asset. The
snapshot's job is to *route* you there, not to do the rebalance itself.

---

## Breach Folds Into "Investigate"

A breach is not a third decision. It is "investigate" with urgency attached:

- `is_breach` → **investigate** (urgency carried by the breach flag + 🚨 icon in the renderer)
- `percentile_rank > 0.80` → **investigate**
- otherwise → **no action**

The *decision* is the same word — open the next artifact and look at the
details. The breach flag changes the *tone* (do it now, notify Head of Risk),
but that tone is already encoded in `is_breach` and the compliance number. It
does not need a third decision value.

---

## The Artifact's Purpose: A Filter

The snapshot answers one question:

> *"Do I need to look at this portfolio in more detail today?"*

Yes → open Change Report + Attribution. No → move on.

That is what a PM actually does with a triage artifact across many portfolios —
they are not making allocation decisions off the morning snapshot; they are
deciding which portfolios get their scarce attention that day.

Making `decision` a first-class output (rather than leaving the numbers to
speak) makes that routing *explicit and traceable*: "investigate" because
breach, or "investigate" because 83rd percentile. A human reading "83rd
percentile" has to do the translation themselves; the field does it and makes it
auditable.

---

## The Full Loop, Correctly Scoped

```
Snapshot → investigate? ──yes──→ Change Report + Attribution
        └─ no → done                      │
                                          ▼
                                    Drift Analysis
                                          │
                                          ▼
                                    Rebalance Recommendation  ← "reduce risk" lives here
                                          │
                                          ▼
                                    Decision Record
```

The snapshot is the entry gate. It does not prescribe — it routes. And
"investigate / no action" is exactly the granularity a gate should have.

---

## What Replaced What

| Before | After |
|---|---|
| `summary_text` (prose describing state) | `decision` (routing: investigate / no action) |
| `_summarise()` — four canned sentences | `_decide()` — one binary rule |
| `percentile_meaning` (display label) | kept — it is context in the "Is This Normal?" section, not a decision |

The earlier `summary_text` wasn't just weak in wording — it was answering the
wrong question (describing state instead of routing attention). `decision`
answers the right question and nothing more.
