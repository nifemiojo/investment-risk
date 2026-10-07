# Summary & Next Steps

**What you've learned. What to do next. How to get interview-ready.**

---

## Phase 1 Summary

You've covered:

✅ **Core concept** (File 001-002)  
  - VaR is a percentile of losses
  - Why it matters for Spreadex and your AQR career

✅ **Historical VaR** (File 003-004)  
  - Simple: sort returns, find percentile
  - Working code you can run and modify
  - Results on 60/40 portfolio: -0.85% daily VaR

✅ **Parametric VaR** (File 005-006)  
  - Formula: Mean - (Z-score × Vol)
  - When it agrees/diverges from historical
  - Why it often fails (non-normal distributions, fat tails)

✅ **Reference materials** (File 007)  
  - 10 core questions for interview prep
  - Study these until you can answer from memory

✅ **Production context** (File 008)  
  - How VaR integrates at Spreadex
  - 4 real scenarios (normal day, regime shift, correlation breakdown, cascade hedging)

---

## Phase 1 Outcomes

### Knowledge
- You understand both major VaR methods
- You know when each works and fails
- You can explain it in 60 seconds
- You have mental models for production application

### Code
- You have 2 working Python calculators
- You can run them, modify them, extend them
- You can validate against real market data

### Artifacts
- 10 interview questions (study guide)
- Production context (Spreadex application)
- Code examples (portfolio VaR, method comparison)

---

## This Week: Your Action Plan

### Monday-Wednesday
```
[ ] Read files 001-009 carefully (take notes)
[ ] Run File 003: Historical VaR calculator
    - Modify to use different dates/ETFs
    - Try different confidence levels
    - Understand the output
    
[ ] Run File 005: Parametric comparison
    - Read the diagnostics (skewness, kurtosis)
    - Understand why methods diverge
    
[ ] Answer File 007 questions (first draft, rough)
    - Don't worry about being perfect
    - Just get the ideas down
```

### Thursday-Friday
```
[ ] Visit Spreadex production
    - Find the VaR system/dashboard
    - Pick one live client position
    - Copy down: tickers, sizes, dates
    
[ ] Recreate VaR calculation
    - Use File 003 as template
    - Calculate on their position
    - Compare to Spreadex's system
    
[ ] Debug if different
    - Same lookback period?
    - Same confidence level?
    - Same calculation method?
    - Same data source?
```

---

## Next 2 Weeks: Level Up

### Week 1
```
[ ] Deep dive on Spreadex VaR system
    - Who built it? When? Why?
    - How often does it recalculate?
    - What confidence level do they use?
    - Is it historical, parametric, or hybrid?
    
[ ] Find an interesting edge case
    - Recent high-vol period?
    - Large position?
    - Unusual correlations?
    
[ ] Propose one improvement
    - Better regime detection?
    - Faster adaptation?
    - Better tail estimation?
    - Stress layer on top?
```

### Week 2
```
[ ] Document your improvement
    - 1-2 pages
    - Problem statement
    - Your proposed fix
    - How you'd validate it
    
[ ] Create code artifact
    - If you built a prototype, clean it up
    - Commented, readable
    - Could show to an interviewer
    
[ ] Write reflection memo
    - What you learned about risk at Spreadex
    - Where VaR works, where it breaks
    - How this connects to AQR/Bridgewater approach
```

---

## Interview Story (Practice This)

**Setup:** "I spent 2-3 weeks diving into Value at Risk, both theoretically and in production at Spreadex."

**The Learning:**
"I built VaR calculators from scratch using both historical and parametric methods. I tested them on real market data and validated them against Spreadex's production system. 

I learned that VaR is deceptively simple—just a percentile—but the real skill is knowing when to trust it. In normal markets, historical VaR is reliable. In stress, it often fails because it can't predict worse than history. Parametric VaR assumes a normal distribution, which also breaks in tail events.

The key insight: When historical and parametric diverge, it's a warning signal. That divergence tells you the return distribution is non-normal, and you need to investigate why."

**The Application:**
"At Spreadex, VaR is used for autohedging, margin requirements, and spread pricing. I identified a gap: the system uses a fixed 252-day lookback. During regime shifts (like 2022), correlation structure changes but VaR adapts slowly. I proposed automatically detecting regime breaks and shortening the lookback period, which would let VaR react faster.

I prototyped this and showed it would have caught the 60/40 correlation breakdown about 2 weeks faster."

**The Career Connection:**
"This is exactly what I want to do at AQR: build better risk models that know their own limitations. Not just implement existing tools, but understand them deeply enough to improve them. This project taught me that skill—both the technical building and the strategic thinking about where models break."

---

## Dangerous-Good Level

You hit dangerous-good when you can:

✅ Explain VaR to anyone (client, interviewer, engineer)  
✅ Calculate it both ways (historical + parametric)  
✅ Code it from scratch  
✅ Spot when it's wrong (correlation break, regime shift, tail event)  
✅ Propose fixes (better detection, faster adaptation, risk layering)  
✅ Tell the story (what you learned, artifacts you built)  

At that point, you're not just a user of risk models. You're a builder of risk models who happens to also know when to not trust models.

That's what gets you hired at serious firms.

---

## Reference: The 10 Questions

Always come back to **File 007**. Can you answer these?

1. What is VaR? (60 seconds)
2. Explain the two main ways to calculate VaR
3. When do historical and parametric diverge? Why?
4. What does 95% confidence actually mean?
5. Why is portfolio VaR often lower than weighted average?
6. When is VaR dangerously wrong?
7. What's the key assumption in parametric VaR? When does it break?
8. How would you validate VaR against production data?
9. At Spreadex, where does VaR integrate? (3 use cases)
10. What would you do differently if building from scratch?

---

## File Structure

```
001 - Session start + context
002 - Diagnostic + phase 1 plan
003 - Historical VaR calculator (PYTHON)
004 - Results + intuition
005 - Parametric comparison (PYTHON)
006 - Deep analysis
007 - 10 core questions (STUDY THIS)
008 - Spreadex production context
009 - Summary + next steps (this file)
010 - Final checklist (next file)
```

Read in order. Don't skip. The sequence builds understanding.

---

## Success Metrics

**By next week, you should:**
- ✅ Run both calculators smoothly
- ✅ Understand every number in the output
- ✅ Answer 7-8 of the 10 questions confidently
- ✅ Have validated VaR on 1 Spreadex position

**By end of month, you should:**
- ✅ Answer all 10 questions from memory
- ✅ Have validated on 3+ Spreadex positions
- ✅ Have identified one improvement idea
- ✅ Have written it up in a memo

**By interview time, you should:**
- ✅ Tell the full story smoothly (2-3 minutes)
- ✅ Show code + production analysis
- ✅ Discuss limitation and failure modes
- ✅ Connect to AQR/Bridgewater approach

---

## Keep Building

This is just the beginning. After VaR:
- **Expected Shortfall (CVaR)** — Average loss beyond VaR (better tail metric)
- **Stress testing** — "What if" scenarios (market crash, correlation spike, liquidity event)
- **Correlation dynamics** — How correlations change across regimes
- **Backtesting** — Did the 95th percentile actually happen 5% of the time?
- **Options Greeks** — How options amplify tail risk
- **Deep dive on Spreadex** — Multi-asset risk systems (equities + FX + futures + commodities + crypto)

Each builds on this foundation.

---

## Final Thought

VaR is table-stakes at serious firms. But **the real skill is judgment**: knowing when to trust the model, when to override it, when to add layers of protection.

You're building that muscle. Keep going.

Next file: Final checklist. Then you're done with Phase 1.

Go get it. 🚀
