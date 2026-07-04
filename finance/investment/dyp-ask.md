# DYP-Ask: Deep Yield Potential Assessment Framework

**Portability**: 95pt | **Effort**: 3h | **Type**: Pure persona/framework | **LOC**: 187

---

## Overview

DYP-Ask is a structured interrogation framework for investment thesis validation. It combines Warren Buffett's "circle of competence" discipline with systematic doubt to identify blind spots in investment research.

**Core principle**: Better questions → better analysis → better decisions.

---

## The 12-Question Protocol

### 1. **What is the core business?**
Describe in one sentence. If you can't, you don't understand it.
- ✓ Example: "Shopee is a marketplace that takes a commission on every transaction."
- ✗ Vague: "Shopee operates across Southeast Asia."

### 2. **What problem does it solve?**
For customers. For society. For the founder.
- Link to TAM (total addressable market).
- Assess urgency: Nice-to-have vs. must-have.

### 3. **Why can this company capture value?**
Identify the moat (defensibility):
- Network effects (Shopee vs. competitors)
- Switching costs (hard to leave)
- Brand (Berkshire's reputation)
- Cost advantage (Alibaba's infrastructure)
- Proprietary tech (Tesla's battery)

### 4. **Who are the real competitors?**
Not the obvious ones.
- Direct: Lazada, Amazon, others in same space.
- Indirect: Other uses of customer money (save vs. spend).
- Future: Emerging threats in 2-5 years.

### 5. **What assumptions underlie the bull case?**
List them explicitly:
- Market growth (GMV CAGR)
- Take rate stability
- Unit economics
- Regulatory environment

### 6. **Which of these assumptions could be wrong?**
Stress-test each:
- What if take rate compresses 30%?
- What if GMV growth slows to 5%?
- What if a regulator imposes caps?

### 7. **What does the balance sheet really show?**
Beyond the headline:
- Quality of earnings (cash vs. accrual)
- Working capital trends
- Hidden liabilities (operating leases, contingencies)
- Debt structure (covenant risk)

### 8. **Is management aligned with shareholders?**
- Skin in the game (ownership %)
- Compensation structure (stock vs. cash)
- Track record of capital allocation
- Communication transparency

### 9. **At what price is this fairly valued?**
- DCF base case (explicit assumptions)
- DCF bear case (margin of safety)
- Peer multiples (why different?)
- Historical range (cyclicality)

### 10. **What is your personal conviction level?**
0-100 scale:
- 90+: Core holding, never sell
- 70-89: High conviction, buy more on dips
- 50-69: Moderate, position-size accordingly
- <50: Pass or research more

### 11. **What would change your mind?**
- Specific numbers that would trigger a sell
- Market signals to monitor
- Quarterly milestones that could disappoint

### 12. **Am I right for the right reasons?**
- Is your thesis documented?
- Can you explain it to a 10-year-old?
- Have you tested it against counterarguments?

---

## Usage Pattern

### For New Investments
```
1. Initial thesis (1-2 pages)
2. Run 12-question protocol
3. Identify key risks
4. Set entry/exit criteria
5. Document assumptions
6. Compare vs. alternatives
```

### For Portfolio Review
```
Quarterly:
- Re-run Q3, Q5, Q6 (stress-test assumptions)
- Check Q8 (management changes?)
- Verify Q11 (sell triggers hit?)

Annually:
- Full 12-question refresh
- Update fair value (Q9)
- Reassess conviction (Q10)
```

### For Disagreement Resolution
When you and a peer disagree on a stock:
```
1. Each answers all 12 questions independently
2. Compare where assumptions diverge
3. Debate only the 2-3 questions with biggest gap
4. Rest is usually just confidence level or risk tolerance
```

---

## Common Failure Modes & Fixes

| Failure | Why It Happens | Fix |
|---------|----------------|-----|
| Q1 too vague | Lazy thinking | Rewrite until a child understands |
| Q3 missing moat | Analyst missed competitive intensity | Reverse-engineer competitor advantage |
| Q5 too optimistic | Confirmation bias | Have a skeptic challenge each assumption |
| Q7 balance sheet ignored | "It's just accounting" | Trace 3 years of cash flow; find the gap |
| Q8 management dismissed | "Numbers matter more" | Check CEO turnover, stock sales in last year |
| Q9 no margin of safety | "Fair value is fair value" | Your range should be ±30% minimum |
| Q10 conviction inflated | "I already bought it" | Refresh after Q3 earnings; gut-check |

---

## Integration with 1ai-Ecosystem

### Trigger Skills
- `thesis-tracker`: Store and version control your answers
- `thesis-drift`: Monitor which assumptions are breaking
- `quality-screen`: Pre-filter stocks before running DYP-Ask
- `investment-checklist`: Apply after DYP-Ask passes

### Output Format
```json
{
  "stock": "SHOP",
  "date": "2026-07-04",
  "answers": {
    "q1_core_business": "Shopee takes commission on marketplace transactions across SEA.",
    "q3_moat": "Network effects + scale + ecosystem stickiness",
    "q5_assumptions": ["GMV CAGR 15%", "Take rate 2.5%", "Regulatory stable"],
    "q6_stress_test": ["GMV drops to 8% CAGR", "Take rate compressed 20%"],
    "q9_dcf_base_fair_value": "$32-40",
    "q10_conviction": 72
  },
  "recommendation": "BUY below $30"
}
```

---

## References

**Warren Buffett's Circle of Competence**: Invest only in businesses you fully understand.

**Charlie Munger's Inversion**: Instead of asking "why succeed?", ask "how could this fail?"

**Benjamin Graham's Margin of Safety**: Never pay close to intrinsic value; demand a discount.

---

## Next Steps in 1ai-Ecosystem

1. ✅ Deploy DYP-Ask to 1ai-skills
2. → Integrate with `thesis-tracker` for persistent storage
3. → Build dashboard showing conviction vs. price
4. → Add peer benchmarking (how do others score?)
5. → Connect to alert system (when Q11 triggers fire)

**Status**: Ready for TIER 1 deployment. Zero external dependencies.
