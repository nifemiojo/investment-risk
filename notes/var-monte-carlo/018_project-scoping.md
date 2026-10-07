# Monte Carlo VaR Projects: From Concept to Code

**Date:** 2026-07-10
**Topic:** Three practical projects to take Monte Carlo and GARCH concepts into real analysis

---

## Project 1: Semi-Variance vs Variance — Testing the Symmetry Assumption

**The question:** Does standard deviation overstate or understate downside risk at Spreadex?

**Why it matters:** You identified that variance treats +5% and −5% identically, but risk management only cares about the downside. This project quantifies whether that matters in practice.

**What to do:**

1. Pick one of Spreadex's major risk exposures — an index, a commodity, FX pair
2. Pull daily returns for the past 1–2 years
3. Compute:

$$\text{Standard deviation: } \sigma = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(r_i - \bar{r})^2}$$

$$\text{Downside deviation: } \sigma_{\text{down}} = \sqrt{\frac{1}{n}\sum_{i=1}^{n}\min(r_i - \bar{r}, 0)^2}$$

**Terms:**
- $\sigma$: standard deviation (all deviations)
- $\sigma_{\text{down}}$: downside deviation (only negative deviations)
- $\min(r_i - \bar{r}, 0)$: zero for returns above the mean, the deviation for returns below

4. Compare: is $\sigma_{\text{down}} > \sigma$ or $\sigma_{\text{down}} < \sigma$? By how much?
5. Compute parametric VaR using both measures. How different are the numbers?
6. Backtest: which VaR estimate has the exception rate closer to the expected 5%?

**If $\sigma_{\text{down}} > \sigma$:** The distribution has a fat left tail. Standard VaR is too optimistic.

**If $\sigma_{\text{down}} < \sigma$:** The distribution has a fat right tail (rallies are bigger than crashes). Standard VaR is too conservative.

**External artifact:** "When Symmetry Fails: Downside Risk vs Total Risk in [Asset Class]" — a short writeup with code.

---

## Project 2: Detecting and Measuring Volatility Clustering

**The question:** Is volatility clustering actually present in Spreadex's risk exposures, and how much does ignoring it distort VaR?

**Why it matters:** Parametric and historical VaR both assume each day's return is an independent draw from the same distribution. If volatility clusters exist, this assumption is violated — VaR after a crash is higher than VaR after a calm day, but the models give you the same number.

**What to do:**

### Part A: Detect Clustering

1. Pick the same asset as Project 1
2. Compute daily squared returns: $r_t^2$
3. Compute the autocorrelation of $r_t^2$ at lags 1, 2, 5, 10:

$$\rho_k = \frac{\sum_{t=k+1}^{n}(r_t^2 - \overline{r^2})(r_{t-k}^2 - \overline{r^2})}{\sum_{t=1}^{n}(r_t^2 - \overline{r^2})^2}$$

**Terms:**
- $\rho_k$: autocorrelation of squared returns at lag k
- If $\rho_1$ is significantly positive → volatility clusters exist

4. Plot $r_t^2$ over time. Do you see calm periods and turbulent periods visually?

### Part B: Estimate a GARCH Model

5. Fit a GARCH(1,1) to the daily returns (use `arch` library in Python)
6. Extract the conditional volatility series $\sigma_t$
7. Plot $\sigma_t$ against actual returns. Do the volatility spikes align with turbulent periods?

### Part C: Show the VaR Impact

8. Pick two dates: one after a calm period (low $\sigma_t$), one after a turbulent period (high $\sigma_t$)
9. Compute:
   - Parametric VaR (fixed σ̂ from the full sample)
   - GARCH-conditional VaR ($\mu + \sigma_t \cdot z_{\alpha}$)
10. Show: after a crash, GARCH VaR is X% higher than parametric VaR. The parametric model is sleeping at the wheel.

**External artifact:** "Volatility Clustering in [Asset Class]: Evidence and VaR Implications" — writeup + code + plots.

---

## Project 3: Build a Monte Carlo VaR Engine (Multi-Day GARCH)

**The question:** For a 10-day horizon, how different is Monte Carlo VaR (with GARCH) from the parametric √10 rule?

**Why it matters:** This is where Monte Carlo genuinely earns its keep. Parametric VaR uses √10 scaling. Monte Carlo + GARCH simulates actual 10-day paths where volatility evolves.

**What to do:**

1. Fit a GARCH(1,1) to daily returns (from Project 2)
2. Implement the Monte Carlo engine:

```python
def simulate_paths(sigma_current, omega, alpha, beta, mu, horizon, n_paths):
    paths = np.zeros((n_paths, horizon))
    for i in range(n_paths):
        sigma = sigma_current
        for t in range(horizon):
            z = np.random.normal(0, 1)
            r = mu + sigma * z
            paths[i, t] = r
            sigma_sq = omega + alpha * r**2 + beta * sigma**2
            sigma = np.sqrt(sigma_sq)
    return paths
```

3. Run 10,000 paths of 10 days each from two starting states:
   - Starting from current (calm) volatility
   - Starting from elevated (post-crash) volatility
4. For each, compute the 10-day cumulative returns and the 5th percentile
5. Compare with parametric √10 VaR

**The key output:** A table showing:

| Starting State | Monte Carlo 10-day VaR | Parametric √10 VaR | Difference |
|---|---|---|---|
| Calm (σ = 1.0%) | −X% | −Y% | Z% |
| Elevated (σ = 2.5%) | −X% | −Y% | Z% |

**External artifact:** A GitHub repo with a clean, documented Monte Carlo VaR implementation + a writeup explaining the method and the results.

---

## Sequencing

Projects 1 and 2 are standalone — either can be done first. Project 3 depends on Project 2 (you need the GARCH parameters).

**Recommended order:**
1. Project 1 first (simplest — just computing two standard deviations)
2. Project 2 next (introduces GARCH estimation, sets up Project 3)
3. Project 3 last (ties everything together into a working Monte Carlo engine)

---

## Connection to Your Goals

These projects map directly to your learn-before-leaving framework:

| Spreadex Learning Area | Project Connection |
|---|---|
| **Portfolio Exposure & Risk** | All three projects deepen VaR understanding — the core risk metric |
| **Automated Trading** | Project 2 (vol clustering) has implications for when hedges should be triggered |
| **Attribution** | Understanding conditional vs unconditional risk changes how you interpret P&L |
| **External artifact** | Each project produces a GitHub-ready output that compounds beyond Spreadex |

---

## Check-In

Which project excites you most as a starting point? And do you want to set up the sandbox environment now — pull some actual Spreadex-relevant data and start computing?