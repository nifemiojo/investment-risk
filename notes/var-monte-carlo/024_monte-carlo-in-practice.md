# Monte Carlo VaR in Practice: The Practitioner's View

**Date:** 2026-07-10
**Topic:** When practitioners use Monte Carlo, how they implement it, how they communicate results, and how they handle its limitations

---

## The Decision: When to Reach for Monte Carlo

Practitioners don't use Monte Carlo as their default VaR method. They reach for it when the other methods demonstrably fail. The decision tree:

```
Is the portfolio linear?
├── Yes → Is the distribution roughly normal?
│   ├── Yes → Parametric VaR. Done.
│   └── No  → Historical VaR. Done.
└── No (contains options, structured products, etc.)
    └── Monte Carlo VaR. You need full revaluation.
```

The litmus test: **can you compute portfolio P&L as a weighted sum of asset returns?** If yes, you probably don't need Monte Carlo. If no — if the P&L function has curvature (gamma, vega, cross-gammas) — Monte Carlo is the only honest answer.

---

## How They Actually Implement It

### The Production Pipeline

```
1. DATA INGESTION
   Market data (prices, vols, rates, curves)
   Position data (what does the book hold?)
   ↓
2. MODEL CALIBRATION
   Estimate GARCH parameters (or whatever process)
   Calibrate correlation matrix
   Fit shock distributions
   ↓
3. SCENARIO GENERATION
   Generate correlated shocks across all risk factors
   Apply the process model (GARCH, etc.)
   ↓
4. FULL REVALUATION ← THE EXPENSIVE STEP
   For each scenario, reprice every instrument
   Options: Black-Scholes, Heston, SABR, etc.
   Bonds: discount cash flows with simulated curves
   ↓
5. AGGREGATION
   Sum P&L across all positions for each scenario
   Sort, read percentile
   ↓
6. REPORTING
   VaR number + breakdowns + diagnostics
```

### The Computational Bottleneck

Step 4 is where the cost lives. For a portfolio of 10,000 options, repricing each one under 10,000 scenarios = 100 million option valuations. That's minutes to hours, not microseconds.

**Workarounds practitioners use:**

- **Delta-gamma approximation:** Instead of full revaluation, approximate P&L as:
  
  $$\text{P\&L} \approx \delta \cdot \Delta S + \frac{1}{2}\gamma \cdot (\Delta S)^2$$
  
  **Terms:**
  - $\Delta S$: simulated change in the underlying
  - $\delta$: first derivative (delta)
  - $\gamma$: second derivative (gamma)
  
  This is much faster than full revaluation but loses accuracy for large moves or complex payoffs.

- **Grid computing:** Distribute scenarios across a compute cluster. Each node prices a subset of scenarios.

- **Importance sampling:** Don't simulate uniformly — oversample the tail. With 10,000 paths, only 500 are below the 5th percentile. Most of your computation is spent on scenarios you don't care about. Importance sampling concentrates scenarios in the tail region, reducing the number of paths needed.

- **Variance reduction:** Antithetic variates (for every random draw, also use the negative of that draw), control variates (use a related instrument with a known price as a benchmark). These techniques reduce the sampling error for a given number of paths.

---

## How They Use the Results

### Not Just One Number

No practitioner reports a single Monte Carlo VaR and walks away. The output is a dashboard:

| Output | What It Tells You |
|---|---|
| **VaR (95%, 1-day)** | Tomorrow's worst case at 95% confidence |
| **VaR (99%, 1-day)** | Tomorrow's worst case at 99% — the "really bad day" |
| **VaR (95%, 10-day)** | The 10-day horizon — regulatory standard |
| **Expected Shortfall** | Average loss BEYOND the VaR threshold |
| **VaR by asset class** | Which positions are driving the risk? |
| **Marginal VaR** | How much does each position add to total VaR? |
| **Component VaR** | What fraction of total VaR comes from each position? |
| **Stress VaR** | VaR under specific historical scenarios (2008, COVID) |

### The Questions They Answer

The VaR number itself is the least interesting output. The real questions are:

- **"What's driving the VaR today?"** — Is it a single concentrated position? A correlation assumption? A volatility spike?
- **"How would VaR change if I reduced position X by 20%?"** — Marginal VaR answers this.
- **"Is the model working?"** — Backtesting: are exceptions happening at the expected rate?
- **"What's the worst case beyond the VaR threshold?"** — Expected Shortfall. VaR says "you'll lose at most X, 95% of the time." ES says "in the 5% of the time you exceed X, your average loss is Y."

---

## How They Communicate Results

### The Core Challenge

Monte Carlo VaR is hard to explain. "We simulated 10,000 possible futures from a GARCH model with skewed-t shocks" is not a sentence that works in a board meeting.

Practitioners translate:

| Internal Understanding | External Communication |
|---|---|
| "10,000 paths from a GJR-GARCH with skewed-t innovations" | "We stress-tested the portfolio against a wide range of market scenarios, including ones worse than anything we've seen historically" |
| "The 5th percentile of the simulated P&L distribution" | "On 19 out of 20 days, we expect to lose less than £X" |
| "The model assumes conditional normality of standardized residuals" | "The model accounts for the fact that volatile periods cluster together" |

### The Honesty

Good practitioners are explicit about limitations:

> "This number assumes the future will behave like our model. If markets change in ways our model doesn't capture — a liquidity crisis, a correlation breakdown, a new type of shock — this number will be wrong. Here's how wrong it's been in the past, and here's what we're doing to catch it when it breaks."

### The Layered Approach

No single number is trusted alone. The communication always includes:

1. **Monte Carlo VaR** (the model-driven number)
2. **Historical VaR** (the reality check — what does the data say without a model?)
3. **Stress tests** (what happens in specific bad scenarios?)
4. **Backtesting results** (how accurate has the model been?)
5. **Limits and triggers** (what actions are taken at what thresholds?)

The message: "All models are wrong. Here's how we use several wrong models together to be less wrong than any one alone."

---

## When They Don't Use Monte Carlo

| Situation | Why Not | What They Use Instead |
|---|---|---|
| **Linear portfolio, normal-ish returns** | Overkill. Formula is instant and exact. | Parametric VaR |
| **Need to explain to non-technical audience** | "Simulated 10,000 paths" loses people | Historical VaR ("we looked at the last 252 days") |
| **Intraday risk monitoring** | Too slow. Need sub-second updates. | Parametric with real-time vol estimates |
| **Quick sanity check** | "Is this trade directionally risky?" doesn't need simulation | Delta notional or simple parametric |
| **Model is unvalidated** | Garbage in, garbage out. No point simulating from an untested model. | Historical VaR while building confidence in the model |

---

## The Failure Modes Practitioners Worry About

### 1. Model Risk Amplification

Monte Carlo doesn't fix a bad model — it amplifies it. If your GARCH parameters are wrong, 10,000 paths of wrongness are worse than one wrong formula. The simulation gives you a false sense of precision.

### 2. The "Black Box" Problem

Historical VaR = "sort the last 252 returns." Anyone can understand it. Monte Carlo = "we simulated from a process you can't see." When the number is wrong, it's harder to diagnose why. Was it the process model? The shock distribution? The correlation matrix? The revaluation method?

### 3. Sampling Error in the Tail

With 10,000 paths at 99% confidence, only 100 paths are in the tail. Your estimate of the 1st percentile is based on the 100th-worst outcome. With 1,000 paths, it's based on the 10th-worst. The tail estimate is noisy and unstable.

### 4. The Calibration Illusion

You fit a GARCH model to 5 years of daily data (1,260 observations). You estimate 6 parameters. The model fits the past well. Then you simulate 10,000 paths into the future. The apparent precision of 10,000 paths masks the fact that the model is built on 1,260 noisy observations.

### 5. The "Right Model, Wrong Regime" Problem

Your GARCH model was calibrated on a bull market with occasional corrections. Then a genuine crisis hits — the kind with correlation breakdowns and liquidity freezes. The model simulates from a world that no longer exists. The VaR is wrong, and it's wrong in the dangerous direction.

---

## How They Validate

- **Backtesting at multiple horizons:** Does the exception rate match the confidence level? A 95% VaR should be breached on ~5% of days.
- **Kupiec test:** Statistical test for whether the number of exceptions is consistent with the confidence level.
- **Christoffersen test:** Extends Kupiec to also test whether exceptions cluster (they shouldn't — if they do, the model isn't capturing volatility dynamics).
- **Comparison with simpler methods:** If Monte Carlo VaR is consistently different from historical VaR, understand why. The difference itself is diagnostic.
- **Stress period performance:** How did the model perform during the last crisis? If it failed then, it'll fail again.

---

## Check-In

The practitioner's view: Monte Carlo is a tool for specific problems (nonlinear portfolios, complex dependencies, multi-period horizons), not a default. It's expensive, hard to explain, and amplifies model risk. But when the problem demands it, it's the only honest answer.

Key tensions:
- **Flexibility vs fragility:** More parameters = more ways to be wrong
- **Precision vs accuracy:** 10,000 paths look precise, but the model is only as good as its calibration
- **Power vs explainability:** Simulation answers questions other methods can't, but it's harder to debug when wrong

Does this connect to how you'd actually use it at Spreadex? The autohedge system's VaR — is it parametric or Monte Carlo? And does the room hold instruments where the P&L is nonlinear enough to justify simulation?