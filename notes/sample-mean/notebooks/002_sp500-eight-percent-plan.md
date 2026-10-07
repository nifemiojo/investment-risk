# Notebook Plan: Testing the "S&P 500 Returns 8% Per Year" Claim

**Session:** sample-mean/notebooks  
**Topic:** Applying sample-mean concepts to a real-world claim  
**Status:** Plan — review before implementation  
**Design rule:** Keep it simple. Two notebooks, one concept each. No deep dives.

---

## 1. The Claim

> *"The S&P 500 returns about 8% per year on average."*

You hear this everywhere — financial media, Reddit, your uncle at Thanksgiving. It's treated as a fact. But after Notebook 001, you now know that any "average return" is just a sample mean — a random variable, an estimate, not a fixed truth.

This mini-series tests the claim against real SPY data and the concepts you've already built: sample means are random, estimates have uncertainty, and signal-to-noise ratios for daily equity returns are terrible.

---

## 2. The Two Notebooks

| # | Notebook | One key concept | 
|---|----------|----------------|
| 1 | `006_sp500-eight-percent-claim` | **8% is an estimate, not a fact** — convert the headline number to daily, compute what the data actually says, show that different windows give radically different answers |
| 2 | `007_sp500-confidence-interval` | **The estimate is imprecise** — build a confidence interval around the long-run mean, compute the signal-to-noise ratio, ask whether we can even reject zero |

---

## 3. Notebook 1: The 8% Claim — What the Data Actually Says

**One key concept:** *"8% per year" is a sample mean computed over a specific window. Change the window, change the number. The claim is an estimate, not a constant of nature.*

**Prerequisite:** Notebook 001 (sample mean is random)

### Cell Structure

| Cell | Type | Content |
|------|------|---------|
| 1 | Markdown | Title, lesson, prerequisites |
| 2 | Markdown | ⚙️ Parameters |
| 3 | Code | Parameters: TICKER, START_DATE, END_DATE, CLAIMED_ANNUAL_RETURN = 8.0 |
| 4 | Code | Imports + load SPY data |
| 5 | Markdown | **Part A: The headline number, translated** |
| 6 | Markdown | What does 8% annual actually mean in daily terms? Simple division: 8/252 ≈ 0.032%. Compound: (1.08)^(1/252) − 1 ≈ 0.031%. Contextualise: "On a typical day, the S&P 500 goes up about three-hundredths of one percent." |
| 7 | Code | Compute both simple and compound daily equivalents. Print them. Show what £10,000 becomes after 1 year at 8% vs flat. |
| 8 | Markdown | **Part B: What does the long-run data actually say?** |
| 9 | Code | Compute the actual mean daily return over the full dataset. Annualise it. Print: "The actual average annual return over this period was X%, not 8%." |
| 10 | Markdown | **Part C: Does it depend on when you measure?** |
| 11 | Markdown | The 8% claim implies a stable property of the market. But you've already seen that different windows give different means. Let's check. |
| 12 | Code | Split the data into 5-year chunks. Compute annualised mean for each. Bar chart. Is any chunk exactly 8%? |
| 13 | Markdown | **Part D: Rolling 10-year average** |
| 14 | Code | Rolling 2520-day (≈10-year) mean, annualised. Line plot. Horizontal line at 8%. Show that the rolling average crosses 8% sometimes, but spends most of its time somewhere else. |
| 15 | Markdown | **Takeaway:** "8% per year" is not a constant. It's a sample mean computed over a specific period. Change the period, change the number. The claim is useful as a rough benchmark, but treating it as a precise, stable fact is a mistake. |
| 16 | Markdown | Key insight + link to next notebook |

### Figures

| Figure | What |
|--------|------|
| Fig 1a | Bar chart: annualised mean return for each 5-year chunk. Horizontal line at 8%. No bar hits it exactly. |
| Fig 1b | Line plot: rolling 10-year annualised mean over time. Horizontal line at 8%. It drifts. |

---

## 4. Notebook 2: How Much Should You Trust It?

**One key concept:** *The long-run mean return has a confidence interval wide enough to drive a truck through. The signal-to-noise ratio is terrible. You cannot reject the hypothesis that the true mean is zero at standard confidence levels.*

**Prerequisite:** Notebook 001 + the sample-mean markdown docs (002_sample-mean-as-estimator.md)

### Cell Structure

| Cell | Type | Content |
|------|------|---------|
| 1 | Markdown | Title, lesson, prerequisites |
| 2 | Markdown | ⚙️ Parameters |
| 3 | Code | Parameters: TICKER, START_DATE, END_DATE |
| 4 | Code | Imports + load SPY data |
| 5 | Markdown | **Part A: The signal-to-noise ratio** |
| 6 | Markdown | The daily mean is the signal. The daily standard deviation is the noise. For SPY: signal ≈ 0.03%, noise ≈ 1.2%. Ratio ≈ 0.025. This is abysmal. |
| 7 | Code | Compute daily mean, daily std, and the ratio. Print them. Add context: "For every 1 unit of signal, there are 40 units of noise." Compare to something with a better ratio (e.g. monthly returns: mean ≈ 0.67%, std ≈ 5.5%, ratio ≈ 0.12 — still bad but 5× better). |
| 8 | Markdown | **Part B: Confidence interval for the mean** |
| 9 | Markdown | Using the full dataset (n = several thousand), build a 95% CI: $\\bar{x} \\pm t_{n-1, 0.025} \\cdot s/\\sqrt{n}$ |
| 10 | Code | Compute 95% CI for daily mean. Convert both bounds to annualised. Print: "We are 95% confident the true annual mean is between X% and Y%." |
| 11 | Markdown | **Part C: Is zero inside the interval?** |
| 12 | Markdown | If zero is inside the 95% CI, we cannot reject $H_0: \\mu = 0$. This doesn't mean the true mean IS zero — it means we don't have enough evidence to say it isn't. |
| 13 | Code | Check if 0 is inside the daily CI. Print the conclusion. Also show the CI on a number line: the interval, a dot at the estimate, a dot at 0, a dot at the claimed 8% annual equivalent. |
| 14 | Markdown | **Part D: How much data would we need?** |
| 15 | Markdown | To shrink the CI enough that zero is definitively outside (i.e. the lower bound > 0), how many years of data would we need? Solve: $\\bar{x} - t \\cdot s/\\sqrt{n} > 0 \\Rightarrow n > (t \\cdot s / \\bar{x})^2$. This is a thought experiment — the answer is uncomfortable. |
| 16 | Code | Compute required n for the lower bound to exceed zero. Convert to years. Print: "To be confident the true mean is positive, you'd need about X years of data. That's longer than the S&P 500 has existed / longer than markets have been in their current form." |
| 17 | Markdown | **Takeaway:** The 8% claim is directionally useful — stocks probably go up over the long run — but as a precise number it's nearly meaningless. The uncertainty around the mean is enormous, and you can't even rule out zero. This is why risk management focuses on volatility (which you CAN estimate precisely) rather than expected returns. |
| 18 | Markdown | Key insight + series wrap-up |

### Figures

| Figure | What |
|--------|------|
| Fig 2a | Number line: the 95% CI for annualised mean. Dots at estimate, 0, and 8%. The interval spans several percentage points. |
| Fig 2b | Bar or line: required years of data to push the lower CI bound above zero — likely in the hundreds |

---

## 5. Summary: Two Notebooks, One Through-Line

```
Notebook 1:  "8% per year? Not exactly — the number depends on when you look."
Notebook 2:  "And even the long-run average is so imprecise you can't reject zero."
```

The pay-off: **the most quoted number in finance is a sample mean, with all the uncertainty that implies. After this series, you'll never hear 'the market returns 8%' the same way again.**

---

## 6. Design Notes

- **Keep it light.** These are capstone notebooks — applying concepts, not introducing new ones. Two notebooks, ~6–8 code cells each.
- **Real data only.** No synthetic section needed — the claim itself is about real markets. The synthetic intuition was built in Notebooks 001–005.
- **Connect back explicitly.** Every concept references a prior notebook or markdown doc. "In Notebook 001, you saw that different samples give different means. The 8% claim is just one sample's mean."
- **Notebook numbering:** Continue from the existing series. Notebook 001 is done. These are 006 and 007 (002–005 are already planned for sampling distribution, standard error, data-vs-sampling, and CLT).
- **Tone:** Conversational. "Let's fact-check something you've heard a thousand times."
- **No new statistics concepts.** CIs were covered in the markdown docs (002_sample-mean-as-estimator.md Section 6). These notebooks apply that knowledge, they don't teach it.

---

## 7. File Layout

```
notebooks/sample-mean/
├── 006_sp500-eight-percent-claim.ipynb
├── 007_sp500-confidence-interval.ipynb
└── ...
```

Plan location:
```
sessions/sample-mean/notebooks/
├── 001_sampling-distribution-plan.md      ← existing (notebooks 001–005)
└── 002_sp500-eight-percent-plan.md        ← this plan (notebooks 006–007)
```

---

## 8. Questions for You

1. **Scope:** Two notebooks feel right? Or collapse into one? Expand to three?

2. **Depth on the CI:** Notebook 2 has a CI and "required n" calculation. Is that the right depth, or too much? The "required n" part is a bit of a party trick — mathematically correct but practically absurd (the answer is hundreds of years). Keep it?

3. **Tone:** "Conversational fact-check" — does that work, or keep the more formal teaching tone from the earlier docs?

4. **Rolling window in Notebook 1:** I suggested a rolling 10-year mean plot. Ten years is long enough to smooth some noise but short enough to show variation. Right window?

5. **Order:** Build these after completing notebooks 002–005 (the planned sampling distribution series), or jump ahead and build 006–007 now since they're self-contained and only need Notebook 001 as a prerequisite?