# Monte Carlo VaR: Session Summary & Handover

**Date:** 2026-07-10
**Session folder:** `./sessions/var-monte-carlo/`
**Status:** Conceptual foundation solid. Key distinctions internalized. Ready to bridge to estimation and failure modes.

---

## What We Covered (21 Files)

| File | Topic | Key Takeaway |
|---|---|---|
| 001 | Opening | Socratic — where does your understanding break? Monte Carlo from normal = expensive parametric. |
| 002 | Three gaps | Distributions w/o quantile, path-dependency, multi-asset dependence |
| 003 | Boundary corrected | It's not "no quantile formula" — it's "can you reduce the problem to a single-period fixed-parameter distribution?" |
| 004 | Vol clustering example | Concrete numbers on oil shock: parametric VaR simultaneously too conservative (calm) and too dangerous (crisis) |
| 005 | Distributions vs processes | Coin → discrete returns → normal → AR(1) process. Distribution = static; process = evolves with memory. |
| 006 | Monte Carlo simulates both | Distribution draws vs process paths. Universal fallback: if you can code the rule, you can simulate it. |
| 007 | The algorithm | Model → simulate N scenarios → compute P&L → sort → read percentile. Same "sort and read" as historical VaR. |
| 008 | Scenarios vs paths | Scenario = one draw. Path = sequence of dependent draws. For 1-day from a distribution, they're the same. For 10-day GARCH, 10K paths = 100K draws. |
| 009 | From paths to VaR | Each path → one cumulative return. VaR is the quantile ACROSS paths, not within each path. |
| 010 | Simulation frequency | Match the frequency where dependence lives. Daily is convention (empirical signal + data availability + decision horizon). |
| 011 | Why daily | Empirical sweet spot, practical data quality, decision-aligned. But it IS a choice — HAR models show multi-scale dynamics. |
| 012 | GARCH from first principles | ω (floor), α (news), β (memory/persistence). Walkthrough: crash spikes vol, quiet days keep it elevated via β. |
| 013 | Why squared returns | Sign doesn't matter for variance. r² is an unbiased proxy for σ². Squaring gives more weight to extremes. |
| 014 | Vol not return autocorrelation | GARCH = "big moves beget big moves, but direction is a coin flip." Not momentum, not trend. |
| 015 | Symmetric vs asymmetric | Variance treats rallies and crashes equally. Leverage effect: crashes actually spike vol more. GJR-GARCH/EGARCH fix this. Deeper question: should risk measurement use semi-variance? |
| 016 | r² as variance proxy | Full derivation: σ_t known at start of day (constant), z_t random. E[r²] = σ² · E[z²] = σ². r² ~ σ² · χ²₁ — unbiased but extremely noisy. |
| 017 | 1-day VaR and path-dependency | Original version — somewhat confusing. Rewritten in 020. |
| 018 | Project scoping | Three projects: semi-variance test, volatility clustering detection + GARCH estimation, Monte Carlo VaR engine |
| 019 | Population vs conditional variance | σ²_uncond = ω/(1−α−β) (long-run average). σ²_t = conditional (changes daily). r² estimates σ²_t, not σ²_uncond. |
| 020 | 1-day walkthrough | Concrete: calm day σ=1.08% → VaR=£17.8K. Post-crash σ=1.55% → VaR=£25.5K. Formula = simulation for 1-day. |
| 021 | Parametric vs GARCH parametric | Same formula structure (μ−z·σ). Difference is σ̂: fixed sample stat vs time-varying conditional estimate. |

---

## Key Mental Models Built

### 1. Distribution vs Process
- **Distribution** = static list of outcomes and probabilities. Each draw independent. No memory.
- **Process** = rule for how outcomes evolve. Today depends on yesterday. Has memory.
- Monte Carlo can simulate either.

### 2. Scenario vs Path
- **Scenario** = one draw (1-day VaR from a distribution: 10K scenarios = 10K draws)
- **Path** = sequence of dependent draws (10-day GARCH: 10K paths = 100K draws)
- The computational cost multiplies with horizon length.

### 3. GARCH as Time-Varying Conditional Variance
- σ²_t = ω + α·r²_{t-1} + β·σ²_{t-1}
- ω = floor, α = reaction to news, β = persistence (half-life = ln(0.5)/ln(β))
- Models volatility clustering, not return autocorrelation
- Conditional (daily) vs unconditional (long-run) variance

### 4. The Clean Separation
- **GARCH** changes *how you estimate volatility* — conditional on yesterday, not flat sample average
- **Monte Carlo** changes *how you compute the quantile* — simulation instead of formula
- Two independent innovations. Can use GARCH without MC (1-day). Can use MC without GARCH (simulate from fixed distribution).

### 5. When Monte Carlo Earns Its Keep
- **Multi-period paths with dependence** (no formula for 10-day GARCH distribution)
- **Complex models with no closed-form quantile** (regime-switching, copulas, nonlinear P&L)
- If neither applies: MC is just an expensive way to rediscover the formula

---

## What's Still to Cover

- [ ] **GARCH estimation** — how ω, α, β are actually fitted from data (MLE)
- [ ] **Monte Carlo failure modes** — sampling error, model risk amplification, garbage in garbage out, computation/time constraints
- [ ] **Multi-asset Monte Carlo** — Cholesky decomposition, copulas, joint simulation
- [ ] **Connection to Spreadex systems** — what model does the autohedge VaR actually use?
- [ ] **Backtesting Monte Carlo VaR** — how do you validate a simulation-based model?

---

## Connection to Other VaR Methods

| Method | How It Gets the Distribution | Key Limitation |
|---|---|---|
| **Historical** | Actual past returns (252 points) | Assumes past ≈ future; window/regime sensitivity |
| **Parametric** | Imposes distribution (normal), 2 parameters | Normality assumption; fixed σ̂ |
| **GARCH Parametric** | Conditional variance from GARCH, normal shocks | Still assumes normal shocks; 1-day only (formula) |
| **Monte Carlo** | Simulates from any specified model | Model risk; computational cost; sampling error |

---

## Project Sequencing (from 018)

1. **Semi-variance vs variance** — simplest, tests symmetry assumption
2. **Volatility clustering detection + GARCH estimation** — introduces GARCH fitting, sets up project 3
3. **Monte Carlo VaR engine** — 10-day GARCH paths, compare to √10 scaling

Each produces an external artifact (GitHub + writeup).

---

## User Preferences Active

- Auto-save all responses to `./sessions/<topic>/NNN_*.md` (skill: `teaching-session-logging`)
- LaTeX: `$$...$$` for display math, `$...$` for inline math (never `$$...$$` inline)
- Sandbox miniconda env for Python work
- Socratic teaching style: find hazy concept, drill depth over breadth
- Examples first, concrete before abstract
