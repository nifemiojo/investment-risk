# What to Focus On Next: Four Learning Paths

**Date:** 2026-07-03  
**Topic:** Mapping dangerous-good mastery from VaR foundations to production implementation

---

## **Current State: You've Mastered VaR Foundations**

✅ Component 1: The Loss (what exactly is being measured)
✅ Component 2: Time Horizon (rehedging period, data frequency)
✅ Component 3: Underlying Data (sample size, direct vs scaled)
✅ Component 4: Model Assumption (stationarity, when it breaks)
✅ LaTeX formulas with explicit term definitions

**You now understand:**
- The precise definition of VaR
- What assumptions it embeds
- When it works and when it fails
- How to frame it correctly for different audiences

---

## **Four Options for Next Level**

### **Option A: Three Calculation Methods (Historical vs Parametric vs Monte Carlo)**

**Scope:**
- How to actually calculate VaR (not just define it)
- Strengths/weaknesses of each approach
- Which assumptions each method embeds
- When to use which

**Key Questions Answered:**
- What's the difference between "historical VaR from 252 days" vs "parametric assuming normal"?
- Why do they diverge? What does the divergence signal?
- Which method is less fragile to assumption breaking?
- How would you implement each?

**Why It Matters:**
- Production reality: Spreadex probably uses one or more of these
- You need to know each method's failure modes
- Gives you the "how" to match your "what"
- Direct path to implementation

**Practical Urgency:** ⚠️ **HIGH** (you'll need this for actual coding)

**Estimated time:** 2-3 hours (learning + understanding)

---

### **Option B: Expected Shortfall (CVaR) — What Happens Beyond VaR**

**Scope:**
- VaR = threshold; ES = average loss beyond threshold
- Why ES is more informative for tail risk
- How to calculate it (quick, builds on VaR)
- Why regulators now prefer ES to VaR

**Key Questions Answered:**
- VaR says "5% of days you breach this threshold"—but how bad?
- What's the average loss on those 5% days?
- Why is this better for hedging decisions?

**Why It Matters:**
- VaR tells you "here's the boundary," not "how bad?"
- ES answers: "When I breach VaR, what's the real damage?"
- More complete risk picture for decision-making
- Regulatory trend (Basel III prefers ES)

**Practical Urgency:** 🟡 **MEDIUM** (important for hedging strategy, less urgent than methods)

**Estimated time:** 1-2 hours (relatively simple extension of VaR)

---

### **Option C: Multi-Asset Portfolio Risk (Beyond Single-Asset)**

**Scope:**
- Correlations and diversification effects
- Why 60/40 stock/bond isn't always 60/40 risk
- Portfolio VaR vs sum of individual VaRs
- When diversification fails (exact mechanism of crises)

**Key Questions Answered:**
- How do you combine individual asset risks into portfolio risk?
- When does 60/40 become 50/50 or 40/60 in a crisis?
- Why do correlations "flip" to +0.7 when you need diversification?
- How do you model tail dependence?

**Why It Matters:**
- Spreadex has multiple assets (not just one)
- Fundamental for systematic investing thesis
- Connects directly to your AQR/Bridgewater direction
- Understanding correlation breakdown = understanding crises
- Critical for position limits and rehedging

**Practical Urgency:** 🟡 **MEDIUM-HIGH** (core to portfolio thinking)

**Estimated time:** 3-4 hours (conceptually rich, worth the depth)

---

### **Option D: Backtesting & Validation (Does Your Model Actually Work?)**

**Scope:**
- Testing if your VaR predictions match reality
- Detecting when assumptions break
- Early warning systems (rolling diagnostics)
- Production monitoring procedures

**Key Questions Answered:**
- How often should VaR be breached? (Should be ~5% for 95% VaR)
- If it's breached more often, what does that signal?
- How do you set up automated alerts?
- When do you override the model?

**Why It Matters:**
- VaR is only useful if you validate it
- Catches model drift before it costs money
- Connects to "detect assumption failure" from Component 4
- Transforms VaR from theoretical to operational

**Practical Urgency:** ⚠️ **HIGH** (risk management discipline)

**Estimated time:** 2-3 hours (building validation framework)

---

## **Recommended Sequence: Action Bias First**

### **Path for Dangerous-Good Mastery at Spreadex**

**Optimal order (2-3 week learning arc):**

#### **1. Methods (A) — The "How" Layer**
- 2-3 hours
- Learn three calculation approaches
- Understand when each breaks
- Prepares you to code/implement

#### **2. Implementation Sprint — Put It to Work**
- 3-4 hours coding
- Use yfinance SPY/BND data (2024-2026)
- Calculate all three methods on same data
- Observe where they diverge (deeply enlightening!)
- See stationarity breaking live
- **Output:** Working notebook with all three methods side-by-side

#### **3. Multi-Asset Portfolio Risk (C) — Expand the Frame**
- 3-4 hours
- Calculate portfolio VaR from individual asset VaRs
- Watch correlation structure
- Build intuition for "why 2008 was worse"
- **Output:** 60/40 portfolio risk dashboard with correlation sensitivity

#### **4. Backtesting (D) — Validation & Operations**
- 2-3 hours
- Backtest models against 2024-2026 data
- Build monitoring procedures
- **Output:** Validation report + alert procedures

**Total time:** ~12-15 hours over 2 weeks
**Result:** You move from "I understand VaR" to "I can implement, monitor, and trust it"

---

## **Decision Framework: Which Path Calls to You?**

**Pick based on your learning style:**

| Your Priority | Best Next Step |
|---|---|
| **"I want quick concrete understanding"** | **A (Methods)** → Code it up → You're done |
| **"I want portfolio thinking mastery"** | **C (Multi-Asset)** → Understand diversification → Foundation for trading |
| **"I want operational discipline"** | **D (Backtesting)** → Build validation → Trust your models |
| **"I want systematic depth"** | **A → Code → C → D** (the full arc) |
| **"I want to understand tail risk better"** | **B (Expected Shortfall)** → Understand beyond-VaR losses |

---

## **My Recommendation Given Your Context**

You're at Spreadex learning dealer economics + systematic investing.

**Start with: Methods (A) → Implementation Sprint → Multi-Asset Portfolio Risk (C)**

**Why this sequence:**

1. **Methods** gives you the calculation foundation (bridge theory ↔ code)
2. **Implementation** solidifies it through building (action bias)
3. **Multi-Asset** expands to dealer/portfolio context (directly relevant to Spreadex)
4. **Backtesting** can follow when you're running models in production

This path:
- ✅ Builds from concrete to complex
- ✅ Balances theory + hands-on
- ✅ Directly relevant to Spreadex trading (multi-asset, rehedging, limits)
- ✅ Connects to your systematic investing thesis
- ✅ Gives you dangerous-good intuition

---

## **Alternative: Just Keep Going Deeper**

If you want to maximize depth before coding:

**B (Expected Shortfall) → C (Multi-Asset) → A (Methods) → Implementation**

This builds richer mental models before writing code. Slower but deeper.

---

## **What Feels Right to You?**

1. **Ready to start Methods + coding sprint?** We build all three calculators live
2. **Want to understand portfolio risk first?** We explore 60/40, correlations, tail dependence
3. **Want to start where the production rubber meets the road?** We build backtesting framework
4. **Want somewhere else entirely?** What's calling?

The session files are saved and persistent—we can pick any path and continue from here.

**What's your call?**
