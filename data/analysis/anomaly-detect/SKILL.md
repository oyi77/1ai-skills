---
name: anomaly-detect
description: Use when detecting outliers, anomalies, or unusual patterns in datasets — IQR for univariate, Isolation Forest for multivariate.
domain: data
tags: [analytics, anomaly, data-analysis, outlier-detection]
version: 1.0.0
---

# Anomaly Detect

> **Redirect stub — full documentation at parent [data/analysis](../SKILL.md). This page is a quick reference for standalone use.**

## Quick Reference

Anomaly detection identifies data points that deviate significantly from the expected pattern. This skill covers two complementary methods: **IQR-based detection** (fast, interpretable, univariate) and **Isolation Forest** (multivariate, handles feature interactions). For normally distributed data, z-score (`scipy.stats.zscore`) is a valid alternative to IQR — flag records where |z| > 3. Use IQR for quick flagging of individual column outliers; use Isolation Forest when anomalies emerge from combinations of columns.

A common client scenario: a SaaS dataset with 50K subscription records where manual inspection finds nothing, but IQR flags 200 unusually high-revenue accounts and Isolation Forest catches 50 more that look normal in every column individually but become suspicious when revenue, signup date, and cancellation rate are considered together.

The parent skill also covers the full pipeline (clean → detect → report → visualize) with money-making protocol and orchestration.

### Quick Start

1. **Profile your data** — Run `profile_dataset(df)` to understand column types and distributions. Pay special attention to numeric columns with high skew (revenue, latency, counts) — these are where IQR outliers are most likely.
2. **Choose method** — Use `detect_outliers_iqr()` for per-column outliers or `detect_anomalies_isolation_forest()` for multivariate patterns. If your data is normally distributed, `scipy.stats.zscore(df[col]).abs() > 3` is a drop-in z-score alternative to IQR.
3. **Summarize & act** — Call `anomaly_summary()` to quantify findings, then export flagged records for review


**Method comparison:**
   - IQR: best for column-by-column outlier detection on skewed data
   - Z-score: best for normally distributed data (|z| > 3)
   - Isolation Forest: best for detecting multi-column anomaly patterns
   - Start with IQR; escalate to Isolation Forest when IQR finds nothing but anomalies are suspected
In practice, start with IQR on every numeric column as a first pass, then escalate to Isolation Forest when a business stakeholder asks "are there accounts that look normal individually but suspicious together?" For the IQR pass, use `detect_outliers_iqr()` with a 1.5× multiplier; if too many records flag (above 5%), increase to 3×. For Isolation Forest, set `contamination` to match your expected anomaly rate — 0.01 for rare fraud, 0.1 for broad data quality audits.

### Focused Code Example

```python
import pandas as pd
from scipy import stats
from sklearn.ensemble import IsolationForest

df = pd.read_csv("transactions.csv")

# IQR — flag unusually large/small values per column
numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
Q1 = df["amount"].quantile(0.25)
Q3 = df["amount"].quantile(0.75)
iqr = Q3 - Q1
df["amount_outlier"] = (df["amount"] < Q1 - 1.5 * iqr) | (df["amount"] > Q3 + 1.5 * iqr)
print(f"IQR outliers in 'amount': {df['amount_outlier'].sum()}")

# Isolation Forest — catch multi-column anomalies
model = IsolationForest(contamination=0.05, random_state=42)
features = df[numeric_cols].select_dtypes(include=["float64", "int64"]).dropna()
df.loc[features.index, "is_anomaly"] = model.fit_predict(features) == -1
# The output is a dataframe with new boolean columns (amount_outlier, is_anomaly) and an anomaly_score column (negative = anomalous). Export to CSV with both flags and score so the client can audit which records were flagged and why.
print(f"Isolation Forest anomalies: {df['is_anomaly'].sum()} ({df['is_anomaly'].mean()*100:.1f}%)")
```

### Verification Checklist

- [ ] Numeric columns checked for IQR-detectable outliers
- [ ] Isolation Forest contamination parameter set based on expected anomaly rate (default 5%)
- [ ] Flagged records reviewed manually to confirm they are genuine anomalies, not data errors
- [ ] Anomaly score distribution checked — scores should be negative for outliers
- [ ] Results exported with both flag column and score for client transparency
- [ ] False positive rate estimated (domain experts should spot-check 10–20 flagged rows)

### Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Anomaly detection needs deep learning" | IQR and Isolation Forest catch 80% of real-world anomalies with zero GPU cost. Start simple — escalate only when patterns are clearly non-linear and high-dimensional. |
| "Visual inspection is enough for this dataset" | Human eyes miss subtle multivariate anomalies. Always run a statistical method as a first pass, then validate visually. |
| "A flagged record is always a problem" | Flags indicate *statistical* deviation, not *business* significance. Domain validation is mandatory — a $10M transaction may be legitimate and expected. |
| "IQR with 1.5× multiplier works universally" | For skewed distributions (revenue, latency), use 3× or scipy.stats.zscore with a higher threshold. Test multiplier sensitivity before trusting flags. |

## When to Use
Use this skill when detecting outliers, anomalies, or unusual patterns in datasets — IQR for per-column univariate flagging, Isolation Forest for multivariate interaction patterns that single-column methods miss. Also use when you need an anomaly summary report with score distributions for client deliverables.

## Workflow
See the parent skill for authoritative workflow documentation.
