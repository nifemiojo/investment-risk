# Notebook Plan: Estimators Are Random Variables (Revised)

**Session:** sample-mean/notebooks  
**Topic:** Building intuition that $\bar{x}$ is a random draw from a sampling distribution  
**Status:** Plan — review before implementation  
**Design rule:** One key concept per notebook. Small, digestible, self-contained.

---

## 1. The Five Notebooks

| # | Notebook | One key concept | Data |
|---|----------|----------------|------|
| 1 | `001_one-sample-one-estimate` | **$\bar{x}$ is random** — same process, different samples, different estimates | Synthetic (SPY-parameterised normal) + real SPY |
| 2 | `002_the-sampling-distribution` | **The sampling distribution** — 10,000 estimates reveal the full distribution your single $\bar{x}$ was drawn from | Synthetic + real SPY bootsrap |
| 3 | `003-standard-error-and-sample-size` | **Precision scales with $\sqrt{n}$** — larger samples tighten the sampling distribution, but slowly | Synthetic (normal, three n's) + real SPY at 21/63/252 |
| 4 | `004-data-vs-sampling-distribution` | **Data distribution ≠ sampling distribution** — they are different objects with different shapes | Synthetic (side-by-side) + real SPY (side-by-side) |
| 5 | `005-clt-nonnormal-data` | **The CLT compresses shape toward normality** — even when returns are skewed and fat-tailed, $\bar{x}$ becomes approximately normal | Synthetic (Student's t, three n's) + real SPY (bootstrap at three n's) |

---

## 2. Notebook 1: One Sample, One Estimate

**One key concept:** *Same process, different samples, different estimates. $\bar{x}$ is a random variable.*

### Synthetic section

- True process: $\mu = 0.04\%$, $\sigma = 1.2\%$ (SPY-like normal)
- Draw **one** sample of $n=252$. Compute $\bar{x}_1$. It's close to 0.04% but not exact.
- Draw a **second** sample of $n=252$. Compute $\bar{x}_2$. Different.
- Show both on a simple number-line plot with $\mu$ marked.
- One sentence takeaway: "Same process. Same sample size. Different answer. The variation is real."

### Real data section

- Load real SPY daily returns from the project's data
- Pick two non-overlapping 252-day windows (e.g. 2019–2020 and 2023–2024)
- Compute $\bar{x}$ for each window
- Show both on a number-line plot
- **Key message:** Even with real data, different windows give different means. This isn't a synthetic curiosity — it's your actual estimation problem.

### Figures

| Figure | What |
|--------|------|
| Fig 1a | Two histograms overlaid (synthetic, same bins) with vertical lines for $\bar{x}_1$, $\bar{x}_2$, $\mu$ |
| Fig 1b | Number-line plot for two real SPY windows |

---

## 3. Notebook 2: The Sampling Distribution

**One key concept:** *10,000 estimates reveal the distribution your single $\bar{x}$ was drawn from.*

**Prerequisite:** Notebook 1

### Synthetic section

- Draw 10,000 samples of $n=252$ from SPY-parameterised normal
- Store all 10,000 $\bar{x}$'s
- Plot histogram → this IS the sampling distribution
- Overlay: true $\mu$ (red), your one $\bar{x}$ from Notebook 1 (orange), normal curve $N(\mu, \sigma^2/n)$
- **Key message:** Your estimate is one draw from this distribution. You don't know where in it you sit.

### Real data section

- Load real SPY returns
- Bootstrap: resample (with replacement) 252 returns from the last 5 years of SPY data. Compute $\bar{x}$. Repeat 10,000 times.
- Plot histogram of bootstrap $\bar{x}$'s
- Overlay: the actual $\bar{x}$ from the most recent 252-day window
- **Key message:** This is as close as you can get to seeing the sampling distribution for real data — no normality assumption needed.

### Figures

| Figure | What |
|--------|------|
| Fig 2a | Sampling distribution histogram (synthetic), $\mu$ and one $\bar{x}$ marked, normal curve overlay |
| Fig 2b | Bootstrap sampling distribution (real SPY), actual $\bar{x}$ marked |

---

## 4. Notebook 3: Standard Error and Sample Size

**One key concept:** *Precision improves with $\sqrt{n}$, not $n$. To halve the error, quadruple the data.*

**Prerequisite:** Notebook 2

### Synthetic section

- Three sample sizes: $n = 21, 63, 252$
- For each: draw 10,000 samples, compute $\bar{x}$, record the 10,000 estimates
- Three-panel histogram, shared x-axis, same bin width
- Annotate each panel with: $\text{SE} = \sigma/\sqrt{n}$
- Below the plot: a small table — $n$, SE, "to halve SE, you'd need..."
- **Key message:** The distribution tightens, but slowly. Going from 63 to 252 (4× the data) halves the SE.

### Real data section

- Load real SPY returns  
- For each $n$ (21, 63, 252): take a rolling window of that length, compute $\bar{x}$, slide forward 1 day, repeat → you get a series of $\bar{x}$'s
- Plot the three series on one time axis (different colours/opacities)
- Compute the standard deviation of each rolling-$\bar{x}$ series → this is the *realised* standard error
- Table: $n$, formula SE ($\sigma/\sqrt{n}$), realised SE, ratio
- **Key message:** The realised SE is wider than the formula — because of volatility clustering and non-stationarity. The formula is a lower bound.

### Figures

| Figure | What |
|--------|------|
| Fig 3a | Three-panel histogram (synthetic, $n=21,63,252$) |
| Fig 3b | Rolling $\bar{x}$ series for real SPY at three window lengths |
| Fig 3c | Table: formula SE vs realised SE |

---

## 5. Notebook 4: Data Distribution vs Sampling Distribution

**One key concept:** *They are different objects. The data distribution is wide and (in reality) skewed. The sampling distribution is narrow and approximately normal. Don't confuse them.*

**Prerequisite:** Notebooks 2 and 3

### Synthetic section

- One sample of 10,000 daily returns from SPY-parameterised normal → histogram on the left
- 10,000 $\bar{x}$'s each from $n=252$ → histogram on the right
- Same x-axis range across both panels
- Vertical line at $\mu$ on both
- Annotation: "Width: $\sigma$" on left, "Width: $\sigma/\sqrt{n}$" on right
- **Key message:** The sampling distribution is squashed toward the centre. Averaging removes noise.

### Real data section

- Left panel: histogram of all daily SPY returns (last 5 years)
- Right panel: bootstrap sampling distribution of $\bar{x}$ from Notebook 2
- Same x-axis range
- Annotate with actual standard deviation vs standard error
- **Key message:** Real data makes the difference even starker — the data distribution is skewed and fat-tailed, but the sampling distribution of $\bar{x}$ is much more symmetric and narrow.

### Figures

| Figure | What |
|--------|------|
| Fig 4a | Side-by-side: synthetic data distribution vs synthetic sampling distribution |
| Fig 4b | Side-by-side: real SPY data distribution vs real SPY bootstrap sampling distribution |

---

## 6. Notebook 5: The CLT with Non-Normal Data

**One key concept:** *The CLT compresses the shape. Even when returns are skewed and fat-tailed, $\bar{x}$ becomes approximately normal — but the convergence is slow in the tails.*

**Prerequisite:** Notebook 4 (needs to understand the two distributions first)

### Synthetic section

- True process: Student's t with df=5, shifted and scaled to match SPY $\mu=0.04\%$, $\sigma=1.2\%$
- Show the data distribution first: one sample of 10,000 returns → skewed, fat-tailed. "This is what daily returns look like."
- Three sample sizes: $n = 5, 30, 252$
- For each: draw 10,000 samples, compute $\bar{x}$, plot sampling distribution
- Overlay normal curve on each
- Annotation: at $n=5$, the sampling distribution inherits the skew. At $n=30$, it's more symmetric. At $n=252$, it's close to normal.
- **Key message:** The CLT works — but $n=252$ gets you "approximately normal," not "exactly normal." The tails converge slowest, and VaR lives in the tails.

### Real data section

- Bootstrap from real SPY returns at three sample sizes: $n=21, 63, 252$
- Three-panel histogram of bootstrap $\bar{x}$'s
- Overlay normal curve on each
- QQ plot for $n=252$ bootstrap means against normal
- **Key message:** Even with real SPY data (skewed, fat-tailed), the bootstrap sampling distribution of $\bar{x}$ approaches normality. But check the QQ plot — the tails deviate.

### Figures

| Figure | What |
|--------|------|
| Fig 5a | Data distribution of Student's t returns (one panel) |
| Fig 5b | Three-panel: sampling distributions for $n=5, 30, 252$ with normal overlays |
| Fig 5c | Three-panel: bootstrap sampling distributions for real SPY at $n=21, 63, 252$ |
| Fig 5d | QQ plot: bootstrap $\bar{x}$'s ($n=252$) vs normal quantiles |

---

## 7. Summary: The Learning Arc

```
Notebook 1:  "Wait — different samples give different means?"
Notebook 2:  "Oh. There's a whole distribution of possible means."
Notebook 3:  "And it tightens with more data, but painfully slowly."
Notebook 4:  "The mean's distribution is completely different from the data's distribution."
Notebook 5:  "And it becomes normal even when the data isn't. That's the CLT."
```

Each notebook is ~4–6 cells. Each has one figure (maybe two). Each ends with a single bold sentence — the one thing to remember.

---

## 8. Real Data Integration Strategy

| Notebook | How real data is used |
|----------|----------------------|
| 1 | Two non-overlapping 252-day windows from SPY — compare their means |
| 2 | Bootstrap 10,000 $\bar{x}$'s from SPY returns — see the real sampling distribution |
| 3 | Rolling $\bar{x}$ at three window lengths — compare realised SE to formula SE |
| 4 | Side-by-side: SPY return histogram vs bootstrap $\bar{x}$ histogram |
| 5 | Bootstrap at three n's + QQ plot to assess normality of real sampling distribution |

The synthetic sections always come first — they establish the concept against a known truth ($\mu$). The real data sections then say: "now let's see this in your actual data, where you don't know the truth."

---

## 9. Code Style: Educational Clarity Above All

These notebooks are teaching tools first, code second. Every line must be readable by someone who is still building intuition — not just by someone who already understands.

### 9.1 Variable Names: Full Words, Domain Meaning

| ❌ Don't | ✅ Do | Why |
|----------|-------|-----|
| `r = np.random.normal(...)` | `daily_returns = np.random.normal(...)` | What is `r`? A return? A row? A rate? |
| `sm = np.mean(samples, axis=1)` | `sample_means = np.mean(samples, axis=1)` | `sm` could mean anything. `sample_means` is the concept. |
| `n, mu, sig = 252, 0.04, 1.2` | `n_days = 252; true_mu = 0.04; true_sigma = 1.2` | Grouped assignment saves lines but costs comprehension. |
| `x1, x2 = ...` | `sample1_returns = ...; sample2_returns = ...` | Number suffixes don't convey meaning. |

### 9.2 One Operation Per Line

```python
# ❌ Chained — hard to read, harder to debug
plt.hist(np.mean(np.random.normal(mu, sigma, (10000, n)), axis=1), bins=50)

# ✅ One step at a time
# Draw 10,000 samples of n returns each — shape: (10000, n)
samples = np.random.normal(loc=true_mu, scale=true_sigma, size=(n_simulations, n_days))
# Compute the mean of each sample — shape: (10000,)
sample_means = np.mean(samples, axis=1)
# Plot
plt.hist(sample_means, bins=50)
```

Every variable has a name. Every step is inspectable. A beginner can print `samples.shape` or `sample_means[:5]` to see what's happening. A one-liner hides all of that.

### 9.3 Named Parameters, Always

```python
# ❌ Positional — what do these numbers mean?
returns = np.random.normal(0.04, 1.2, 252)

# ✅ Named — self-documenting
returns = np.random.normal(loc=true_mu, scale=true_sigma, size=n_days)
```

No magic numbers. Every parameter is named, and the values come from the Parameters cell — not hardcoded mid-cell.

### 9.4 Comments That Explain WHY, Not WHAT

```python
# ❌ WHAT — the code already says this
sample_means = np.mean(samples, axis=1)  # compute the mean of each sample

# ✅ WHY — the code doesn't say this
# axis=1 means "average across columns" — each row is one sample of n_days returns.
# The result is 10,000 numbers: one mean per sample.
sample_means = np.mean(samples, axis=1)
```

The code already tells you *what* it does. Comments should tell you *why* it's structured that way, *what the shape means*, or *what concept is being demonstrated*.

### 9.5 Print Statements That Narrate

The notebook should tell a story that can be followed just by reading the output:

```
Sample 1: mean daily return = 0.031%
Sample 2: mean daily return = 0.052%
True mean (the process we're sampling from): 0.040%

→ The two samples gave different estimates. Neither is exactly right.
→ This variation is real — it happens every time you estimate from finite data.
```

Every code cell should print something interpretable. The printout should make sense even if you skip the code.

### 9.6 Cell Structure: Concept → Code → Takeaway

Each logical section of a notebook follows this rhythm:

```
┌─────────────────────────────────┐
│ Markdown: What are we about to  │
│ do and why? (2-3 sentences)     │
├─────────────────────────────────┤
│ Code: The implementation        │
│ (clean, commented, step-by-step)│
├─────────────────────────────────┤
│ Markdown: The takeaway          │
│ (1 bold sentence + 1-2 lines)   │
└─────────────────────────────────┘
```

No section is code-only. No section is markdown-only. They work as pairs.

### 9.7 Loops with Purpose, Not Just to Iterate

When looping over simulations:

```python
# ❌ Terse loop — the body is dense
sample_means = []
for _ in range(10000):
    sample_means.append(np.random.normal(mu, sigma, n).mean())

# ✅ Loop with a descriptive iterator and a comment on what each iteration does
sample_means = []
for simulation_i in range(n_simulations):
    # Draw one sample of n_days returns from the true process
    one_sample = np.random.normal(loc=true_mu, scale=true_sigma, size=n_days)
    # Compute its mean — this is one draw from the sampling distribution
    one_mean = np.mean(one_sample)
    sample_means.append(one_mean)
```

The second version teaches. The first version works but obscures. For 10,000 iterations where vectorisation is faster and cleaner (Section 9.2), use the vectorised approach — but for smaller loops where the explicit version clarifies the concept, prefer clarity over speed.

### 9.8 Plots That Communicate Instantly

| Rule | Example |
|------|---------|
| Title says what we're looking at | `"Sampling Distribution of the Sample Mean (n=252)"` not `"Figure 1"` |
| Axes have units | `"Daily Return (%)"` not `"Value"` |
| Annotations explain the visual | Arrow pointing to a line: `"Your one estimate: 0.031%"` |
| Legend is meaningful | `"True μ"` not `"Line 1"` |
| Colour is deliberate | One colour for data, one for estimates, one for truth — consistent across notebooks |

### 9.9 Summary: The Code Style Checklist

Before any cell is done, check:

- [ ] Every variable name is a full word (or two) that conveys meaning
- [ ] Every numpy/scipy function call uses named parameters
- [ ] No operation chains longer than one method call without an intermediate variable
- [ ] Every number that has meaning comes from the Parameters cell — no magic constants in code
- [ ] Comments explain *why*, not *what*
- [ ] The cell prints output that tells a story
- [ ] The cell is paired with a markdown cell: one above (context), one below (takeaway)
- [ ] Plots have descriptive titles, labelled axes, and annotations

---

## 10. Technical Notes

- **Seed**: Set once in Notebook 1, reference it in subsequent notebooks so synthetic sections are reproducible
- **SPY data path**: Use the project's existing data pipeline — `from data.something import load_spy_returns` or equivalent. Don't hardcode a CSV path
- **Notebook style**: Match Phase 1 notebooks — dark background, clean matplotlib params, `%matplotlib inline`
- **Each notebook is self-contained**: imports, parameters, everything inside. Someone can open Notebook 3 without running 1 or 2
- **Parameters cell**: Every notebook starts with a "Parameters" cell (matching the Phase 1 convention) — true $\mu$, $\sigma$, $n$ values, seed

---

## 11. File Layout

```
areas/finance/projects/historical-var/notebooks/sample-mean/
├── 001_one-sample-one-estimate.ipynb
├── 002_the-sampling-distribution.ipynb
├── 003-standard-error-and-sample-size.ipynb
├── 004_data-vs-sampling-distribution.ipynb
├── 005_clt-nonnormal-data.ipynb
└── verify-notebooks.py                     ← runs all five, checks they execute cleanly
```

This sits alongside the existing Phase 1 notebooks (`01_single_point_var.ipynb` through `16_n_asset_generalisation.ipynb`) but in its own subfolder to keep the topic self-contained. The plan document stays in sessions:

```
sessions/sample-mean/notebooks/
└── 001_sampling-distribution-plan.md       ← this plan
```

---

## 12. Questions for You

1. **Granularity:** Five notebooks feel right? Or split further / merge any?

2. **Real data source:** Where does SPY data live in this project? I'll need the exact import path before coding. Is there a `data/` module or a specific CSV/parquet file?

3. **Notebook style:** Confirm dark background matches Phase 1. Want me to check an existing notebook first for exact matplotlib rcParams?

4. **Order to build:** All five at once, or one at a time with review between each?

5. **Student's t df=5:** Right level of non-normality for Notebook 5? Or want something with explicit negative skew (e.g. a mixture distribution)?