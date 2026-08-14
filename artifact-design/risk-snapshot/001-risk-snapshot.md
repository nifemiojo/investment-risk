# Artifact Design: Risk Snapshot

**Status**: Design complete, not yet implemented  
**Date**: 2026-08-04  
**Artifact type**: Risk Snapshot  
**Answers**: "What risk is the portfolio taking right now — and am I okay?"

---

## PM Usage: The 30-Second Scan

A PM managing multiple portfolios scans each one in ~15 seconds. The Snapshot is the triage artifact. It doesn't answer "why?" — it answers "should I look?"

The PM's eyes move in this order:

```
1. Breach indicator (red/green)     ← 0.5s — binary. Red = stop everything.
2. Is This Normal? (percentile)     ← 1s   — should I be surprised?
3. Direction (up/down arrow)        ← 1s   — is this new or ongoing?
4. Budget utilisation bar           ← 2s   — how much room do I have?
5. Number itself                    ← only if something above flagged it
```

If all green → next portfolio. If red or orange → open Change Report and Attribution.

The Snapshot is a stateless function of `(portfolio, returns_data, date)`. It doesn't need yesterday's Snapshot — the Change Report handles comparison.

---

## Frequency & Triggers

The artifact type is point-in-time. Frequency is set at the edge:

| Frequency | When | Use case |
|---|---|---|
| Daily (morning) | Before market open, yesterday's close | Routine scan. "What did I walk into today?" |
| Daily (close) | After market close, today's data | End-of-day. "What am I carrying overnight?" |
| Intraday | Every 15-30 min during volatile sessions | Active monitoring. "Is the move accelerating?" |
| On demand | Before a trade, meeting, or after an event | "What does my risk look like right now?" |
| Weekly | Ahead of team meeting or IC prep | Summary view for discussion |

---

## Decisions It Enables

The Snapshot doesn't recommend action. It triggers the decision cascade:

| What the Snapshot shows | PM decision | Next step |
|---|---|---|
| Breach (utilisation ≥ 100%) | Escalate immediately | Open Change Report. Determine cause. Inform Head of Risk. Prepare for potential position reduction. |
| Elevated (percentile > 80th, no breach) | Flag for investigation | Open Change Report and Attribution. What changed? Is it concentrated? Rebalance early? |
| Normal (percentile ≤ 80th, no breach) | No action required | Move on. Next portfolio. |
| Rising rapidly (direction ↑, change_z > 2.0) | Heightened vigilance | Even at normal level, velocity matters. Fast rise from 50th to 75th percentile demands attention. |

The Snapshot also enables **alert routing** (system decision, not PM decision): breach → alert, elevated → notification, normal → silent in daily report.

---

## Business Justification

### 1. Fiduciary Evidence

The Investment Policy Statement sets risk limits. The Snapshot is the timestamped record that the PM operated within mandate — or caught breaches and escalated them. Without it, there's no evidence risk was managed. With it, every day is auditable.

### 2. Risk Budget as Scarce Resource

The PM's capacity to take new positions is `risk_budget − current_VaR`. The Snapshot's headroom number tells the PM exactly how much capacity remains. At 98% utilisation, every allocation decision is constrained. At 60%, there's room to deploy.

### 3. Early Warning — Vol Before Drawdown

Volatility expansion precedes losses. VaR rises before P&L turns negative. A PM who sees VaR climbing from £180K to £240K knows something is shifting — potentially before any position shows a loss. The Snapshot is a leading indicator of trouble.

### 4. Portfolio-Level Thinking

The Snapshot collapses multiple positions, strategies, and asset classes into one number. It forces the PM to think about the whole, not the parts. This is the difference between a trader (position-level) and a PM (portfolio-level).

### 5. Communication Currency

"How much risk are we running?" → answered in seconds. "Were you within limits during the selloff?" → the Snapshot log is the evidence. Risk is abstract; the Snapshot makes it concrete and discussable.

---

## The Display

```
╔══════════════════════════════════════════╗
║  RISK SNAPSHOT                           ║
║  60/40 Multi-Asset                      ║  ← portfolio_name
║  14 March 2022 · Close                  ║  ← timestamp + data_freshness
║  Historical VaR (95%, 252-day)           ║  ← var_method, var_confidence, var_window
╠══════════════════════════════════════════╣
║                                          ║
║  PORTFOLIO VaR                           ║
║  £218,400 / 2.18% of NAV                ║  ← var_currency, var_pct
║                                          ║
║  RISK BUDGET                             ║
║  ████████████░░░░░░░░ 82% utilised       ║  ← budget_utilisation + bar
║  ✅ Within limit (2.7% headroom)         ║  ← is_breach + headroom_pct
║                                          ║
║  IS THIS NORMAL?                          ║
║  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░ 83rd percentile     ║  ← percentile_rank + level bar
║  Today's VaR ranks at the 83rd percentile ║  ← percentile_meaning (sentence)
║  of this portfolio's own trailing VaR     ║
║  history since Jan 2019 — notably above   ║
║  this portfolio's norm, worth a look.     ║
║                                          ║
║  DIRECTION                                ║
║  ▲ Up 1.4% since yesterday               ║  ← direction, change_since_last_pct
║  (within normal daily fluctuation)        ║  ← change_label
║                                          ║
║  ─────────────────────────────────────── ║
║  Decision: → investigate                 ║  ← decision
║                                          ║
╚══════════════════════════════════════════╝
```

---

## Data Model

```python
@dataclass(frozen=True)
class RiskSnapshot:
    """Point-in-time risk measurement with distributional context."""

    # === Identity ===
    portfolio_name: str
    timestamp: str                    # "2022-03-14T16:30:00"
    data_freshness: str               # "Close" | "Intraday-14:30"
    var_method: str                   # "Historical" | "Parametric" | "Monte Carlo"
    var_confidence: float             # 0.95
    var_window: int                   # 252

    # === Core Measurement ===
    var_currency: float               # 218_400
    var_pct: float                    # 0.0218 (daily)
    var_annualised_pct: float         # 0.176 (daily × √252)
    nav: float                        # 10_000_000 — Net Asset Value

    # === Budget Comparison ===
    risk_budget_annual_pct: float     # 0.15 (annualised VaR limit at 95% confidence)
    risk_budget_currency: float       # 1_500_000
    budget_utilisation: float         # 0.82
    is_breach: bool                   # utilisation >= 1.0
    headroom_pct: float               # 0.027 (negative if breach)
    headroom_currency: float          # 270_000

    # === Distributional Context ===
    percentile_rank: float              # 0.78
    percentile_meaning: str             # "lighter than usual for this portfolio" | "about average for this portfolio" | "notably above this portfolio's norm, worth a look" | "unusually high for this portfolio, investigate" | "far beyond this portfolio's norm, escalate"
    level_thresholds: dict[str, float]  # {"elevated": 0.80, "high": 0.90, "extreme": 0.95}
    distribution_lookback_start: str    # "2019-01-02" — first date of the VaR history the percentile ranks against

    # === Direction (since last check) ===
    change_since_last_pct: float | None     # 0.014 (None if no prior snapshot exists)
    change_since_last_currency: float | None
    direction: str                          # "up" | "down" | "flat" | "first_snapshot"
    change_label: str                       # "within normal range" | "notable" | "significant" | "first_snapshot"

    # === Decision ===
    decision: str                     # "investigate" | "no action" — the snapshot's single routing output
```

---

## Design Decisions

| Decision | Rationale |
|---|---|
| `data_freshness` stored explicitly | A Snapshot at 2:30pm using 2:15pm prices is different from one using yesterday's close. The PM needs to know which they're looking at. |
| `risk_budget_currency` alongside `risk_budget_annual_pct` | PM thinks in currency. Budget is set in percentage. Both views needed. |
| `headroom_pct` and `headroom_currency` | Not just "within budget" — *how much* room. Actionable capacity number. |
| `level_thresholds` stored on the Snapshot | Makes `percentile_meaning` auditable. If thresholds change later, historical Snapshots still know what rules produced their labels. |
| `distribution_lookback_start` stored | Percentile rank means nothing without the reference window. "78th percentile since 2019" vs. "since last month" are different contexts. |
| `change_since_last` included but minimal | Single delta + label for the quick scan. A PM who wants to understand the change opens the Change Report. The Snapshot just says "is it moving?" |
| `decision` is a routing output, not prose | `investigate` if breach or percentile > 80th, else `no action`. The snapshot decides whether to look closer, not what state things are in. |
| `change_since_last` can be `None` | The first Snapshot for a portfolio has no prior Snapshot to compare against. |
| Frozen dataclass | Immutable once computed. No accidental mutation in display code. |

---

## What the Snapshot Does NOT Include

These are deliberate exclusions — separate artifacts:

| Excluded | Where it lives | Rationale |
|---|---|---|
| Per-asset contribution | Attribution | Different question: "where from?" |
| Correlation shifts | Diversification Monitor or Change Report | Detail that doesn't help the "am I okay?" scan |
| Historical VaR chart | Companion visualization, not the artifact | The percentile rank captures historical context in one number |
| Trade recommendations | Rebalance Recommendation | Observes, doesn't prescribe |
| Breach history | Decision Journal or Breach Log | About today, not history |

---

## Edge Cases

| Scenario | How the model handles it |
|---|---|
| Breach in progress | `is_breach = True`, `headroom_pct` is negative, `decision = "investigate"` (the breach flag carries the escalation urgency) |
| Portfolio weights changed mid-day | Uses current weights. Snapshot of whatever state existed at that moment. |
| Missing price data | Engine raises error. No partial snapshots. |
| Multiple VaR methods | Separate Snapshot instances per method. Comparison is a different artifact. |
| First Snapshot (no prior for change) | `change_since_last = None`, `direction = "first_snapshot"`, `change_label = "first_snapshot"` |