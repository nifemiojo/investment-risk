# 014 — Notebook 12: Design and Structure

**Date:** 2026-07-22
**Topic:** Notebook 12 — Portfolio Returns and the Diversification Benefit

---

## Notebook structure

**Location:** `projects/historical-var/notebooks/12_portfolio_diversification_benefit.ipynb`

### Part A: Single-point comparison
- Download SPY and BND, align dates (inner join)
- Compute portfolio returns: $r_p = w_1 r_1 + w_2 r_2$
- Individual VaRs → naive sum → portfolio VaR → diversification benefit

### Part B: Rolling diversification benefit
- Rolling VaR on each individual series AND portfolio series
- Rolling naive sum = $w_1 \text{VaR}_{1,t} + w_2 \text{VaR}_{2,t}$
- Rolling benefit = $(\text{naive} - \text{portfolio}) / \text{naive}$
- Three-panel chart: individual vs portfolio VaR, benefit over time, breaches

### Part C: The 2022 collapse
- Zoom into 2021-2023
- Annotate minimum benefit point
- Table: benefit across regimes (pre-COVID, COVID crash, recovery, rate-hiking, recent)

### Part D: The benefit as a monitoring signal
- High benefit (= good diversification) vs low benefit (= fragile portfolio)
- Negative benefit (rare, extreme co-movement signal)
- The naive sum as stress scenario

### Design decisions
- No new `src/` module needed — portfolio return is a one-liner, existing functions accept any return series
- Date alignment via inner join on DataFrame (drops days where one ticker didn't trade)
- All charts use the existing `rolling_var()` and `historical_var()` functions unchanged
