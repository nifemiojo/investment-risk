# V1 Vertical Slice: Portfolio Risk Monitoring → Investigation Trigger

**Status**: Plan agreed, not yet implemented  
**Date**: 2026-08-02

---

## Strategic Frame

- **Home**: Portfolio Monitoring, feeding the Investment Committee
- **Flow**: Measure → Context → Attribute → Detect Change → Interpret → Flag
- **Stance**: Builder who validates the system by operating as PM — point-in-time decisions, no look-ahead, honest tracking of outcomes
- **This is the evolution of the historical-VaR project into the flagship**

---

## The Workflow Loop

```
PORTFOLIO MONITORING          PM DECISION
═══════════════════           ═══════════

Daily Risk Brief ──────────→  "Do I need to investigate?"
                                  YES → Drill into attribution/run scenarios
                                  NO  → File, move on
```

---

## V1 Portfolio

| Asset | Ticker | Allocation | Role |
|---|---|---|---|
| US Equities | SPY | 40% | Growth engine |
| International Equities | EFA | 20% | Equity diversification |
| US Treasuries (7-10yr) | IEF | 25% | Duration / deflation hedge |
| Gold | GLD | 15% | Crisis hedge / inflation diversifier |

**Notional**: £10M  
**Risk budget**: 15% annualized VaR at 95% confidence  
**Method**: Historical VaR, 252-day lookback, positive loss convention

---

## Decisions the Risk Brief Enables

| Decision | Provided by | Threshold |
|---|---|---|
| Is risk within budget? | Portfolio VaR vs. limit | Hard limit (15%) |
| Has risk changed meaningfully? | Z-score of VaR change vs. historical change distribution | \|z\| > 1.5 notable, > 2.0 significant |
| Where is the change coming from? | Asset-level incremental VaR changes | Which asset contribution changed most? |
| Is diversification holding up? | Diversification ratio vs. its own distribution | Below 25th percentile → warning |
| Is this normal? | VaR percentile rank in trailing 3-year distribution | >80th elevated, >90th high, >95th extreme |

---

## Artifacts

### Primary: Daily Risk Brief
- VaR today (£ and %), vs. risk budget (utilisation bar)
- Change since last month (£, %, z-score)
- Attribution: per-asset contribution (incremental VaR), % share, direction of change
- Diversification ratio with plain-language interpretation
- Percentile rank in historical distribution
- Bottom-line summary (2-3 sentences)
- Flag if any threshold is crossed

### Secondary: Diversification Monitor
- Produced when diversification ratio crosses below threshold
- Correlation breakdown (which pairs are shifting)
- Implication for portfolio behaviour
- Historical analogues

### Meta: Decision Journal
- Produced after full historical replay
- What was flagged, when, was it right, what would improve the system
- Demonstrates understanding of methodology limits

---

## Historical Replay

- **Period**: Jan 2020 – Dec 2024 (~1,256 trading days)
- **Warm-up**: First 252 days (no briefs produced)
- **Active**: Apr 2021 – Dec 2024 (~940 daily briefs)
- **Constraint**: Point-in-time — each brief sees only data up to that date

---

## Bottom-Up: Build Plan

### Reused from existing codebase
- `historical_var()` — core VaR calculation
- `rolling_var()` — VaR time series, breach tracking
- `weighted_quantile()` — available for future decay-weighted methods

### New to build
1. Portfolio constructor: weighted return series from 4 assets
2. Incremental VaR: loop existing function, remove each asset in turn
3. Diversification ratio: arithmetic on standalone + portfolio VaR
4. Change detector: z-score of VaR change vs. expanding distribution
5. Percentile ranker: today's VaR in historical VaR distribution
6. Risk Brief template (Markdown)
7. Interpretation rules engine (quantitative → plain language)
8. IEF, EFA, GLD data download

### Out of scope for v1
- Parametric or Monte Carlo VaR
- Trade recommendations ("reduce equity by 5%")
- Automated alerts
- Factor attribution
- Multiple portfolios
- Live data feeds
- Interactive dashboard
