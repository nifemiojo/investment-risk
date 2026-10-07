# Handoff — Portfolio VaR Session (2026-07-22)

**For:** Next agent session
**From:** Session ending 2026-07-22
**Status:** Module 1 + 3 notebooks complete. Lead-lag measurement next.

---

## What we built this session

### Conceptual foundation (19 session files)
`/home/femi/femi-corp/areas/finance/sessions/portfolio-var-prerequisites/`

001-003: Portfolio return as weighted sum (derivation, intuition, mental models)
004-006, 008-009: Covariance and correlation (definitions, scale contamination, when each is useful)
007, 011-013, 015: Diversification benefit (formula, naive sum derivation, worked examples)
010: Correlation breakdown during crises
016: Diversification benefit in practice (three regimes, leading indicator, use cases)
017: Correlation-reactive VaR systems (three approaches)
018: SESSION SUMMARY (full index)
019: Measuring correlation → VaR lead-lag (methodology, not yet built)

### Notebooks executed
All in `/home/femi/femi-corp/areas/finance/projects/historical-var/notebooks/`

- **12_portfolio_diversification_benefit.ipynb** — SPY/BND 60/40, benefit = 13.6%, min 3.8% (Jun 2021), max 31.6% (Nov 2024). Part D includes three regimes + practical use cases.
- **13_correlation_dynamics.ipynb** — 60d/252d ratio, correlation gap, 2022 flip. Ratio clipped at ±5 for readability. Latest ratio = 1.86 (correlation rising).
- **15_correlation_adjusted_var.ipynb** — VaR_adj = α·baseline + (1−α)·naive_sum. Cuts breach spikes 6.36% → 4.89% in strong shift regime. Symmetric blend too conservative when ρ falling.

---

## Plan reference
`/home/femi/femi-corp/areas/finance/projects/historical-var/.hermes/plans/2026-07-21_portfolio-var-lesson-plan.md`

---

## Next: Notebook 13b — Correlation → VaR lead-lag measurement

**Goal:** Quantify whether correlation actually leads VaR, and by how many trading days.

**Three methods (see file 019 for details):**

1. **Cross-correlation plot** — Corr(ratio_t, VaR_{t+k}) for k = −120 to +120 days. Peak at k > 0 means ratio leads VaR.
2. **Event study** — Define "events" as ratio > 2.0. Track average VaR/benefit/breach path from 60 days before to 180 days after.
3. **Rolling cross-correlation** — Does lead time vary by regime?

**Data already available:** All series (ratio, VaR, benefit, breaches) computed in Notebooks 12/13/15. Reuse the data pipeline from Notebook 13.

**Design principles:**
- Always include "so what" — Spreadex/FINBOURNE context
- Connect back to Notebook 15 (does the lead justify the adjustment?)
- Use existing `src/` functions — no new modules needed initially

---

## After 13b: Notebook 14 — Portfolio VaR dashboard

Production monitoring view combining everything:
- All VaR methods on portfolio returns (equal, decay, vol-scaled, combined)
- Multi-window divergence
- Diversification benefit panel
- Correlation ratio panel
- **Correlation-adjusted VaR** (from Notebook 15) alongside standard VaR

---

## Key conventions

- **Sandbox:** `~/.pyenv/versions/miniconda3-latest/envs/sandbox`
- **Sessions folder:** `/home/femi/femi-corp/areas/finance/sessions/<topic-slug>/` (not nested in projects)
- **Notebooks:** `/home/femi/femi-corp/areas/finance/projects/historical-var/notebooks/`
- **yfinance-helpers** editable install at `/home/femi/femi-corp/areas/finance/projects/yfinance-helpers/` — run `~/.pyenv/versions/miniconda3-latest/envs/sandbox/bin/pip install -e <path>` if import fails
- **Execute notebooks:** `~/.pyenv/versions/miniconda3-latest/envs/sandbox/bin/jupyter nbconvert --execute --to notebook --inplace <notebook> --ExecutePreprocessor.timeout=180`
- **LaTeX:** display `$$...$$`, inline `$...$`, never `$$` inline
- **Variable naming:** domain-meaningful (day not t, returns not arr)
- **Teacher skill** loaded — examples first, find hazy concepts, include practical framing

## Teaching principles (for next agent)

1. Always include the "so what" — practical use cases (Spreadex live trading, FINBOURNE institutional, personal toolkit)
2. Roadmap includes n-asset generalisation after 2-asset work is solid
3. User is a quantitative developer at Spreadex, C# → Python learner, career direction = systematic multi-asset investing
4. Design before code — discuss API/structure before writing
5. Save teaching responses verbatim as numbered .md files in sessions folder

## Mental models built (user should retain)

- Percentile of weighted sum ≠ weighted sum of percentiles (unless ρ = +1)
- Portfolio return series as information compression (distribution reveals diversification)
- Stable baseline + fast detector + blend rule (unifying pattern for reactive systems)
- Two-number story: VaR = how much, benefit = how reliable
- Correlation as leading indicator, benefit as symptom, VaR as consequence
- Covariance for computation, correlation for comparison
