---
name: report-gen
description: Use when transforming analysis results into client-ready deliverables — branded HTML or Markdown reports from data profiles, cleaning summaries, anomaly findings, and visualizations.
domain: data
tags: [analytics, report, data-analysis, delivery]
version: 1.0.0
---

# Report Gen

> **Redirect stub — full documentation at parent [data/analysis](../SKILL.md). This page is a quick reference for standalone use.**

## Quick Reference

Report generation wraps raw analysis outputs into a polished deliverable that clients can open in a browser or paste into Notion. This skill produces **branded HTML reports** (with CSS, embedded charts, and structured sections) and **Markdown reports** (for GitHub, Notion, or Slack). The HTML template supports dataset overview, cleaning summary, anomaly findings, and visualization sections — all assembled from the earlier pipeline phases.

The parent skill covers the full pipeline (clean → detect → report → visualize) with money-making protocol for scoping report-only engagements.

### Quick Start

1. **Collect phase outputs** — Profile dict, cleaning report string, anomaly summary string, list of chart HTML/img tags
2. **Call the generator** — `generate_report(profile, cleaning, anomaly, charts, title="Client Analysis")`
3. **Deliver** — Write the output HTML to a file and zip with charts/ folder and optional Markdown version

### Focused Code Example

```python
from datetime import datetime
from pathlib import Path

def generate_report(profile: dict, cleaning: str, anomaly: str,
                    charts: list[str], title: str = "Data Analysis Report") -> str:
    """Build a branded standalone HTML report from analysis phase outputs."""
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{title}</title>
<style>
  body {{ font-family: -apple-system, sans-serif; max-width: 960px; margin: auto; padding: 2rem; }}
  h1 {{ color: #1a1a2e; border-bottom: 3px solid #e94560; }}
  h2 {{ color: #16213e; margin-top: 2rem; }}
  .stat {{ background: #f8f9fa; padding: 1rem; border-radius: 8px; }}
  .anomaly {{ background: #fff3cd; padding: 1rem; border-left: 4px solid #ffc107; }}
  .chart {{ margin: 1.5rem 0; }}
  pre {{ background: #f4f4f4; padding: 1rem; overflow-x: auto; }}
</style></head><body>
<h1>{title}</h1>
<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
<h2>Dataset Overview</h2>
<div class="stat"><strong>Rows:</strong> {profile['rows']} | <strong>Columns:</strong> {profile['columns']} | <strong>Duplicates:</strong> {profile['duplicates']}</div>
<h2>Data Cleaning</h2><pre>{cleaning}</pre>
<h2>Anomaly Detection</h2><div class="anomaly">{anomaly}</div>
<h2>Visualizations</h2>{"".join(f'<div class="chart">{c}</div>' for c in charts)}
</body></html>"""

# Usage
report = generate_report(profile, cleaning, anomaly,
    ['<img src="charts/age_dist.png" style="max-width:100%">'],
    "Q4 Revenue Analysis")
Path("report.html").write_text(report)
print("Report written — open report.html in a browser")
```

### Verification Checklist

- [ ] HTML renders without errors in a browser (test this before delivering)
- [ ] Branding applied (color scheme, logo placeholder if promised to client)
- [ ] All sections present: overview, cleaning, anomaly, visualizations
- [ ] Chart images are embedded or referenced with correct relative paths
- [ ] No debug print statements, traceback outputs, or raw Python objects visible
- [ ] Date/timestamp reflects when the report was generated
- [ ] Markdown version generated alongside HTML for Notion/GitHub distribution

### Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll build the report template later" | Every client wants branding. Template-first saves 2 hours per engagement. Charge for the branded template as a line item. |
| "PDF is the only professional format" | HTML loads instantly, supports interactive charts, and can be printed to PDF on demand. Deliver HTML + Markdown, not PDF. |
| "One report format fits all clients" | Execs want executive briefs (3 bullets). Analysts want raw data. Always offer two versions: full HTML report + one-page executive summary. |
| "Copy-paste into email is faster" | A self-contained HTML report looks 10× more professional than raw output pasted into a message. The 15 minutes to generate it pays back in client trust. |

## When to Use
Use this skill when transforming analysis results into client-ready deliverables — generating branded HTML or Markdown reports from data profiles, cleaning summaries, anomaly findings, and visualizations.

## Workflow
See the parent skill for authoritative workflow documentation.
