# VaR Learning Resources: Foundational & Reliable

**Date:** 2026-07-03  
**Purpose:** Curated resource guide for learning VaR from first principles to production

---

## **Tier 1: Canonical Textbooks (Start Here)**

### 1. **"Value at Risk: The New Benchmark for Managing Financial Risk" (3rd Edition)**
**Author:** Philippe Jorion  
**Publisher:** McGraw-Hill Professional, 2006  
**Status:** Industry standard, most cited VaR textbook

#### Why Read It
- Comprehensive, covers historical/parametric/Monte Carlo methods
- Practical implementation focus
- Good balance of rigor and accessibility
- Exercises at end of each chapter
- Used in universities and FRM exam prep

#### What You'll Learn
- VaR fundamentals and definitions
- Historical simulation methods
- Parametric approaches (normal, Student-t)
- Backtesting and validation
- Enterprise risk management
- Operational and credit risk integration

#### Depth Level
- Intermediate (assumes basic statistics, linear algebra)
- ~600 pages, highly detailed

#### Best For
- Comprehensive foundation
- Reference material
- Interview preparation (standard questions come from here)

---

### 2. **"The Essentials of Risk Management" (2nd Edition)**
**Authors:** Michel Crouhy, Dan Galai, Robert Mark  
**Publisher:** McGraw-Hill, 2014  
**Status:** Practical, less rigorous than Jorion, more accessible

#### Why Read It
- Makes sophisticated concepts accessible to non-specialists
- Focus on "why" not just "how"
- Real-world applications and case studies
- Good coverage of operational, credit, and market risk integration

#### What You'll Learn
- VaR in enterprise risk management context
- Risk measurement methodologies
- Risk governance and frameworks
- Practical implementation challenges
- Historical case studies (useful for understanding model failures)

#### Depth Level
- Intermediate-beginner (less math than Jorion)
- ~500 pages, more narrative focused

#### Best For
- Quick foundation
- Understanding why models fail
- Risk management holistic view

---

### 3. **"Market Risk Analysis, Volume IV: Value at Risk Models"**
**Author:** Carol Alexander  
**Publisher:** Wiley, 2008  
**Status:** Academic rigor + practitioner perspective, most technical

#### Why Read It
- Most comprehensive VaR textbook available
- Deep mathematical treatment
- Covers advanced topics (EVT, backtesting, stress testing)
- Part of 4-volume Market Risk Analysis series (can read standalone)

#### What You'll Learn
- VaR fundamentals with rigorous proofs
- Historical and parametric methods with derivations
- Quantile estimation techniques
- Backtesting procedures and frameworks
- Extreme Value Theory (EVT) for tail risk
- Coherent risk measures (CVaR/Expected Shortfall)
- Volatility forecasting and correlation modeling

#### Depth Level
- Advanced (strong statistics, probability required)
- Highly technical, 800+ pages

#### Best For
- Building strong theoretical foundation
- Advanced implementations
- Research-level understanding

---

## **Tier 2: Technical Reference Documents (Industry Standard)**

### 4. **RiskMetrics Technical Document**
**Source:** MSCI (originally J.P. Morgan, 1994)  
**Format:** PDF, free download (https://www.msci.com)  
**Status:** The foundational VaR framework, still used in production

#### Why Read It
- **Defines** historical VaR as used in practice
- Practical implementation guidance
- Introduced most VaR terminology
- Still referenced in dealer systems (Spreadex likely uses elements of this)

#### What You'll Learn
- RiskMetrics methodology (exponentially weighted moving average)
- Covariance matrix estimation
- Portfolio VaR aggregation
- Interest rate delta-normal approach
- Practical data requirements

#### Depth Level
- Technical, shorter (~50 pages)
- Practical focus, less theory

#### Best For
- Understanding production systems
- Dealer risk implementation
- Quick reference

---

### 5. **Basel Committee Papers on VaR**
**Source:** Bank for International Settlements (BIS)  
**Key Document:** "Messages from the academic literature on risk measurement for the trading book" (BIS Working Paper 19)  
**Format:** PDF, free download (https://www.bis.org)  
**Status:** Regulatory perspective, important for understanding constraints

#### Why Read It
- Understanding regulatory VaR framework
- Model limitations from regulator perspective
- Backtesting requirements (Basel III)
- Limitations and alternatives to VaR

#### What You'll Learn
- Regulatory VaR definitions
- Backtesting procedures
- Model validation requirements
- RWA (risk-weighted assets) calculations
- Why regulators criticize VaR (tail risk blindness)

#### Depth Level
- Technical, shorter (~20 pages per paper)
- Policy/regulatory focus

#### Best For
- Understanding regulatory constraints
- Backtesting procedures
- Why firms have backup hedges

---

### 6. **Glyn Holton's Research Notes on VaR**
**Source:** https://www.glynholton.com/notes/value-at-risk/  
**Format:** Online reference articles  
**Status:** Practitioner-academic hybrid, free resource

#### Why Read It
- Clear explanations of VaR definitions and variations
- Critiques and limitations well-covered
- Links to other resources
- Updated with recent thinking

#### What You'll Learn
- VaR definitions and subtle distinctions
- Probabilistic interpretation
- Model risk discussion
- Practical pitfalls

#### Depth Level
- Accessible, modular

#### Best For
- Quick reference and clarification
- Understanding debates about VaR

---

## **Tier 3: Academic & Advanced (For Depth)**

### 7. **Academic Papers on VaR Failures & Improvements**

#### Key Papers to Read

**"The Problem with Value-at-Risk"** (Taleb, 2007)  
- Critical perspective on VaR limitations
- Why VaR fails in tail events
- Practical examples from 2008
- **Read if:** You want the "VaR is dangerous" perspective

**"A Brief History of Value-at-Risk"** (Jorion, 2006)  
- Historical evolution of VaR concept
- Why it became dominant
- Evolution of thinking
- **Read if:** You want context on how we got here

**"Expected Shortfall as a Coherent Risk Measure"** (Artzner et al., 1999)  
- Mathematical alternative to VaR
- Why VaR is not "coherent"
- Foundation for Expected Shortfall
- **Read if:** You want to understand why VaR is mathematically flawed

**"Backtesting Value-at-Risk Models"** (Jorion, 1996)  
- How to validate if your VaR model is working
- Statistical tests for VaR
- When to reject a model
- **Read if:** You need to audit production VaR systems

---

### 8. **FRM (Financial Risk Manager) Study Materials**
**Source:** GARP (https://www.garp.org)  
**Format:** Comprehensive curriculum, Part 1 Book 2  
**Status:** Industry exam, covers VaR in structured way

#### Why Read It
- Structured curriculum designed for practitioners
- Builds from foundations to practical
- Includes practice problems
- Aligned with Basel/regulatory framework

#### What You'll Learn
- Same as textbooks but organized as exam prep
- Strong on backtesting and validation
- Good problem sets

#### Depth Level
- Varies, comprehensive coverage

#### Best For
- Structured learning path
- If considering FRM certification
- Practice problems and quizzes

---

## **Tier 4: Practitioner Resources (Implementation Focus)**

### 9. **Your Production System Documentation**
**At Spreadex:** 
- Ask for: VaR model documentation
- Ask for: Backtesting reports
- Ask for: Model validation procedures

#### What You'll Learn
- How VaR actually works at your firm
- Window size, percentile, confidence level
- Backtesting methodology
- When they override the model

---

### 10. **Risk Management Blogs & Communities**
**Glyn Holton's site** (https://www.glynholton.com)  
**Risk Academy** (https://riskacademy.blog)  
**r/FRM** (Reddit, active community)  
**LinkedIn Risk Management Groups**

#### Why Read It
- Current conversations about VaR
- How practitioners think about it
- Model improvements being discussed
- Real-world failures analyzed

---

## **Reading Roadmap: Where to Start**

### **If You Have 40 Hours** (Deep Foundation)
1. **Crouhy et al. "Essentials" (2-3 hours)** → Get the big picture
2. **Jorion "Value at Risk" Chapters 1-5 (8-10 hours)** → Core methods
3. **RiskMetrics Technical Document (2 hours)** → Production implementation
4. **Your own notebooks (003, 005)** → See it work
5. **Basel Committee papers (3-4 hours)** → Why regulators care
6. **Jorion chapters 6-10 (6-8 hours)** → Applications and limits
7. **Alexander "Market Risk Analysis Vol IV" selected chapters (10-12 hours)** → Advanced topics

### **If You Have 20 Hours** (Quick Foundation)
1. **Crouhy et al. "Essentials" (2-3 hours)**
2. **Jorion "Value at Risk" Chapters 1-5 (8-10 hours)**
3. **RiskMetrics Technical Document (2 hours)**
4. **Your notebooks + Holton's notes (4-5 hours)**

### **If You Have 10 Hours** (Minimum Viable)
1. **Crouhy et al. "Essentials" Chapters on VaR (3-4 hours)**
2. **Your notebooks 003, 005 + teaching materials (4-5 hours)**
3. **Holton's online reference (1-2 hours)**

---

## **What Each Resource Covers**

| Topic | Jorion | Crouhy | Alexander | RiskMetrics | Basel |
|-------|--------|--------|-----------|-------------|-------|
| Historical method | ✅✅✅ | ✅✅ | ✅✅✅ | ✅✅✅ | ✅ |
| Parametric method | ✅✅✅ | ✅ | ✅✅✅ | ✅✅ | ✅ |
| Monte Carlo | ✅✅ | ✅ | ✅✅ | ✅ | -- |
| Backtesting | ✅✅✅ | ✅ | ✅✅✅ | -- | ✅✅✅ |
| Implementation | ✅✅ | ✅✅✅ | ✅✅ | ✅✅✅ | ✅ |
| Limitations | ✅ | ✅✅✅ | ✅✅✅ | -- | ✅✅ |
| Theory/rigor | ✅✅✅ | ✅ | ✅✅✅ | ✅ | ✅ |
| Case studies | ✅ | ✅✅✅ | ✅ | -- | -- |

---

## **For Your Career Path (Systematic Multi-Asset Investing)**

**Focus on:**
1. **Portfolio VaR** (not just single-asset)
2. **Correlation structures** and breakdowns
3. **Multi-asset integration** (equities, FX, commodities, futures)
4. **Expected Shortfall** (CVaR) — portfolio downside beyond VaR
5. **Stress testing framework** — what happens when normal breaks

**Read these specifically:**
- Jorion chapters on portfolio VaR and backtesting
- Alexander on correlation modeling and EVT
- Basel papers on stressed VaR

---

## **For Spreadex Production Deep-Dive**

Once you're in production, ask for:
1. VaR model documentation (what method, what parameters)
2. Historical vs. parametric comparison process
3. Backtesting reports (does the model pass tests?)
4. Override procedures (when do traders ignore VaR?)
5. Correlation matrix estimation (how updated, what data)
6. Multi-asset aggregation (equities + FX + futures, how combined?)

---

## **Online Communities & Continuing Education**

If you want ongoing learning:
- **FRM Exam** (2-3 months, industry-recognized)
- **CFA Level 2** (portfolio management, risk depth)
- **GARP Risk Academy** (short courses, free resources)
- **Practitioners' conferences** (once you're in the industry)

---

## **What You Should Have After Reading**

### Conceptual Understanding
- ✅ What VaR is (percentile, not forecast)
- ✅ Difference between confidence and percentile
- ✅ Historical vs. parametric trade-offs
- ✅ Why it fails (regime change, fat tails, correlations)
- ✅ When to trust it vs. override it

### Technical Capability
- ✅ Calculate VaR by hand (percentile)
- ✅ Implement Historical VaR in code
- ✅ Understand parametric formula derivation
- ✅ Backtest a VaR model
- ✅ Interpret backtesting results

### Production Ready
- ✅ Understand your firm's VaR model
- ✅ Know when it's breaking
- ✅ Know what hedges trigger at what levels
- ✅ Can explain to non-technical people
- ✅ Can audit model for accuracy

---

## **My Recommendation for You**

**Start with:** Crouhy et al. "Essentials" (2-3 hours) for big picture  
**Then:** Jorion chapters 1-5 (core methods, ~10 hours)  
**Practical:** Your notebooks + RiskMetrics doc  
**Deep dive:** Alexander for advanced topics after you're in production  

**Timeline:** 30 hours over next 2-3 weeks  
**Outcome:** Dangerous-good foundation for Spreadex work

---

## **Books You Should Have Access To**

### Amazon/Library
1. Jorion - "Value at Risk" (3rd Ed) - **Essential**
2. Crouhy et al. - "Essentials of Risk Management" - **Highly recommended**
3. Alexander - "Market Risk Analysis Vol IV" - **Reference, advanced**

### Free Online
1. RiskMetrics Technical Document (MSCI)
2. Basel Committee papers (BIS)
3. Glyn Holton's research notes
4. FRM study materials sample (GARP)

---

## **Next Steps**

1. **Get Jorion's book** (or library access) this week
2. **Read Crouhy chapter on VaR** (overview, ~1 hour)
3. **Work through your notebooks** (seeing it in action)
4. **Tackle Jorion chapters 1-5** (8-10 hours over next 2 weeks)
5. **Come back** with questions on specific topics

Which resource appeals most to you? Want me to find specific chapters or extracts?
