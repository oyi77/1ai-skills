---
name: viz-creator
description: Use when creating data visualizations for analysis or client deliverables — distribution plots, correlation heatmaps, and time-series charts using matplotlib and seaborn.
domain: data
tags: [analytics, visualization, data-analysis, matplotlib, seaborn]
version: 1.0.0
---

# Viz Creator

> **Redirect stub — full documentation at parent [data/analysis](../SKILL.md). This page is a quick reference for standalone use.**

## Quick Reference

Data visualization turns analytical findings into immediately digestible charts. This skill covers three essential chart types using **matplotlib** and **seaborn**: distribution histograms (for understanding value spreads), correlation heatmaps (for feature relationships), and time-series line charts (for trends over time). All output is static PNG, formatted for embedding in HTML reports or client presentations.

The parent skill covers the full pipeline (clean → detect → report → visualize) with money-making protocol and orchestration.

### Quick Start

1. **Select numeric columns** — Identify 3–5 key metrics that tell the story (not every column)
2. **Generate charts** — Call `plot_numeric_distributions()`, `plot_correlation_heatmap()`, and `plot_time_series()` as needed
3. **Embed in report** — Pass the returned file paths as `<img>` tags into `generate_report()`

### Focused Code Example

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path

df = pd.read_csv("client_data.csv")
Path("charts").mkdir(exist_ok=True)

# Distribution — histogram with KDE overlay
fig, ax = plt.subplots(figsize=(10, 4))
sns.histplot(df["revenue"].dropna(), kde=True, ax=ax)
ax.set_title("Distribution of Revenue")
plt.tight_layout()
fig.savefig("charts/revenue_dist.png", dpi=150)
plt.close(fig)

# Correlation heatmap — pairwise numeric relationships
numeric = df.select_dtypes(include=["float64", "int64"])
fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(numeric.corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
ax.set_title("Feature Correlation Matrix")
plt.tight_layout()
fig.savefig("charts/correlation.png", dpi=150)
plt.close(fig)

# Time series — line chart over date
if "date" in df.columns and "revenue" in df.columns:
    series = df[["date", "revenue"]].dropna().sort_values("date")
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(series["date"], series["revenue"], linewidth=1)
    ax.set_title("Revenue over Time")
    plt.xticks(rotation=45)
    plt.tight_layout()
    fig.savefig("charts/revenue_timeseries.png", dpi=150)
    plt.close(fig)

print("Charts saved to charts/")
```

### Verification Checklist

- [ ] Distribution plots generated for 3–5 key numeric columns (histogram + KDE)
- [ ] Correlation heatmap created with annotated coefficients (annot=True)
- [ ] Time-series chart rendered with readable date labels (rotate if crowded)
- [ ] All charts saved at 150+ DPI for print-quality client deliverables
- [ ] Color palette is colorblind-friendly (use `cmap="viridis"` or `sns.color_palette("colorblind")`)
- [ ] Chart titles are client-appropriate, not internal column names
- [ ] No chart has cut-off labels or overlapping axis text (check figsize + rotation)

### Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I need Tableau for professional client work" | Static matplotlib/seaborn charts at 150 DPI look indistinguishable from BI tool output in a report. Start here — add interactivity only when a client specifically requests it and pays for it. |
| "More charts means more value" | Three well-chosen charts that tell a story beat 20 auto-generated histograms. Choose one chart per key finding. |
| "Default matplotlib settings are good enough" | Default colors are ugly and font sizes are too small. Always customize: set dpi=150, use seaborn styles, add clear titles, and choose colorblind-safe palettes. |
| "Interactive charts are always better" | Static PNG: opens everywhere, renders instantly, embeds in any report. Interactive adds complexity. Default to static, upsell interactive Plotly at $200 extra. |

## When to Use
Use this skill when creating data visualizations for analysis or client deliverables — distribution plots, correlation heatmaps, and time-series charts using matplotlib and seaborn.

## Workflow
See the parent skill for authoritative workflow documentation.
