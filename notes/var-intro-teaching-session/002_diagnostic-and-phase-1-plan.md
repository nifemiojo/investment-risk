# Diagnostic & Phase 1 Plan

**Where are you now?**

---

## Your Current State

**On VaR:**
- You've *seen* VaR outputs at Spreadex
- You haven't *studied* the calculation
- Your mental model is hazy
- You've never done it by hand

**What you need:**
- Build it (both methods)
- Understand it (when it works, when it fails)
- Validate it (against Spreadex production)
- Interview-ready artifact

**Time investment:** 
- Phase 1 (this week): 4-6 hours
- Phase 2 (next 2 weeks): 8-10 hours
- Total to dangerous-good level: ~20 hours

---

## Phase 1: Foundation (This Session)

### Goals
- ✅ Build working VaR calculators (2 methods)
- ✅ Understand the numbers (what do they mean?)
- ✅ Learn when each method works/fails
- ✅ Get reference materials (for interviews)

### What We'll Do

**Step 1: Historical VaR** (File 003)
- Simplest method: sort returns, find percentile
- Run on real market data (SPY + BND, 60/40 portfolio)
- See: "On 95% of days, portfolio loses at most X"

**Step 2: Parametric VaR** (File 005)
- Formula-based: assume normal distribution
- VaR = Mean - (Z-score × Volatility)
- Compare to historical: when do they agree? When do they diverge?

**Step 3: Reference Materials** (File 007)
- 10 questions you should answer from memory
- Use for interview prep

**Step 4: Production Context** (File 008)
- How VaR integrates at Spreadex
- 4 real scenarios

---

## Phase 2: Real Scenarios (Next 2 Weeks)

### Goals
- Build VaR on actual Spreadex data
- Validate against production system
- Find one improvement
- Document findings

### What You'll Do

1. **Week 1:** Pick a live position at Spreadex
   - Download position data (tickers, sizes, dates)
   - Recreate VaR calculation using file 003 as template
   - Compare your result to Spreadex's system
   - Debug if different

2. **Week 2:** Build production memo
   - 1-2 pages
   - What's the risk? How VaR addresses it? Where it fails?
   - Your improvement proposal
   - This is CV-worthy

---

## Phase 3: Edge Cases & Failures (Optional, Deeper)

**Topics (if time):**
- Why VaR fails in crises (2008, COVID, 2022)
- Expected Shortfall (better tail metric)
- Correlation breakdowns
- Stress testing frameworks

---

## Before You Continue

**Answer these quick diagnostic questions (for yourself):**

1. Can you explain VaR in 60 seconds? (Try now. Write it down.)
2. Do you know the formula for parametric VaR? (Don't look it up.)
3. Have you ever sorted an array and found a percentile? (Conceptually, yes?)
4. What's the main difference between historical and parametric methods?

**Your answers now:**
- If unclear on all: Good. That's exactly what we're fixing.
- If you got 2-3: You have intuition. We're sharpening it.
- If you got all: You're ready for Phase 2 immediately.

No judgment. Just calibration.

---

## How to Use This Session

### For Learning
Read files 001 → 002 → 003 → ... → 010 in order. Don't skip.

### For Reference
File 007 (10 questions) is your bookmark. Return to it often.

### For Interview Prep
Files 008-009 have your story.

### For Production Deep-Dive
Use files 003-005 as templates for your Spreadex work.

---

## Key Mindset

**VaR is not magic.** It's:
- ✅ Simple enough to understand completely
- ✅ Important enough to master
- ✅ Limited enough to know when to break it

**Your job in next 2 weeks:**
- Get to "I understand this completely"
- Get to "I can improve it"
- Get to "I can explain this to a hedge fund"

---

## Next Step

Read **File 003: Historical VaR Calculator**

It's a working Python script. Your goal:
1. Understand every line
2. Run it
3. Modify it (change the portfolio, the dates, the confidence level)
4. See how results change

That's how you learn. Let's go.
