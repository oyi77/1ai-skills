# Growth Engine

## Persona

**The Data-Driven Growth Architect** - Inspired by high-performance marketing teams at companies like Airbnb, Dropbox, and Uber. This skill embodies the experimental mindset of growth hackers who combine creativity with rigorous statistical validation to scale products exponentially.

**Core Philosophy:** Growth is not magic—it's a systematic process of hypothesis generation, rapid experimentation, and evidence-based decision making. Every tactic is a test; every metric is a lesson.

---

## Skill Definition

**Name:** `growth-engine`

**Pattern:** `marketing/growth/growth-engine`

**Description:** Autonomous marketing experiment framework for systematic growth testing. Includes experiment design, statistical validation, pacing alerts, and automated optimization loops.

---

## Implementation

### Phase 1: Hypothesis Generation

**IDEA Framework for Growth Hypotheses**
```
I - Insight: What user behavior pattern did we observe?
D - Design: What change are we proposing?
E - Expected: What outcome do we predict?
A - Assumption: What must be true for this to work?
```

**Hypothesis Template:**
```
"We believe that [change] for [audience] will result in [outcome]. 
We'll know this is true when we see [metric] change by [amount] 
within [timeframe]."
```

**Priority Scoring (ICE)**
```python
def ice_score(idea):
    impact = rate_1_to_10(idea.potential_lift)      # 1-10
    confidence = rate_1_to_10(idea.evidence)       # 1-10
    ease = rate_1_to_10(10 - idea.implementation_cost)  # 1-10
    
    return (impact * confidence * ease) / 10
```

### Phase 2: Experiment Design

**A/B Test Structure**
```python
experiment = {
    "name": "Headline_Variants_Q2",
    "control": "Current headline",
    "variants": ["Variant A", "Variant B", "Variant C"],
    "metric": "click_through_rate",
    "minimum_detectable_effect": 0.15,  # 15% lift
    "significance_threshold": 0.95,     # 95% confidence
    "estimated_traffic": 10000,         # per week
    "duration_weeks": 3
}
```

**Statistical Power Analysis**
```python
from statsmodels.stats.power import NormalIndPower

power_analysis = NormalIndPower()
sample_size = power_analysis.solve_power(
    effect_size=0.15,
    alpha=0.05,
    power=0.80,
    ratio=1.0
)
```

**Randomization Strategy**
- User-level randomization (consistent experience)
- Stratified sampling (preserve segment ratios)
- Time-based bucketing (day-of-week effects)
- Device type balancing

### Phase 3: Execution & Monitoring

**Pacing Alerts**
```python
pacing_rules = {
    "traffic_allocation": {
        "alert_if_imbalance": 0.55,  # >55% to one variant
        "auto_rebalance": True
    },
    "conversion_rate": {
        "alert_if_drop": 0.20,      # 20% drop from baseline
        "pause_threshold": 0.30     # Pause if 30% drop
    },
    "sample_size": {
        "alert_if_under": 0.70,     # 70% of target
        "extend_if_needed": True
    }
}
```

**Real-Time Dashboards**
- Current lift vs control
- Confidence intervals over time
- Segment breakdowns
- Cohort retention curves

### Phase 4: Statistical Validation

**Bayesian A/B Testing**
```python
import numpy as np
from scipy import stats

def bayesian_ab_test(control_conversions, control_visitors,
                     variant_conversions, variant_visitors):
    
    # Prior: Beta(1, 1) = uniform
    control_posterior = stats.beta(1 + control_conversions,
                                   1 + control_visitors - control_conversions)
    variant_posterior = stats.beta(1 + variant_conversions,
                                   1 + variant_visitors - variant_conversions)
    
    # Monte Carlo simulation
    control_samples = control_posterior.rvs(100000)
    variant_samples = variant_posterior.rvs(100000)
    
    prob_variant_wins = np.mean(variant_samples > control_samples)
    expected_lift = np.mean((variant_samples - control_samples) / control_samples)
    
    return {
        "probability_variant_wins": prob_variant_wins,
        "expected_lift": expected_lift,
        "credible_interval": np.percentile(
            (variant_samples - control_samples) / control_samples,
            [2.5, 97.5]
        )
    }
```

**Sequential Testing (Optional)**
- Stop early if significance reached
- Always valid p-values (mSPRT)
- Avoid peeking bias

### Phase 5: Automated Optimization

**Winner Selection**
```python
def select_winner(experiment_results, confidence_threshold=0.95):
    for variant in experiment_results.variants:
        if variant.prob_beats_control >= confidence_threshold:
            return {
                "winner": variant.name,
                "confidence": variant.prob_beats_control,
                "expected_lift": variant.lift_vs_control,
                "recommendation": "IMPLEMENT"
            }
    
    if experiment.duration >= experiment.planned_duration:
        return {
            "winner": None,
            "confidence": max(v.prob_beats_control for v in experiment_results.variants),
            "recommendation": "INCONCLUSIVE - CONTINUE OR ABANDON"
        }
    
    return {"recommendation": "CONTINUE_TESTING"}
```

**Auto-Scaling Winners**
- Gradual ramp (10% → 50% → 100%)
- Monitor for novelty effect decay
- Document learnings in knowledge base

---

## Growth Experiment Types

### Acquisition Experiments

**Channel Tests**
- Paid: Google vs Facebook vs TikTok
- Organic: SEO vs Content vs Referral
- Partnership: Integration vs Co-marketing

**Creative Optimization**
- Ad copy variations
- Image vs video performance
- Landing page layouts
- CTA button text/color

**Pricing & Packaging**
- Freemium vs trial vs money-back
- Annual vs monthly preferences
- Bundle vs à la carte

### Activation Experiments

**Onboarding Flows**
- Linear vs interactive tutorial
- Progressive disclosure vs full feature tour
- Personalized vs generic welcome

**Aha Moment Optimization**
- Time to value measurement
- Key action identification
- Friction point removal

### Retention Experiments

**Engagement Mechanics**
- Notification timing optimization
- Content personalization
- Gamification elements

**Churn Prevention**
- Early warning systems
- Win-back campaigns
- Exit interview automation

### Referral Experiments

**Viral Mechanics**
- Single-sided vs double-sided incentives
- Referral value optimization
- Social proof integration

---

## Usage Examples

### Example 1: Full Experiment Lifecycle

```python
# 1. Generate hypothesis
hypothesis = growth_hypothesis(
    insight="Users who view demo video convert 3x higher",
    design="Add prominent demo CTA on homepage",
    expected="+25% demo views, +15% trial signups",
    assumption="Demo video quality resonates with target audience"
)

# 2. Design experiment
experiment = design_ab_test(
    hypothesis=hypothesis,
    variants=["demo_cta_v1", "demo_cta_v2"],
    primary_metric="trial_signup_rate",
    secondary_metrics=["demo_view_rate", "time_on_page"],
    traffic_split=[0.34, 0.33, 0.33]  # Control + 2 variants
)

# 3. Launch and monitor
experiment.launch()

while experiment.status == "RUNNING":
    daily_report = experiment.generate_report()
    
    # Check pacing alerts
    if daily_report.sample_size_alert:
        notify("Sample size behind pace")
    
    if daily_report.conversion_drop:
        experiment.pause()
        notify("Conversion rate anomaly detected")
    
    time.sleep(86400)  # Daily check

# 4. Analyze results
results = experiment.final_analysis()

if results.winner and results.confidence >= 0.95:
    implement_winner(results.winner)
    document_learning(results)
else:
    document_learning(results)  # Document negative result too
```

### Example 2: Rapid Experiment Pipeline

```python
# Run multiple micro-experiments in parallel
experiments = [
    {"type": "email_subject", "n_variants": 5, "traffic": "10%"},
    {"type": "cta_color", "n_variants": 4, "traffic": "20%"},
    {"type": "pricing_display", "n_variants": 3, "traffic": "30%"}
]

for exp_config in experiments:
    exp = create_micro_experiment(exp_config)
    exp.launch()
    
# Weekly review
candidates = []
for exp in running_experiments:
    results = exp.get_results()
    if results.confidence >= 0.90:
        candidates.append(results)
        
# Promote winners
for winner in candidates:
    rollout_gradually(winner.variant, [0.10, 0.50, 1.0])
```

### Example 3: Growth Scorecard

```python
# Generate weekly growth report
scorecard = {
    "experiments": {
        "running": 8,
        "completed_this_week": 3,
        "winners": 1,
        "inconclusive": 2
    },
    "metrics": {
        "activation_rate": {"current": 0.35, "lift": "+5%"},
        "retention_d7": {"current": 0.42, "lift": "+3%"},
        "referral_rate": {"current": 0.18, "lift": "+12%"}
    },
    "velocity": {
        "experiments_per_week": 2.5,
        "win_rate": 0.33,
        "avg_lift": "8.5%"
    }
}

generate_weekly_scorecard(scorecard)
```

---

## Integration Points

**Cross-Skill Dependencies**
- `marketing/analytics-dashboard` - For metric tracking
- `content/content-scheduler` - For experiment timing
- `sales/sales` - For lead quality feedback
- `research/trendradar` - For trend-based hypotheses

**Tool Integrations**
- Analytics: Google Analytics 4, Mixpanel, Amplitude
- Testing: Optimizely, VWO, Google Optimize
- Communication: Slack for alerts
- Documentation: Notion for learnings

---

## Statistical Best Practices

### Avoiding Common Pitfalls

**1. Multiple Comparison Problem**
```python
# Bonferroni correction
n_tests = 10
alpha = 0.05
corrected_alpha = alpha / n_tests  # 0.005
```

**2. Sample Ratio Mismatch (SRM)**
```python
def check_srm(observed, expected, p_threshold=0.01):
    from scipy.stats import chisquare
    chi2, p = chisquare(observed, expected)
    return p < p_threshold  # True if SRM detected
```

**3. Novelty Effect**
- Run experiments for minimum 2 weeks
- Check for decay in lift over time
- Monitor day-of-week effects

**4. Seasonality**
- Avoid holiday periods for B2B
- Account for payday cycles
- Document external events

---

## Output Format

```yaml
growth_experiment_report:
  experiment_id: "EXP-2025-054"
  name: "Homepage_Demo_CTA_Test"
  status: "COMPLETED"
  
  hypothesis:
    insight: "Demo viewers convert 3x higher"
    design: "Add prominent demo CTA on homepage"
    expected_outcome: "+25% demo views, +15% trials"
    
  design:
    variants: 3  # Control + 2 variants
    traffic_allocation: [0.34, 0.33, 0.33]
    duration: "14 days"
    sample_size: 15000
    
  results:
    primary_metric:
      name: "trial_signup_rate"
      control: 0.045
      variant_1: 0.052  # +15.6%
      variant_2: 0.058  # +28.9%
      
    statistical_significance:
      variant_1: 0.87  # Not significant
      variant_2: 0.97  # Significant winner
      
    segments:
      mobile:
        lift: "+35%"  # Stronger on mobile
      desktop:
        lift: "+18%"
      
  winner:
    variant: "variant_2"
    confidence: 0.97
    expected_annual_impact: "+$450K ARR"
    implementation_status: "ROLLED_OUT_100%"
    
  learnings:
    - "Demo CTA above fold performs best"
    - "Mobile users more responsive to video"
    - "Consider testing autoplay vs click-to-play"
    
  next_experiments:
    - "Demo placement on pricing page"
    - "Demo length optimization"
    - "Demo personalization by segment"
```

---

## Triggers

- `/growth create-experiment` - Design new experiment
- `/growth analyze <experiment_id>` - Generate results report
- `/growth scorecard` - Weekly growth metrics
- `/growth backlog` - Prioritize experiment ideas

---

**Prerequisites:** Requires access to analytics platform and A/B testing tool. Statistical knowledge recommended but not required—framework handles calculations.

**Donation:** Support development → https://www.tip.md/oyi77

## When NOT to Use

- [TODO: Add specific exclusion cases for this skill]
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- [TODO: Add behavioral signs the skill is being violated]
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] [TODO: Add specific evidence-based checklist items]
- [ ] All required outputs generated
- [ ] Success criteria met

