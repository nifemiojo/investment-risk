# The Monte Carlo VaR Algorithm

**Date:** 2026-07-10
**Topic:** The step-by-step algorithm — from model to VaR number

---

## You Already Know the Core Pattern

Historical VaR is:

```
Collect N past returns → sort → read the α-percentile
```

Monte Carlo VaR is:

```
Simulate N future returns from a model → sort → read the α-percentile
```

The only new piece is step 1: generating the returns. Everything else is identical.

---

## The Algorithm

### Step 1: Specify the Model

Choose what you're simulating from:

- **A distribution:** $r \sim N(\hat{\mu}, \hat{\sigma}^2)$
- **A process:** $r_t = \mu + \phi \cdot r_{t-1} + \epsilon_t$
- **Whatever you can code**

### Step 2: Choose the Number of Scenarios

How many simulated returns? Typically 10,000 to 100,000. More scenarios = less sampling error, but more computation.

### Step 3: Generate Scenarios

If simulating from a distribution: draw $N$ independent returns.

If simulating a process: generate $N$ paths, each of length equal to the VaR horizon (e.g., 1 day, 10 days).

### Step 4: Compute Portfolio P&L for Each Scenario

For a simple linear portfolio: P&L = position × return.

For a portfolio with options: reprice the book under each scenario.

### Step 5: Sort and Read

Sort the P&Ls from worst to best. The α-percentile is your VaR.

---

## Concrete Example: Normal Distribution (Just to See the Algorithm)

Even though simulating from a normal distribution converges to the parametric formula, let's walk through it to see the algorithm in action.

**Setup:** Position = £1,000,000 in SPY. Estimated μ̂ = 0.05%, σ̂ = 1.2% per day. 95% confidence, 1-day horizon.

```python
import numpy as np

# Step 1: Specify the model
mu = 0.0005
sigma = 0.012

# Step 2: Choose N
N = 10000

# Step 3: Generate scenarios
simulated_returns = np.random.normal(mu, sigma, N)

# Step 4: Compute P&L for each scenario
position = 1_000_000
pnls = position * simulated_returns  # simple linear portfolio

# Step 5: Sort and read the 5th percentile
var_95 = np.percentile(pnls, 5)

print(f"Monte Carlo 95% VaR: £{abs(var_95):,.0f}")
print(f"Parametric 95% VaR:  £{1_000_000 * (mu - 1.6449 * sigma):,.0f}")
```

Typical output:
```
Monte Carlo 95% VaR: £19,245
Parametric 95% VaR:  £19,239
```

The difference (~£6) is sampling error. Run it again and you'll get a slightly different number. That's the cost of simulation.

---

## Concrete Example: Something Parametric Can't Do

Now let's simulate from a Student's t-distribution with 4 degrees of freedom — fatter tails than normal. Same μ̂ and σ̂:

```python
from scipy import stats

# Parameters
mu = 0.0005
sigma = 0.012
df = 4  # degrees of freedom — lower = fatter tails

# Generate scenarios
simulated_returns = stats.t.rvs(df=df, loc=mu, scale=sigma, size=N)

# Same P&L and sort step
pnls = position * simulated_returns
var_95_t = np.percentile(pnls, 5)

print(f"Monte Carlo t(4) 95% VaR: £{abs(var_95_t):,.0f}")
print(f"Parametric normal 95% VaR: £{1_000_000 * (mu - 1.6449 * sigma):,.0f}")
```

Typical output:
```
Monte Carlo t(4) 95% VaR: £25,130
Parametric normal 95% VaR: £19,239
```

The t-distribution VaR is ~30% higher because the fatter tails make extreme losses more likely. The normal distribution underestimates the risk.

**Now we're doing something parametric VaR can't do.** You can get the t-distribution quantile from `stats.t.ppf(0.05, df=4, loc=mu, scale=sigma)`, which would give the same answer — but the point is: you'd need to know the t-distribution's quantile function exists and how to call it. Monte Carlo doesn't care: feed it any distribution you can sample from, and you get the VaR.

---

## The General Pattern

```
Whatever model you specify
         ↓
    Generate N scenarios from it
         ↓
    Compute P&L for each scenario
         ↓
    Sort P&Ls from worst to best
         ↓
    Read the α-percentile = VaR
```

The first two steps are where Monte Carlo earns its flexibility. The last three are mechanical — identical to historical VaR.

---

## Check-In

The algorithm is simple. The power is in step 1 — *what model you choose to simulate from.*

I want to move us toward the simulation of processes (path-dependent models) since that's where Monte Carlo is genuinely irreplaceable. But first: **does the algorithm make sense?** And do you see where the computational cost comes from — why 10,000 scenarios matters versus 100?