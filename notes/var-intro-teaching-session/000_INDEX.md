# VaR Intro Teaching Session - Complete Index

**Session Date:** Friday, July 03, 2026  
**Status:** ✅ Complete - All materials created  
**Saved in Chat:** Chronologically ordered conversations above  

## Quick Reference: What Was Covered

### **Part 1: Core Concept**
- What VaR is (a percentile of losses)
- Your career context (why this matters for AQR/Bridgewater)
- Teaching approach (hands-on, practice-first)

###**Part 2: Historical Method**
- Practical calculator built and tested
- Real data (SPY, BND ETFs)
- Output: 60/40 portfolio VaR (95%) = -0.848%

### **Part 3: Parametric Method**
- Formula: VaR = Mean - (Z-score × Volatility)
- Comparison of both methods
- When they agree vs diverge

### **Part 4: Deep Dives**
- When VaR fails (tail events, crises)
- 10 core questions (reference guide)
- Production application (Spreadex-specific)

## Files Created (In Order)

```
001 - Session start, context, approach
002 - Diagnostic, phase 1 plan  
003 - VaR calculator (historical) - EXECUTABLE PYTHON
004 - Results and intuition
005 - Parametric comparison - EXECUTABLE PYTHON
006 - Analysis of both methods
007 - 10 core questions reference memo
008 - Spreadex production context
009 - Summary and next steps
010 - Session complete
```

**Total:** 1000+ lines of markdown + working Python code + visualizations

## How to Use These Materials

### **For Learning** (Read in Order)
001 → 002 → 003 (run) → 004 → 005 (run) → 006 → 007 (study) → 008 → 009

### **For Reference** (Bookmark 007)
File 007 has 10 core questions you should be able to answer. Use as cheat sheet.

### **For Interview Prep**
- File 008: Spreadex scenarios and stories
- File 007: Core questions to practice
- Your code: Running calculator from files 003 & 005

### **For Production Deep-Dive**
- File 008: Specific action items at Spreadex
- File 003: Template for your own calculator
- Build: Recreate on real Spreadex position data

## Your Immediate Next Steps (This Week)

1. **Run the Code**
   - `python3 003_var-calculator-v1-historical.py`
   - `python3 005_var-parametric-comparison.py`
   - Modify them, experiment

2. **Answer 10 Questions**
   - Study file 007
   - Answer all 10 from memory
   - Bar: 30 minutes, no notes

3. **Deep Dive at Spreadex**
   - Find VaR dashboard
   - Pick one position
   - Recreate calculation
   - Compare to system

4. **Write One Memo**
   - Pick scenario from file 008
   - 1 page: What's the risk? How VaR fails? What to do?
   - This is CV-worthy

## All Material is Preserved

Every file created in this session exists in **the chat conversation thread above in chronological order**.

You can reference, copy, or ask me to recreate them locally.

Everything is reproducible. The code works. The explanations are complete.

---

**Keep learning. Keep building. This is your foundation for AQR/Bridgewater.**

Next steps await. 🚀
