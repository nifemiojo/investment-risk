# The Mean Doesn't Have to Be an Observed Value

**Session:** sample-mean  
**Topic:** The sample mean as an abstract summary — it may never appear in your data  
**Prerequisites:** sample-mean/001 (sample mean as first raw moment), sample-mean/002 (sample mean as estimator), location/001 (location overview), location/002 (what is centre)

---

## 1. Start with a Story: The Average Family

### 1.1 2.4 Children

You've heard the statistic: "the average British family has 2.4 children."

Have you ever met a family with 2.4 children? Of course not. You can't have four-tenths of a child. Every actual family has 0, 1, 2, 3, 4... children — whole numbers. But the average across all families is 2.4.

This number — 2.4 — **is a perfectly valid, meaningful summary of British families.** It tells you something real: families tend to have 2 or 3 children, with a slight tilt toward 2. It's useful for planning school places, housing policy, and demographic projections.

But 2.4 is not a description of any actual family. No family looks like the average. The average is an abstraction — a single number that represents the *centre* of the data, not any specific data point.

**This is the core idea:** the mean is a mathematical summary. It lives in the space of possible summaries. It does not have to live in the space of possible observations.

### 1.2 The Mean of a Coin Flip

Flip a fair coin. Code heads = 1, tails = 0.

- Flip 1: Heads → 1
- Flip 2: Tails → 0
- Flip 3: Heads → 1
- Flip 4: Heads → 1
- Flip 5: Tails → 0

The sample mean:

$$\bar{x} = \frac{1 + 0 + 1 + 1 + 0}{5} = \frac{3}{5} = 0.6$$

Every individual flip was either 1 or 0. The mean is 0.6 — a value that **has never occurred and can never occur.** A coin flip doesn't produce 0.6. It produces heads (1) or tails (0). The mean of 0.6 is an abstract property of the *collection* of flips, not a property of any single flip.

Yet 0.6 tells you something real: heads came up 60% of the time. It's a meaningful summary — it's just not a value the coin can actually produce.

---

## 2. Why This Happens: The Mean as a Balance Point

### 2.1 The Seesaw Analogy — Refined

Imagine the number line as a seesaw (a plank balanced on a fulcrum). Each data point is a 1 kg weight placed at its value on the number line.

```
-2%        -1%         0%        +1%        +2%
 |          |          |          |          |
                         ●
                     (fulcrum at
                      the mean)
```

The mean is the point where you'd place the fulcrum so the seesaw balances perfectly — the weights on the left exactly counterbalance the weights on the right.

**Now the crucial observation:** the fulcrum doesn't have to sit where a weight already is. It can sit between weights. It can sit in a gap. It can sit at a value that has no weight on it at all. The fulcrum's job is to balance, not to coincide with a weight.

### 2.2 A Concrete Numerical Example

Three returns: −2%, +1%, +4%.

The mean: $\bar{x} = \frac{-2 + 1 + 4}{3} = \frac{3}{3} = 1\%$.

Now place them on the number line with the fulcrum at 1%:

```
Weight at -2%: distance from fulcrum = 3 units to the left
Weight at +1%: distance from fulcrum = 0 units (sits exactly on it!)
Weight at +4%: distance from fulcrum = 3 units to the right
```

The −2% weight pulls left with force proportional to distance 3. The +4% weight pulls right with force proportional to distance 3. They cancel. The seesaw balances.

Notice: the +1% return happens to sit exactly at the mean (by coincidence here). But that's not necessary. Let me change one number:

Three returns: −2%, +0.5%, +4%.

The mean: $\bar{x} = \frac{-2 + 0.5 + 4}{3} = \frac{2.5}{3} \approx 0.833\%$.

Now nobody sits at 0.833%. The fulcrum is at 0.833%, but the nearest observations are at 0.5% and 1% (which isn't even in the data). The seesaw still balances perfectly — the fulcrum just sits in empty space.

### 2.3 The Continuous Case

Financial returns are continuous — they can (in principle) take any value. In practice, with 252 daily returns, you'll never see the exact same return twice anyway. So the mean of continuous data almost always lands at a value that never occurred in the sample.

That's normal. That's how means work. The mean is not a "typical value" in the sense of "a value that actually happened." It's a typical value in the sense of "the central tendency of the collection."

---

## 3. Discrete vs Continuous: When This Matters More

### 3.1 The Distinction

| Type of data | Examples | Can the mean be an observed value? |
|---|---|---|
| **Discrete (counts)** | Number of children, daily trades, VaR exceptions, coin flips coded 0/1 | Sometimes, but often not. The mean of coin flips is a proportion (0.6), not a possible flip outcome |
| **Discrete (categories coded as numbers)** | Credit ratings (AAA=1, AA=2, ...), sentiment scores (1–5) | The mean may be 3.7 — meaningless as a specific rating, but meaningful as an average |
| **Continuous** | Daily returns, temperatures, heights | In theory, the mean *could* equal an observed value (if the data happened to average to one of its points). In practice, with real-valued data, this almost never happens |
| **Binary (0/1)** | Default/no-default, exception/no-exception | The mean IS a proportion — always between 0 and 1, never exactly 0 or 1 unless every observation is the same |

### 3.2 The Proportion Interpretation

Binary data (0/1) produces the cleanest example of this phenomenon. The mean of binary data is a proportion — a number between 0 and 1. But every individual observation is either 0 or 1.

**Example:** Over 252 trading days, your 95% VaR model should be breached on about $0.05 \times 252 \approx 13$ days. Code each day: 1 if VaR was breached, 0 if not.

$$
\bar{x} = \frac{\text{number of breaches}}{252} = \frac{7}{252} \approx 0.0278
$$

The mean is 0.0278 (a 2.78% breach rate). Every day was either 1 (breach) or 0 (no breach). The mean lives in the space between — and that's exactly where it should be. It's telling you "about 2.8% of days breached," which is a proportion, not a statement about any single day.

---

## 4. The Mean vs Other Measures of "Typical"

### 4.1 Three Ways to Be Typical

| Measure | What it means to be "typical" | Does it have to exist in the data? |
|---------|------------------------------|-----------------------------------|
| **Mean** | The balance point. The value that minimises squared error | **No.** Lives wherever the math puts it |
| **Median** | The halfway mark. 50% above, 50% below | **Not necessarily.** With an even number of observations, the median is the average of the two middle values — which may not have occurred. With an odd number, it's an actual observation |
| **Mode** | The most frequent value. The peak of the histogram | **Yes** — by definition, it's the value that appears most often |

### 4.2 Worked Example: Bimodal Returns

Imagine a strategy that mostly makes small gains but occasionally has large losses:

Daily returns over 10 days: −5%, −4%, +0.2%, +0.3%, +0.2%, +0.4%, +0.1%, −6%, +0.3%, +0.2%

Sort them: −6%, −5%, −4%, +0.1%, +0.2%, +0.2%, +0.2%, +0.3%, +0.3%, +0.4%

| Measure | Value | In the data? |
|---------|-------|-------------|
| **Mean** | $\frac{-6 + (-5) + (-4) + 0.1 + 0.2 + 0.2 + 0.2 + 0.3 + 0.3 + 0.4}{10} = \frac{-13.3}{10} = -1.33\%$ | **No.** None of the 10 returns is −1.33% |
| **Median** | Average of 5th and 6th values: $\frac{0.2 + 0.2}{2} = 0.2\%$ | **Yes.** 0.2% appears three times |
| **Mode** | The most frequent: +0.2% (appears 3 times) | **Yes.** By definition |

The mean (−1.33%) paints a very different picture from the median (+0.2%) or mode (+0.2%). The mean is pulled down by the three big losses. But **none of these losses was −1.33%** — they were −4%, −5%, and −6%. The mean synthesises all the data into a single number that didn't actually happen. It's not a lie — it accurately reflects that the losses were big enough to drag the average negative. But it's not a "typical day" in the sense of a day you'd actually experience.

### 4.3 The Mean Is Not a Prediction

This is the most important conceptual point. The mean of −1.33% does NOT mean "I expect tomorrow's return to be −1.33%." It means "the long-run average of this strategy, across many repetitions, converges to −1.33%."

The gap between "average" and "prediction for tomorrow" is enormous for financial returns. On any given day, you'll get a large loss (−5%), a small gain (+0.2%), or something in between. You won't get −1.33%. The mean summarises the *process*, not a specific *outcome*.

---

## 5. Why This Matters for Finance

### 5.1 Expected Return Is Not Typical Return

The expected return of the S&P 500 might be 0.04% per day. But look at actual daily returns:

- Some days: +1.5% (rallies)
- Some days: −2.3% (selloffs)
- Most days: somewhere in between
- Almost never: exactly +0.04%

The expected return of 0.04% is an abstraction. It's the balance point of the return distribution. It's crucial for pricing, portfolio construction, and risk budgeting. It is NOT a forecast that says "tomorrow will be +0.04%."

**This is why risk management exists.** If the mean were a reliable daily prediction, you wouldn't need VaR. You'd just collect your 0.04% every day. But the mean is a long-run property of the process — and any given day can be wildly different.

### 5.2 The Mean of a VaR Exception Series

If your 95% VaR model is correct, each day is a Bernoulli trial: breach (1) with probability 5%, no breach (0) with probability 95%.

The true mean of this process is $\mu = 0.05$ (a proportion). But no day is ever "0.05 breached." The mean is a proportion — a rate — not a description of any day. Over 252 days, you expect about 13 breaches. Any specific count will be an integer. The expected count of 12.6 is not a possible observation — but it's the correct expectation.

### 5.3 Portfolio Weights

Your optimal portfolio might allocate 23.7% to equities, 41.2% to bonds, and 35.1% to alternatives. Those are the weights that maximise expected return for a given risk level.

But you can't actually hold fractional percentages that precisely — most funds have minimum investment sizes, and rounding adds up. The mathematical optimum (a set of means from an optimisation) produces values that may not be investable. The solution is real; the investability is approximate.

### 5.4 The Danger: Treating the Abstraction as Reality

| The mistake | Why it's wrong |
|---|---|
| "The average return is 0.04%, so I should make 0.04% tomorrow" | The mean is a balance point, not a forecast. Tomorrow could be +2% or −3% |
| "The average family has 2.4 children, so the Smiths are abnormal with 2" | 2 is normal. 2.4 is an average across millions of families — no family is 2.4 |
| "The VaR model was breached on 2.8% of days, so today has a 2.8% chance of breach" | The breach probability (under the model) is 5%. The 2.8% is a sample rate — an estimate, not the truth |
| "The efficient frontier says 23.7% equities, so I'll buy exactly that" | The 23.7% is the output of a model with estimated inputs. It's not a commandment; it's a suggestion with wide error bars |

---

## 6. The Mean in the Context of Moments

### 6.1 Recall: Raw Moment $k=1$

From sample-mean/001: the sample mean is the first raw moment:

$$\bar{x} = \mu'_1 = \frac{1}{n}\sum_{i=1}^{n} x_i$$

This formula is purely mathematical. It takes $n$ numbers, adds them, divides by $n$. It doesn't check whether the result appears in the original list. It doesn't care. The formula produces a number in the *convex hull* of the data — somewhere between the minimum and maximum. But as we've seen, "between the minimum and maximum" leaves plenty of room for values that never occurred.

### 6.2 Higher Moments Have the Same Property

| Moment | Formula | Can it be an observed value? |
|--------|---------|------------------------------|
| Mean ($\mu'_1$) | $\frac{1}{n}\sum x_i$ | Almost never for continuous data |
| Variance ($\mu_2$) | $\frac{1}{n}\sum (x_i - \bar{x})^2$ | Almost never — it's an average of squared deviations |
| Skewness | Standardised third central moment | Almost never |
| Kurtosis | Standardised fourth central moment | Almost never |

**Every moment is an abstraction.** They are summary statistics — mathematical functions of the data that condense it into single numbers. None of them needs to correspond to an actual observation. Their job is to describe *properties of the distribution*, not to identify specific data points.

### 6.3 The Only Time the Mean Must Be an Observed Value

If all observations are identical — every day the return is exactly +0.5% — then the mean is +0.5%, and yes, it equals every observation. But that's a degenerate case. In any real dataset with any variation, the mean typically lands at a value that never occurred.

---

## 7. Counterexamples: When the Mean IS an Observed Value

It's worth noting the cases where the mean does coincide with an observation — because they help clarify the general rule.

### 7.1 Symmetric Data with a Centre Point

Five returns: −2%, −1%, 0%, +1%, +2%.

Mean: $\frac{-2 + (-1) + 0 + 1 + 2}{5} = \frac{0}{5} = 0\%$.

Zero is in the data. Symmetry around a central observation guarantees this.

### 7.2 Small Discrete Sets with the Right Numbers

Three coin flips: 0, 1, 1.

Mean: $\frac{0 + 1 + 1}{3} = \frac{2}{3} \approx 0.667$. Not in the data.

Two coin flips: 0, 1.

Mean: $\frac{0 + 1}{2} = 0.5$. Not in the data (flips are 0 or 1).

But two flips: 1, 1. Mean = 1. In the data (both flips are 1).  

Or: 0, 0. Mean = 0. In the data.

The mean equals an observed value only when all observations are the same (trivial) or when the numbers happen to balance perfectly at a value that's already present (rare coincidence in anything but the smallest datasets).

---

## 8. The Bigger Picture: Summaries vs Observations

### 8.1 Two Different Spaces

| | Space of observations | Space of summaries |
|---|---|---|
| **What lives here** | Actual daily returns. −2.1%, +0.3%, +1.2%... | The mean, the median, the variance, the VaR |
| **How many values** | As many as you have observations ($n$) | As many summaries as you choose to compute |
| **Are they "real"?** | Yes — these are what actually happened | Yes — but in a different sense. They're real *properties* of the data, not real data points |
| **Example** | "On March 15 2024, SPY returned −1.2%" | "The average daily SPY return over the last year was 0.04%" |

### 8.2 The Mean Lives in Summary Space

Once you compute $\bar{x} = 0.04\%$, that number is a real, valid summary. It exists. It describes something true about your data. It just doesn't describe any particular day.

This is not a flaw. It's the entire point of summarisation. If you wanted to talk about specific observed values, you'd list the returns. You compute the mean precisely because you want something that is NOT any particular observation — you want the central tendency of the whole collection.

---

## 9. Summary

| Concept | The idea | Concrete anchor |
|---|---|---|
| **Mean ≠ observed value** | The mean is a mathematical summary. It doesn't need to appear in the data | Average family has 2.4 children. No family has 2.4 children |
| **The mean of binary data** | A proportion between 0 and 1. Every observation is 0 or 1 | 7 VaR breaches in 252 days → mean = 0.0278. No day is 0.0278 breached |
| **Balance point** | The fulcrum that makes the seesaw balance. Can sit between weights | Returns −2%, +0.5%, +4% → mean = 0.833%. No observation at 0.833% |
| **Expected return ≠ typical return** | The long-run average is not a forecast for tomorrow | SPY expected daily return ≈ 0.04%. Actual days: −2.3%, +1.5%, etc. |
| **All moments are abstractions** | Mean, variance, skewness, kurtosis — none needs to exist in the data | They describe *properties of the distribution*, not specific observations |
| **Summary space vs observation space** | Summaries are real properties of the collection, not real data points | "Average return was 0.04%" is a true statement about the year — it's just not a statement about any single day |

---

## 10. Check-in Questions

1. **You flip a fair coin 10 times: H, T, H, H, T, T, H, T, H, H. Code H=1, T=0. Compute the mean. Is this value something a coin flip can produce? What does it actually represent?**

2. **A portfolio has these 5 daily returns: −3%, +7%, −1%, +2%, 0%. Compute the mean. Does it equal any of the observed returns? Place the five returns on a number line and explain where the fulcrum sits and why.**

3. **Why is "the expected daily return is 0.04%" NOT the same as "I expect tomorrow's return to be 0.04%"? What's the difference between a long-run average and a point prediction?**

4. **The mode of a dataset is, by definition, an observed value. The mean usually isn't. The median sometimes is, sometimes isn't. For each measure, explain what kind of "centre" it describes and why it does or doesn't need to exist in the data.**

5. **Your 95% VaR model expects 5% of days to breach, or about 12.6 days out of 252. Why is 12.6 a meaningful number even though you can't observe 12.6 breach days? What does the 0.6 represent?**

6. **A colleague says: "The average return of this strategy is −1.33% per day, so every day I hold it, I lose 1.33%." Looking at the bimodal example in Section 4.2, explain what's wrong with this statement. What does −1.33% actually tell you?**

7. **All moments (mean, variance, skewness, kurtosis) are computed from the data but almost never equal any observation in the data. Why is this not a problem? What is the purpose of a summary statistic?**