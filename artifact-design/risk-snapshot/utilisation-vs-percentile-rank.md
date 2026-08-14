# Two Risk Metrics, Two Different Questions

**Artifact**: Risk Snapshot  
**Fields**: `budget_utilisation`, `percentile_rank`, `percentile_meaning`  
**Date**: 2026-08-08

---

## The Core Distinction

The Snapshot contains two numbers that look at the same VaR but answer fundamentally different questions:

| | Budget utilisation | Percentile rank |
|---|---|---|
| **Question** | "Am I compliant?" | "Should I be surprised?" |
| **Reference frame** | The IPS — contractual, external | The portfolio's own history — internal |
| **Audience** | Client, IC, regulator | PM, Head of Risk |
| **Consequence of high value** | Formal breach protocol | Investigation, judgment call |
| **Action verb** | Escalate | Investigate |

They are correlated but not redundant. Conflating them would be a design error.

---

## Budget Utilisation

### What it is

$$ \text{utilisation} = \frac{\text{VaR}_{\text{annualised}}}{\text{risk\_budget}} $$

The annualised VaR divided by the risk budget set in the Investment Policy Statement. A percentage of a contractual limit.

### Where it comes from

The risk budget flows from governance: Client Mandate → IPS → PM. The PM didn't choose 15% — the client's risk tolerance, filtered through the IPS, produced it. The PM's job is to deploy that 15% efficiently.

### Question it answers

> *"Am I operating within the terms of my mandate?"*

This is a **fiduciary** question. It doesn't ask whether the risk level is appropriate — it asks whether it's permitted.

### Decision it enables

| Utilisation | Decision |
|---|---|
| ≤ 80% | Deploy freely. Headroom exists for new positions. |
| 80–95% | Capacity-constrained. Any new position needs a corresponding reduction elsewhere. |
| 95–100% | Approaching the limit. Active management of risk budget required. |
| > 100% | **Breach.** Formal protocol: notify IC, reduce positions or request override, document. |

### Who it's for

- **IC / Governance**: "Were you within mandate?"
- **Client / Regulator**: "Was our capital managed within agreed limits?"
- **PM (action mode)**: "Can I add this position?"

The utilisation history IS the governance record. It answers the audit question: *"Did the PM operate within the fiduciary contract?"*

---

## Percentile Rank

### What it is

$$ \text{percentile\_rank} = P(\text{VaR}_{\text{historical}} < \text{VaR}_{\text{current}}) $$

The fraction of historical VaR observations (from rolling windows over the portfolio's own return history) that were lower than today's VaR. A measure of where today's risk sits in the portfolio's own distribution.

### Where it comes from

The portfolio's own return history. A rolling VaR time series is computed, and today's VaR is ranked within that distribution. The reference window matters — "78th percentile since 2019" is different from "78th percentile since last month."

### Question it answers

> *"Is this level of risk normal for me?"*

This is a **calibration** question. It doesn't ask whether the risk is permitted — it asks whether it's unusual given the portfolio's own track record.

### Decision it enables

| Percentile | Meaning | Decision |
|---|---|---|
| < 50th | `lighter than usual for this portfolio` | Running light. Not surprised — but IC may ask: "are you deploying the budget?" |
| 50–80th | `about average for this portfolio` | Not surprised. Move on. |
| 80–90th | `notably above this portfolio's norm, worth a look` | Surprised. Open the Change Report. |
| 90–95th | `unusually high for this portfolio, investigate` | Very surprised. Something has probably shifted. Investigate. |
| > 95th | `far beyond this portfolio's norm, escalate` | Alarmed. Escalation-worthy, even without a breach. |

The meaning encodes both the surprise level and the decision. The PM doesn't translate "0.87" → "is that high?" — they read "notably above this portfolio's norm, worth a look" and know what to do.

### Who it's for

- **PM (scan mode)**: "Which portfolios do I look at first?"
- **Head of Risk**: "Which PMs are operating outside their normal range?"
- **PM (retrospective)**: "Has my risk-taking behaviour changed over time?"

The percentile history answers: *"Is this PM taking more risk than they used to — and is that a deliberate strategy shift or drift?"*

---

## Why You Need Both

### Scenario 1: High utilisation, low percentile

> Portfolio is at 92% utilisation (near the limit) but 30th percentile.

**Interpretation**: You're close to your limit, but that's *normal for you* — you've always run near the limit. You're capacity-constrained but not surprised. The utilisation tells you "be careful." The percentile tells you "this isn't unusual — no need to investigate *why* risk is high, because it's always high." The mandate might be calibrated too tight, or the PM runs an aggressive strategy within a tight budget. Either way, the IC conversation is about the budget, not the PM's behaviour.

### Scenario 2: Low utilisation, high percentile

> Portfolio is at 65% utilisation (plenty of headroom) but 92nd percentile.

**Interpretation**: You're well within your limit, but this is unusually high risk *for you*. Something has changed — a new position, a correlation breakdown, a strategy drift. The utilisation says "fine, move on." The percentile says "stop, something is different." This is the early warning that the utilisation number alone would miss.

The PM who ignores the percentile in this scenario is the PM who gets blindsided when the unusual becomes the new normal — and utilisation hits 100% two weeks later.

### Scenario 3: High utilisation, high percentile

> Portfolio is at 98% utilisation and 97th percentile.

**Interpretation**: Both numbers are screaming. You're near breach AND this is extremely unusual for you. Something has gone wrong. The breach protocol AND the investigation need to happen simultaneously. This is not a routine near-limit situation — it's a crisis.

### Scenario 4: Low utilisation, low percentile

> Portfolio is at 45% utilisation and 20th percentile.

**Interpretation**: You're running light and that's normal for you (or you're even lighter than usual). Both numbers agree: nothing to see here. But the IC might ask: *"You're consistently at 20th percentile of your own risk-taking — are you deploying the budget the client gave you?"*

---

## The Summary Table

| | Budget utilisation | Percentile rank |
|---|---|---|
| **Computation** | VaR ÷ risk budget | rank(VaR in historical VaRs) |
| **Source of reference** | IPS (external, contractual) | Portfolio returns (internal, empirical) |
| **Answers** | Am I compliant? | Should I be surprised? |
| **For** | IC, client, regulator | PM, Head of Risk |
| **High =** | Breach protocol | Investigation |
| **Low =** | Room to deploy | Nothing unusual |
| **History answers** | Was the PM within mandate? | Has the PM's risk-taking changed? |
| **Failure mode if ignored** | Breach without response | Surprise without warning |

---

## Design Principle

> **Budget utilisation is the governance metric. Percentile rank is the calibration metric. One proves you followed the rules. The other tells you whether the rules need attention.**

The Snapshot shows both because a PM who only sees one is flying with one eye closed. Utilisation alone can't warn you that something unusual is brewing. Percentile alone can't tell you if you've crossed a fiduciary line. Together, they answer the two questions every PM asks before anything else: *"Am I okay?"* and *"Is this normal?"*