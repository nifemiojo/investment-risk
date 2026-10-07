# Why standardised returns have sigma ≈ 0.95, not exactly 1.0

**Date:** 2026-07-14
**Topic:** Understanding the deviation from theoretical sigma = 1 in standardised returns
**Turn:** 007c

## User observation

In Part B, the standardised returns have sigma ≈ 0.95 rather than exactly 1.0. If we divided each return by its own sigma, shouldn't the result have unit variance?

## Explanation

### The ideal case (which doesn't hold)

If you knew the *true* instantaneous volatility sigma_t for each return, then:

$$z_t = \frac{r_t}{\sigma_t}$$

would have variance exactly 1.0 (assuming r_t has zero mean). The division removes all time-varying scale.

### What we actually have

We don't know the true sigma_t. We estimate it with a 20-day trailing realised vol:

$$\hat{\sigma}_t = \sqrt{\frac{1}{20} \sum_{i=1}^{20} r_{t-i}^2}$$

This is an estimate. It has its own noise. The standardised return becomes:

$$z_t = \frac{r_t}{\hat{\sigma}_t}$$

Now the variance of z_t depends on how well sigma_hat matches the true sigma. Three reasons sigma_z deviates from 1.0:

### 1. Vol estimation noise (the main one)

Trailing realised vol is a noisy estimate. During the March 2020 crash, vol spiked from ~1% to ~5% in a matter of days. The 20-day trailing vol takes ~10 days to reflect half of that spike. So:

- During the spike: sigma_hat < true sigma → z_t = r_t / sigma_hat is TOO LARGE (inflates variance)
- After the spike: sigma_hat > true sigma → z_t = r_t / sigma_hat is TOO SMALL (deflates variance)

These two effects partially cancel but don't perfectly offset. The net result depends on the specific path of volatility.

### 2. Small sample (252 observations)

With only 252 standardised returns, the sample standard deviation has its own sampling error. Even if the true sigma were exactly 1.0, you'd expect sample sigma to bounce around between ~0.90 and ~1.10 for n=252 (standard error ≈ 1/sqrt(2×252) ≈ 0.045).

0.95 is within one standard error of 1.0 — this is consistent with random sampling variation.

### 3. The mean isn't exactly zero

SPY has a small positive daily mean (~0.05%). Dividing by sigma_t scales the mean but doesn't remove it. If some returns have μ/sigma_t > 0, the sample variance picks up a small additional component from the non-zero mean. This is negligible for daily returns.

### The practical answer

sigma_z = 0.95 is close to 1.0 and well within the sampling variation you'd expect from 252 observations with an imperfect vol estimator. If you ran the same calculation on a different 252-day window, you might get 1.05. Neither is meaningfully different from 1.0.

If sigma_z were consistently 0.75 or 1.30 across many windows, that would indicate a systematic bias in the vol estimator. But 0.95 on one window is just noise.