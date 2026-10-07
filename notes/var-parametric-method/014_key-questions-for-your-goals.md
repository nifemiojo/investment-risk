# Key Questions Given Your Goals

**Date:** 2026-07-07
**Topic:** What you should be asking, organized by timeframe and goal

---

## Your Goals (As I Understand Them)

| Timeframe | Goal |
|---|---|
| **Now** | Understand VaR deeply enough to interpret Spreadex's autohedge system |
| **6-12 months** | Build systematic investing intuition — move from "what" to "how to build" |
| **Career** | Transition from builder-at-dealer to builder-owner solving real beneficiary problems (institutional, sovereign wealth) |

---

## Questions for Monte Carlo (Immediate)

These are the questions that will make the Monte Carlo session productive:

**1. "What can Monte Carlo do that parametric and historical can't?"**

Not asking for a list of features. Asking: what specific failure modes from the last two sessions does Monte Carlo solve? Where does it fail where the others don't?

**2. "What's the actual simulation engine doing?"**

Parametric compresses data to μ̂, σ̂. Historical sorts real returns. Monte Carlo generates fake returns. How? From what distribution? With what assumptions about the data-generating process?

**3. "What parameters does Monte Carlo need, and how are they estimated?"**

Monte Carlo is still parametric at its core — you need to specify a model to simulate from. What model choices matter? How sensitive is the output to those choices?

**4. "When is Monte Carlo worth the computational cost?"**

Parametric takes microseconds. Monte Carlo might take seconds or minutes. When do you pay that price?

**5. "What are Monte Carlo's own failure modes?"**

Every method has them. What's the Monte Carlo equivalent of the "normality assumption is wrong" or "window cliff"?

---

## Questions for Production Risk Systems (Medium-Term)

These bridge from VaR methods to how risk actually works at Spreadex:

**6. "How is VaR actually calibrated in production?"**

Not the textbook version. The live system. What distribution? What window? What decay factor? What backtesting frequency? Who adjusts the parameters and when?

**7. "What happens when VaR breaches — operationally?"**

Not theoretically. At 3pm on a Tuesday when the dashboard goes red. Who gets alerted? What actions are automatic vs manual? Who has override authority?

**8. "How are position limits derived from VaR, and who sets them?"**

The chain: risk appetite → VaR limit → position limits → trader constraints. Where is judgment inserted? Where is it mechanical?

**9. "When has the model been overridden, and why?"**

The best risk managers have war stories. Find them. Ask: "Tell me about a time VaR said one thing and you did another. What did you see that the model didn't?"

---

## Questions for Systematic Investing (Career Direction)

These connect VaR to your broader thesis:

**10. "How does VaR translate into position sizing for a systematic strategy?"**

Risk parity says: equalize risk contribution. But how do you actually compute that? What happens when correlations shift? How often do you rebalance?

**11. "What's the difference between using VaR for risk control vs using it for portfolio construction?"**

Risk control: "Am I within limits?" Portfolio construction: "How do I allocate to maximize return per unit of VaR?" These are different mindsets. The second one is where systematic investing lives.

**12. "When does VaR-based risk budgeting break, and what replaces it?"**

At institutional scale, simple VaR risk budgeting fails. Tail dependence, illiquidity, regime change, non-normal distributions. What do the Bridgewaters and AQRs actually use?

**13. "How do real beneficiaries (pension funds, endowments, sovereign funds) think about risk?"**

They don't think in VaR. They think: "Will we meet our liabilities? Can we sustain spending?" VaR is the implementation layer. What's the translation layer above it?

---

## The Meta-Questions

These are the ones that separate dangerous-good from merely competent:

**14. "What am I assuming when I use this number, and what would make those assumptions break?"**

You've already internalized this for parametric VaR. Make it a reflex for every method, every model, every number you encounter.

**15. "Who is this number for, and what decision does it inform?"**

A VaR for the regulator is different from a VaR for the trader is different from a VaR for the board. Same calculation, different framing, different action. Always ask: who's the audience?

**16. "What would I need to see to stop trusting this model?"**

Define your exit criteria before you enter. What breach rate? What divergence between methods? What market conditions? If you can't answer this, you don't really understand the model's limits.

---

## Priority Order for Monte Carlo Session

If I had to pick the 3-4 that will make the Monte Carlo session most productive:

1. **What can Monte Carlo do that parametric/historical can't?** (sets the frame)
2. **What's the actual simulation engine doing?** (the mechanics)
3. **What are Monte Carlo's own failure modes?** (the critical lens)
4. **When is Monte Carlo worth the computational cost?** (the practical judgment)

The rest can unfold naturally as we go.

---

## What Am I Missing?

These questions come from my understanding of your goals. But you know your context better than I do. 

Are there questions you're holding that aren't on this list? Things you've wondered while watching the risk systems at Spreadex? Gaps in the career arc you're trying to bridge?
